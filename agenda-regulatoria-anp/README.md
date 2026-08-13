# Agenda Regulatória ANP — Arquivo de PDFs-fonte

Arquivo primário (PDFs) das cinco versões usadas para extrair os dados
estruturados hoje em `agenda_regulatoria_anp` (Tabela 15) e
`historico_cronograma_acao_regulatoria` (Tabela 16) do BCU
(`dbf-intelligence-bcu`). Este é só o arquivamento da fonte primária — os
dados já extraídos, estruturados e carregados em produção não estão aqui.

## Status do arquivamento (13/08/2026)

| Arquivo nesta pasta | Nome original | Status |
|---|---|---|
| `2017-2018_agenda-lancamento.pdf` | `agendaregulatoria201720181.pdf` | ✅ arquivado |
| `2020-2021_agenda-lancamento_v1-rascunho.pdf` | `agendaregulatoria20202021v1.pdf` | ✅ arquivado |
| `2020-2021_agenda-lancamento_v3.0-30-01-2020.pdf` | `agendaregulatoria20202021v3.pdf` | ✅ arquivado |
| *(pendente)* | `agenda-regulatoria-2022-2023-1.pdf` | ⏳ **não enviado ainda** — 1º relatório de acompanhamento (1º PC, jul/2022) |
| *(pendente)* | `agenda-regulatoria-2022-2023-5.pdf` | ⏳ **não enviado ainda** — 5º relatório de acompanhamento (5º PC, jul/2024, AR estendida) |

**Os dois PDFs do biênio 2022-2023 ainda não foram enviados a este
repositório.** Os dados extraídos deles já estão em produção (ver seção 3
abaixo), mas os arquivos PDF originais continuam pendentes de upload. Não
remover esses dois da biblioteca do projeto Claude.ai até que apareçam
aqui.

## 1. 2022-2023: relatórios de acompanhamento, não agenda de lançamento

`agenda-regulatoria-2022-2023-1.pdf` e `agenda-regulatoria-2022-2023-5.pdf`
**não são a agenda de lançamento do biênio 2022-2023** — são o 1º e o 5º
"Relatório Consolidado de Acompanhamento" (pontos de controle semestrais
que a ANP publica sobre a execução da agenda já lançada). Isso já causou
confusão numa sessão anterior (RS-REG-13082026), tratando esses relatórios
como se fossem a própria agenda. Não deve se repetir: quando alguém pedir
"a agenda 2022-2023", a pergunta certa é "qual ponto de controle?" — não
existe um único documento "a agenda 2022-2023" nesta série, existe uma
sequência de relatórios de acompanhamento ao longo do biênio.

## 2. 2020-2021 v3: é a agenda de lançamento, não uma atualização de 2021

`2020-2021_agenda-lancamento_v3.0-30-01-2020.pdf` traz na capa
"v.3.0 – 30/01/2020" — ou seja, é uma revisão da **agenda de lançamento**
do biênio, publicada em janeiro de 2020, e não uma atualização feita em
2021 como uma sessão anterior presumiu (o nome do arquivo, sem essa data
de capa visível, induzia a esse erro). `v1` é um rascunho/edição anterior
da mesma agenda de lançamento, sem marca de versão na capa — por isso o
sufixo `_v1-rascunho` no nome renomeado.

## 3. Isto não duplica trabalho de extração

Os dados estruturados das cinco versões — incluindo as diferenças entre
v1 e v3 (2020-2021) e entre o 1º e o 5º PC (2022-2023): troca de servidor
responsável, seções que desaparecem entre versões (ex.: "Diretrizes da
Diretoria Colegiada" presente em v1 mas ausente em v3), deslizamento de
cronograma (prazos anunciados que se movem de relatório para relatório) —
já estão carregados em produção no BCU, commit `613bbb9` do
`dbf-intelligence-bcu`, e preservados nos CSVs fonte commitados junto com
essa carga (`agenda_regulatoria_2017_2018.csv`,
`agenda_regulatoria_2020_2021.csv`, `agenda_regulatoria_2022_2023.csv`).
Este arquivamento em PDF é só da fonte primária, para auditoria e
reprocessamento futuro caso necessário — não é preciso reextrair nada
daqui para uso corrente.

## 4. Pendência aberta — link textual Tabela 15 ↔ Tabela 16 nunca funcionou

Achado desta sessão (13/08/2026), registrado aqui para não se perder:
as 79 linhas originais da Agenda 2025-2026 em `agenda_regulatoria_anp`
(carregadas em 12/08/2026) têm o campo `titulo` **sem acentuação**
(ex.: "Distribuicao e Revenda de GLP", "Transparencia de Precos na
Revenda"), enquanto `historico_cronograma_acao_regulatoria.titulo_acao`
usa texto **acentuado** ("Distribuição e Revenda de GLP", "Transparência
de Preços na Revenda"). Como o link entre as duas tabelas é só textual
(não há FK — `historico_cronograma_acao_regulatoria` nem tem coluna
`id_acao`), esse link **nunca funcionou desde a criação** das duas
tabelas — não é regressão da migração de schema desta sessão (confirmado:
o mesmo JOIN roda vazio tanto no banco atual quanto no backup
pré-migração).

**Não resolvido nesta sessão — fica como pendência para sessão futura:**
- (a) corrigir a acentuação das 79 linhas antigas de 2025-2026,
  reprocessando `agendaregulatoria20252026.pdf` (arquivo ainda não
  migrado para este repositório — permanece na biblioteca do projeto, já
  que está marcado "JÁ CARREGADO no BCU... não precisa reextração" no log
  de proveniência da sessão de extração);
- (b) formalizar o link Tabela 15 ↔ Tabela 16, seja com uma FK real
  (exigiria adicionar `id_acao` a `historico_cronograma_acao_regulatoria`
  e popular a partir de um match manual/revisado) ou com uma comparação
  normalizada (remover acentos dos dois lados na hora da consulta, sem
  alterar os dados armazenados).

## Proveniência

Ver `log_versoes_agenda_regulatoria.csv` (produzido durante a extração,
13/08/2026) para hash MD5, formato interno (OCR vs. PDF texto nativo),
contagem de páginas/ações e recomendação de status por versão — não
incluído neste repositório, mas disponível na sessão de extração original
caso necessário para auditoria.

## Repositórios relacionados

- `dbf-intelligence-bcu` — banco processado (Tabelas 15 e 16), scripts de
  carga (`carregar_agenda_regulatoria.py`,
  `carregar_historico_cronograma.py`) e schema.
