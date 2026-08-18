# Contexto de arquivamento — detectar_movimentacao_raw_anp.py

**Arquivado em:** 18/08/2026, por decisão de Daniel Braga Frederico.

## O que é este arquivo

Protótipo v0.1 de detecção de movimentação a partir de extração bruta da
ANP (233 linhas). Encontrado na biblioteca do projeto Claude.ai durante
auditoria de 18/08/2026 — **nunca foi commitado no repositório GitHub
dbf-intelligence-bcu**, ou seja, nunca esteve conectado ao pipeline real
de produção.

## Por que tem valor histórico

O docstring interno deste protótipo já documenta o bug que foi
redescoberto e corrigido independentemente em 18/08/2026: comparar
`grupo_distribuidor` (rollup societário) em vez de `vinculacao_a` (nível
marca) gera falsos positivos maciços de "mudança de bandeira"
(documentado aqui como 46.073 eventos espúrios; a investigação de
18/08/2026, partindo de uma base diferente, encontrou 32.129/32.713
falsos positivos pelo mesmo motivo).

Ou seja: alguém, em algum momento anterior a 18/08/2026, já tinha
identificado esse problema e esboçado uma solução — mas o conhecimento
não chegou a ser conectado ao código de produção, e por isso não foi
encontrado durante o trabalho desta sessão até uma auditoria de
biblioteca revelar o arquivo.

## Por que NÃO foi usado como solução

A solução implementada em produção (18/08/2026, dentro de
`detectar_movimentacao.py`, commit a confirmar) é mais completa que este
protótipo:
- Trata separação por domínio (GLP × Combustíveis Líquidos) — bug real
  encontrado ao carregar pares de grupo econômico GLP que vazaram para
  a comparação de Combustíveis (par VIBRA→VIBRA ENERGIA causou 6.801
  eventos espúrios até a correção).
- Reaproveita as funções já testadas do `detectar_movimentacao.py`
  existente, em vez de duplicar toda a lógica de leitura/anomalias num
  script separado.

Este protótipo não tem a correção de domínio nem passou pelos testes de
integridade (`PRAGMA integrity_check`, `foreign_key_check`) que a
implementação de produção passou.

## Lição de processo registrada

Todo conhecimento técnico gerado (mesmo em protótipo/rascunho) deveria
ser commitado no repositório de produção, não deixado só na biblioteca
do Claude.ai — os dois ambientes são isolados, e um protótipo correto
"invisível" para o pipeline real não ajuda ninguém no momento em que o
mesmo problema aparece de novo.
