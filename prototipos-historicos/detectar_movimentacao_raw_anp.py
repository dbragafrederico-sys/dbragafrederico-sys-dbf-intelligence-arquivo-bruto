"""
DBF Intelligence — Detecção de movimentação a partir de extração BRUTA da ANP
Protótipo v0.1

DIFERENÇA em relação a detectar_movimentacao.py:
  Aquele script compara duas versões do DataBook (já processado, com
  campos derivados). Este script compara a extração BRUTA da ANP
  (CSV, sem os campos derivados como porte_dbf, latitude/longitude,
  multibandeira, unidades_rede) contra o estado atual do BCU — usando
  apenas os campos que existem nos dois lados: autorização, CNPJ,
  razão social, UF/município e distribuidora/bandeira.

  Isso NÃO substitui a reconstrução de uma nova versão do DataBook
  (v10 GLP / v4 Combustíveis) — a lógica que deriva porte_dbf, classe
  numérica, multibandeira, geocodificação etc. a partir do bruto não
  está documentada em nenhum script deste projeto, e não deve ser
  reconstruída por inferência. Este script apenas cobre o caso de uso
  mais imediato e mais seguro: saber o que mudou no mercado.

Uso:
    python3 detectar_movimentacao_raw_anp.py \
        --dominio GLP --csv /caminho/cadastro-revendas-glp.csv
    python3 detectar_movimentacao_raw_anp.py \
        --dominio COMBUSTIVEIS --csv /caminho/dados-cadastrais-...csv
"""

import argparse
import csv
import sqlite3
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "dbf_bcu.sqlite"


def normalizar_nome(nome):
    if nome is None:
        return None
    s = unicodedata.normalize("NFKD", str(nome))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().upper()


def carregar_glp_bcu(conn):
    """Estado 'antigo' = o que já está carregado no BCU (DataBook v9).

    IMPORTANTE: usa vinculacao_a, não grupo_distribuidor. O DataBook v9
    guarda DOIS níveis de taxonomia de distribuidor em revenda_glp:
    vinculacao_a é a marca (ex.: 'LIQUIGÁS', 'SUPERGASBRAS ENERGIA') —
    o mesmo nível de granularidade do campo DISTRIBUIDORA da extração
    bruta da ANP. grupo_distribuidor é o grupo econômico/holding (ex.:
    'COPA ENERGIA', 'SHV ENERGY') — um rollup societário que a extração
    bruta não tem. Comparar contra grupo_distribuidor gera falsos
    positivos maciços de 'mudança de bandeira' (detectado e corrigido
    nesta sessão: 46.073 eventos espúrios, ~77% da base inteira,
    causados exatamente por essa troca de campo)."""
    registros = {}
    for numero_autorizacao, cnpj, razao_social, chave, grupo_distribuidor, bandeirada in conn.execute("""
        SELECT numero_autorizacao, cnpj, razao_social, chave_uf_municipio, vinculacao_a, bandeirada
        FROM revenda_glp
    """):
        if not numero_autorizacao:
            continue
        registros[numero_autorizacao] = {
            "cnpj": cnpj, "razao_social": razao_social, "chave_uf_municipio": chave,
            "grupo_distribuidor": grupo_distribuidor, "bandeirada": bandeirada,
        }
    return registros


def carregar_glp_csv(caminho):
    registros = {}
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            numero_autorizacao = row.get("AUTORIZACAO")
            if not numero_autorizacao:
                continue
            distribuidora = (row.get("DISTRIBUIDORA") or "").strip()
            uf, mun = row.get("UF"), normalizar_nome(row.get("MUNICIPIO"))
            chave = f"{uf}|{mun}" if uf and mun else None
            bandeirada = "Independente" if distribuidora.upper() == "INDEPENDENTE" else "Bandeirada"
            registros[numero_autorizacao] = {
                "cnpj": row.get("CNPJ"), "razao_social": row.get("RAZAOSOCIAL"),
                "chave_uf_municipio": chave, "grupo_distribuidor": distribuidora,
                "bandeirada": bandeirada,
            }
    return registros


def carregar_combustiveis_bcu(conn):
    registros = {}
    for numero_autorizacao, cnpj, razao_social, chave, bandeira in conn.execute("""
        SELECT numero_autorizacao, cnpj, razao_social, chave_uf_municipio, bandeira
        FROM posto_combustivel
    """):
        if not numero_autorizacao:
            continue
        registros[numero_autorizacao] = {
            "cnpj": cnpj, "razao_social": razao_social, "chave_uf_municipio": chave, "bandeira": bandeira,
        }
    return registros


def carregar_combustiveis_csv(caminho):
    registros = {}
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            numero_autorizacao = row.get("AUTORIZACAO")
            if not numero_autorizacao:
                continue
            uf, mun = row.get("UF"), normalizar_nome(row.get("MUNICIPIO"))
            chave = f"{uf}|{mun}" if uf and mun else None
            registros[numero_autorizacao] = {
                "cnpj": row.get("CNPJ"), "razao_social": row.get("RAZAOSOCIAL"),
                "chave_uf_municipio": chave, "bandeira": row.get("BANDEIRA"),
            }
    return registros


