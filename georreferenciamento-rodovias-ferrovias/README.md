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
| `SNV_202607A.*` | DNIT/BIT — versão 202607A | gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas | ⏳ pendente — só `.shx` recebido até agora |

`BaseFerro`: 4.427 registros (`PolyLine`), sistema de referência
`GCS_SIRGAS_2000`, codepage UTF-8. Campos de atributo confirmados por leitura
direta com `pyshp`: `objectid_1`, `tip_situac`, `bitola`, `sigla`,
`municipio`, `id`, `uf`, `label`, `nome`, `extensao`, `sigla_coin`,
`extensao_c`, `extensao_e`, `st_length_` — os usados na carga do BCU são
`id`, `uf`, `municipio`, `nome`, `tip_situac`, `bitola`, `sigla`, `extensao`
(ver `carregar_malha_transporte.py` em `dbf-intelligence-bcu`).

`SNV_202607A` ainda não está completo nesta pasta — só recebido `.shx` até
o momento. Não remover o original da biblioteca do projeto Claude.ai até
o arquivamento completo ser confirmado aqui.

## Repositórios relacionados

- `dbf-intelligence-bcu` — schema (`malha_rodoviaria_federal`,
  `malha_ferroviaria`) e script de carga (`carregar_malha_transporte.py`).
