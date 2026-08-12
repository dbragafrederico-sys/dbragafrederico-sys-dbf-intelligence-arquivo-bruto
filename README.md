# DBF Intelligence — Arquivo Bruto e Histórico

Repositório privado de **arquivo bruto e histórico de baixa frequência de
consulta** da DBF Intelligence. Criado em 12/08/2026 como extensão do
padrão de persistência já validado com o **Banco de Conhecimento Único
(BCU)** — em vez de manter esses arquivos ocupando espaço permanente na
biblioteca do projeto no Claude.ai, eles vivem aqui e são recuperados sob
demanda quando um reprocessamento ou consulta pontual exige o dado bruto.

**Repositório irmão:**
`https://github.com/dbragafrederico-sys/dbf-intelligence-bcu` (banco
processado, índices calculados — fonte de verdade operacional)

**Status (12/08/2026):** migração da Fase 1 **concluída**. Repositório
criado e estrutura de pastas montada via Claude Code, a partir do briefing
técnico `DBF_Briefing_Tecnico_Migracao_Arquivo_Bruto_12-08-2026.md`, e
todos os arquivos enviados manualmente por Daniel via anexos no chat (o
ambiente de execução do Claude Code não acessa a biblioteca do projeto no
Claude.ai diretamente):

- ✅ `regulatorio-referencia/` — 3/3 arquivos enviados
- ✅ `dados-fiscais-brutos/` — 2/2 arquivos enviados
- ✅ `historico-requalificacao/` — 20/20 arquivos enviados (2007–2026, inclui `2024requalificacao1.pdf`)
- ✅ `historico-troca-botijao/` — 20/20 arquivos enviados (2007–2026)

Total: 45 arquivos migrados (a série histórica veio com 20 anos por pasta,
não 19 como estimado no briefing original).

## Por que este repositório existe

A biblioteca do projeto DBF Intelligence no Claude.ai atingiu 175MB — bem
acima do limite prático de referência (~30MB) — majoritariamente por
conta de dados brutos e séries históricas já processadas em outro lugar
(RA-REG-001, DataBooks) ou de consulta esporádica. Este repositório separa
esse material do núcleo ativo do projeto, sem descartar nada.

## Regra operacional que rege este repositório

Sempre que a biblioteca do projeto Claude.ai ultrapassar **50% da
capacidade**, repetir o processo de triagem e migração para cá, nesta
ordem de prioridade:

1. Dados brutos já processados em outro lugar
2. Séries históricas de baixo uso
3. PDFs regulatórios de referência pontual
4. Só por último, se necessário: DataBooks ativos e núcleo vivo do projeto

DataBooks ativos e documentos de uso corrente (relatórios de sessão, notas
metodológicas, manuais) **não** migram para cá — continuam na biblioteca
do Claude.ai, onde o acesso precisa ser imediato a cada sessão.

## Estrutura do repositório (Fase 1 — planejada)

```
dbragafrederico-sys-dbf-intelligence-arquivo-bruto/   (GitHub, privado)
├── dados-fiscais-brutos/
│   ├── dadosfisc19982018_1.xlsx              # 28,1MB — fiscalização ANP 1998-2018
│   └── dadosfiscapartir2019_1.xlsx            # 15,5MB — fiscalização ANP a partir de 2019
├── historico-requalificacao/
│   └── [2007 a 2026]requalificacao.pdf        # 19 arquivos, 15MB — série histórica ANP
├── historico-troca-botijao/
│   └── [2007 a 2026]programanacionaldestroca.pdf  # 19 arquivos, 13MB — Programa Nacional de Troca de Botijão
├── regulatorio-referencia/
│   ├── Zoneamento_Uso_e_Ocupacao_do_Solo__Leis_org.pdf    # 15,5MB — caso Rodrigogaz/Mogi das Cruzes
│   ├── NTEPEDPGDEA202201_GLP_e_Outros_Usos.pdf            # 12,0MB — nota técnica ANP
│   └── 60783A_Geografia_Redes_Distribuicao_Gas_Canalizado_Brasil.pdf  # 5,5MB — referência setorial
└── README.md
```

**Total a migrar nesta fase: 42 arquivos, ~103MB.** As pastas acima já
existem no repositório; os arquivos em si ainda estão pendentes de envio.

## Proveniência dos dados

- **Dados fiscais brutos:** extrações originais do Painel Dinâmico da
  Fiscalização ANP (1998–2026, ~637 mil registros). Já sintetizados e
  analisados no relatório `RA-REG-001_2026_Fiscalizacao_ANP`. Os arquivos
  brutos aqui servem apenas para reprocessamento pontual — não para
  consulta corrente.
- **Histórico de requalificação:** documentos anuais ANP sobre
  requalificação de botijões de GLP, 2007–2026. Base para a análise
  "botijão vencido/requalificação" (iniciada, ainda não concluída).
- **Histórico do Programa Nacional de Troca de Botijão:** documentos
  anuais ANP, 2007–2026.
- **PDFs regulatórios de referência única:** documentos consultados em
  projetos específicos — o Zoneamento é do caso Rodrigogaz/Mogi das
  Cruzes; a nota técnica NT EPE e o estudo de geografia de redes são
  referência setorial ampla, não vinculados a um projeto único.

## Como recuperar um arquivo

Não é necessário clonar o repositório inteiro para pegar um único
documento. Exemplo de recuperação pontual (uma vez que os arquivos
estiverem no repositório):

```
https://raw.githubusercontent.com/dbragafrederico-sys/dbragafrederico-sys-dbf-intelligence-arquivo-bruto/main/historico-requalificacao/2015requalificacao.pdf
```

Para acesso completo (reprocessamento, auditoria, nova análise sobre a
série):

```
git clone https://x-access-token:<TOKEN>@github.com/dbragafrederico-sys/dbragafrederico-sys-dbf-intelligence-arquivo-bruto.git
```

**Sobre o token:** mesmo padrão do BCU — token de acesso pessoal
fine-grained, gerado por sessão, nunca salvo em memória do Claude ou em
configuração persistente. O repositório é e deve continuar **privado**.

## Pendências em aberto

1. ~~Enviar os arquivos da Fase 1~~ — concluído em 12/08/2026 (45 arquivos).
2. Fase 2 (avaliar depois): decidir se os DataBooks ativos (GLP v10,
   Combustíveis v4, MAE v2 — ~24MB) migram para cá com um fluxo de
   clone→query como o do BCU, ou permanecem na biblioteca do Claude.ai.
   Não recomendado migrar agora — só se a biblioteca voltar a se
   aproximar do limite após esta Fase 1.
3. CSVs de vendas/entregas ANP (GLP_Vendas_Atual, GLP_Entregas_Historico
   etc., ~9,2MB) — candidatos de baixo custo-benefício para uma eventual
   Fase 2.
4. Confirmar remoção dos 42 arquivos correspondentes na biblioteca do
   projeto Claude.ai, após validar que a recuperação a partir deste
   repositório está funcionando.