def comparar_glp(antigos, novos):
    eventos = []
    for autorizacao in set(antigos) & set(novos):
        a, n = antigos[autorizacao], novos[autorizacao]
        if a["bandeirada"] != n["bandeirada"]:
            tipo = "tornou_se_independente" if n["bandeirada"] == "Independente" else "saiu_de_independente"
            eventos.append((autorizacao, n["cnpj"], n["razao_social"], n["chave_uf_municipio"],
                             None, None, a["grupo_distribuidor"], n["grupo_distribuidor"],
                             a["bandeirada"], n["bandeirada"], tipo))
        elif normalizar_nome(a["grupo_distribuidor"]) != normalizar_nome(n["grupo_distribuidor"]):
            eventos.append((autorizacao, n["cnpj"], n["razao_social"], n["chave_uf_municipio"],
                             None, None, a["grupo_distribuidor"], n["grupo_distribuidor"],
                             a["bandeirada"], n["bandeirada"], "mudanca_bandeira"))
    for autorizacao in set(novos) - set(antigos):
        n = novos[autorizacao]
        eventos.append((autorizacao, n["cnpj"], n["razao_social"], n["chave_uf_municipio"],
                         None, None, None, n["grupo_distribuidor"], None, n["bandeirada"], "entrada_mercado"))
    for autorizacao in set(antigos) - set(novos):
        a = antigos[autorizacao]
        eventos.append((autorizacao, a["cnpj"], a["razao_social"], a["chave_uf_municipio"],
                         None, None, a["grupo_distribuidor"], None, a["bandeirada"], None, "saida_mercado"))
    return eventos


def comparar_combustiveis(antigos, novos):
    eventos = []
    for autorizacao in set(antigos) & set(novos):
        a, n = antigos[autorizacao], novos[autorizacao]
        if normalizar_nome(a["bandeira"]) != normalizar_nome(n["bandeira"]):
            branca_antes = str(a["bandeira"]).upper() in ("BANDEIRA BRANCA", "BRANCA", "SEM BANDEIRA")
            branca_agora = str(n["bandeira"]).upper() in ("BANDEIRA BRANCA", "BRANCA", "SEM BANDEIRA")
            if branca_agora and not branca_antes:
                tipo = "tornou_se_bandeira_branca"
            elif branca_antes and not branca_agora:
                tipo = "saiu_de_bandeira_branca"
            else:
                tipo = "mudanca_bandeira"
            eventos.append((autorizacao, n["cnpj"], n["razao_social"], n["chave_uf_municipio"],
                             a["bandeira"], n["bandeira"], tipo))
    for autorizacao in set(novos) - set(antigos):
        n = novos[autorizacao]
        eventos.append((autorizacao, n["cnpj"], n["razao_social"], n["chave_uf_municipio"],
                         None, n["bandeira"], "entrada_mercado"))
    for autorizacao in set(antigos) - set(novos):
        a = antigos[autorizacao]
        eventos.append((autorizacao, a["cnpj"], a["razao_social"], a["chave_uf_municipio"],
                         a["bandeira"], None, "saida_mercado"))
    return eventos


def gravar_glp(conn, eventos, origem_csv):
    agora = datetime.now(timezone.utc).isoformat()
    registros = [(*e, "BCU (DataBook GLP v9)", str(origem_csv), agora) for e in eventos]
    conn.executemany("""INSERT INTO movimento_bandeira_glp (
        numero_autorizacao, cnpj, razao_social, chave_uf_municipio,
        situacao_anterior, situacao_nova, grupo_distribuidor_anterior,
        grupo_distribuidor_novo, bandeirada_anterior, bandeirada_nova,
        tipo_movimento, arquivo_origem_anterior, arquivo_origem_novo, data_deteccao
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", registros)
    conn.commit()


def gravar_combustiveis(conn, eventos, origem_csv):
    agora = datetime.now(timezone.utc).isoformat()
    registros = [(*e, "BCU (DataBook Combustíveis v3)", str(origem_csv), agora) for e in eventos]
    conn.executemany("""INSERT INTO movimento_bandeira_combustiveis (
        numero_autorizacao, cnpj, razao_social, chave_uf_municipio,
        bandeira_anterior, bandeira_nova, tipo_movimento,
        arquivo_origem_anterior, arquivo_origem_novo, data_deteccao
    ) VALUES (?,?,?,?,?,?,?,?,?,?)""", registros)
    conn.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dominio", required=True, choices=["GLP", "COMBUSTIVEIS"])
    parser.add_argument("--csv", required=True)
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)

    if args.dominio == "GLP":
        antigos = carregar_glp_bcu(conn)
        novos = carregar_glp_csv(args.csv)
        eventos = comparar_glp(antigos, novos)
        gravar_glp(conn, eventos, args.csv)
        idx_tipo = 10
    else:
        antigos = carregar_combustiveis_bcu(conn)
        novos = carregar_combustiveis_csv(args.csv)
        eventos = comparar_combustiveis(antigos, novos)
        gravar_combustiveis(conn, eventos, args.csv)
        idx_tipo = 6

    print(f"Base anterior (BCU): {len(antigos)} registros")
    print(f"Base nova (CSV bruto ANP): {len(novos)} registros")
    print(f"Comparação concluída: {len(eventos)} eventos detectados.\n")

    por_tipo = {}
    for e in eventos:
        tipo = e[idx_tipo]
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    for tipo, qtd in sorted(por_tipo.items()):
        print(f"  {tipo}: {qtd}")

    conn.close()


if __name__ == "__main__":
    main()
