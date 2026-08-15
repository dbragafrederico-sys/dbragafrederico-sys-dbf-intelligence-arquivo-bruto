# Mapas Multimodais por UF

Mapas de infraestrutura de transporte multimodal (rodovias, ferrovias,
portos, aeroportos etc.), um PDF por UF mais o mapa nacional consolidado.
Consulta esporádica, sem interpretação em lote — leitura só sob demanda
de projeto específico (Frente 4, Inteligência Territorial).

## Status do arquivamento (15/08/2026)

| Arquivos | Fonte | URL | Status |
|---|---|---|---|
| `se.pdf`, `brasil.pdf` | DNIT GEO | gov.br/dnit/pt-br/assuntos/planejamento-e-pesquisa/dnit-geo/mapas-multimodais | ✅ arquivados |
| `rr.pdf`, `ap.pdf`, `ce.pdf`, `rn.pdf`, `al.pdf`, `pe.pdf`, `pb.pdf`, `ma.pdf`, `pa.pdf`, `ac.pdf`, `am.pdf`, `pi.pdf`, `to.pdf`, `ro.pdf`, `mt.pdf`, `df.pdf`, `go.pdf`, `es.pdf`, `mg.pdf`, `rj.pdf`, `ms.pdf`, `ba.pdf`, `pr.pdf`, `rs.pdf`, `sc.pdf`, `sp.pdf` | BIT/MT | gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas | ✅ arquivados |

**28 de 28 arquivados — arquivamento completo.** Todos os 26 estados + DF
(via BIT/MT) mais o mapa nacional consolidado e SE (via DNIT GEO). Todos os
arquivos verificados individualmente como PDFs genuínos (`%PDF-1.6`) e sem
duplicatas entre si antes do commit. Os originais podem agora ser removidos
da biblioteca do projeto Claude.ai — arquivamento aqui confirmado como fonte
de registro.

## Repositórios relacionados

- `dbf-intelligence-bcu` — schema (`malha_rodoviaria_federal`,
  `malha_ferroviaria`) e script de carga (`carregar_malha_transporte.py`).
