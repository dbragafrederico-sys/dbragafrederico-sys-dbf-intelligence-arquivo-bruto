# Georreferenciamento — Malha Rodoviária e Ferroviária Federal

Shapefiles brutos de infraestrutura de transporte (DNIT/BIT/MT), arquivados
completos aqui. Os atributos (sem geometria) são carregados no BCU
(`dbf-intelligence-bcu`, tabelas `malha_rodoviaria_federal` e
`malha_ferroviaria`) para consulta pontual em projetos de Inteligência
Territorial (Frente 4) e possível insumo futuro de índices (IVR/território).

## Status do arquivamento (15/08/2026)

| Shapefile | Fonte | URL | Status |
|---|---|---|---|
| `BaseFerro.*` | BIT/MT | gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/Base-GEO/BaseFerro.zip | ✅ arquivado (8/8 componentes) |
| `SNV_grupo1..4.*` (= `SNV_202607A`, reparticionado) | DNIT/BIT — versão 202607A | gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas | ✅ arquivado (4 grupos + `.prj`/`.cpg` comuns) |

`BaseFerro`: 4.427 registros (`PolyLine`), sistema de referência
`GCS_SIRGAS_2000`, codepage UTF-8. Campos de atributo confirmados por leitura
direta com `pyshp`: `objectid_1`, `tip_situac`, `bitola`, `sigla`,
`municipio`, `id`, `uf`, `label`, `nome`, `extensao`, `sigla_coin`,
`extensao_c`, `extensao_e`, `st_length_` — os usados na carga do BCU são
`id`, `uf`, `municipio`, `nome`, `tip_situac`, `bitola`, `sigla`, `extensao`
(ver `carregar_malha_transporte.py` em `dbf-intelligence-bcu`).

`SNV_202607A` foi entregue reparticionado em 4 grupos
(`SNV_grupo1.shp/.shx/.dbf` a `SNV_grupo4.shp/.shx/.dbf`) por limite de
tamanho de transferência — divisão por UF, sem critério geográfico além do
balanceamento de volume. A união dos 4 grupos soma **7.673 registros**
(`PolyLine`), equivalente ao arquivo original do DNIT/BIT, sem perda ou
alteração de dados (zero sobreposição de UF entre grupos, estrutura de
campos idêntica nos 4). `SNV_202607A.prj`/`.cpg` (sistema de referência e
codepage, comuns aos 4 grupos) também arquivados.

Campo de atributo mapeado na carga: o nome real no `.dbf` é `id_trecho_`
(truncado a 10 caracteres pelo formato DBF) — corrigido em
`carregar_malha_transporte.py` após bug encontrado nesta carga (o mapeamento
original assumia `id`, o que geraria `NULL` silencioso em `id_trecho_dnit`
para as 7.673 linhas; corrigido e validado com checagem estrutural de campos
antes da carga).

Os componentes `.shx`/`.sbn`/`.sbx` do arquivo original não-particionado
(`SNV_202607A`, recebidos isoladamente antes da chegada dos 4 grupos) **não
foram arquivados** — pertencem a uma estrutura de arquivo único que não
corresponde aos `.shp` efetivamente entregues (os 4 grupos), e arquivá-los
junto aos grupos criaria pares `.shp`/`.shx` inconsistentes. Cada grupo tem
seu próprio `.shx` correto, gerado junto com seu `.shp`.

## Repositórios relacionados

- `dbf-intelligence-bcu` — schema (`malha_rodoviaria_federal`,
  `malha_ferroviaria`) e script de carga (`carregar_malha_transporte.py`).
