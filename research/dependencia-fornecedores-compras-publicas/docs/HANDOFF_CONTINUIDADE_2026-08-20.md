# HANDOFF DE CONTINUIDADE — Dependência Estrutural de Fornecedores nas Compras Públicas

Atualizado em 2026-08-20.

## 1. Objetivo do projeto

Artigo quantitativo provisoriamente intitulado:

**Dependência Estrutural de Fornecedores nas Compras Públicas: Concentração da Carteira, Exposição em Rede e Vulnerabilidade a Choques Coletivos**

Pergunta central: em que medida compradores públicos municipais observados no PNCP apresentam concentração financeira de sua carteira de fornecedores, recorrência contratual e exposição estrutural a fornecedores centrais da rede, e quanto essas dimensões divergem entre si?

Não usar linguagem causal salvo se houver desenho específico. As regressões atuais são associativas.

## 2. Repositório e organização

Repositório: `Jacson-Nascimento/Jacson-Nascimento`

Diretório do artigo:
`research/dependencia-fornecedores-compras-publicas`

Estrutura principal:
- `data/raw/`
- `data/processed/pncp_mensal/`
- `scripts/`
- `results/`
- `docs/`
- `paper/`

Google Drive do artigo:
`ARTIGO - Dependencia de Fornecedores e Compras Publicas`

Subpastas já existentes:
- `01_Dados`
- `02_Scripts`
- `03_Documentacao_Tecnica`
- `04_Resultados`
- `05_Artigo`
- `06_Referencias`

Regra permanente: bases integrais/privadas podem ficar no Drive; GitHub público recebe somente dados minimizados. Fornecedor pessoa física não deve ter CPF/nome republicado no GitHub. Base pública principal = fornecedores PJ.

## 3. Recorte temporal

Período econômico principal: **instrumentos assinados em 2025**, de 01/01/2025 a 31/12/2025.

A coleta do PNCP é feita por **data de publicação**, mês a mês. Para a análise econômica, prevalece `ano_assinatura = 2025`.

Motivo: há cauda longa de publicação. Portanto, após fechar dezembro/2025, ainda deve existir uma **janela de captura tardia em 2026** para recuperar instrumentos assinados em 2025 e publicados depois.

Não tratar resultados acumulados Jan–M como resultado anual definitivo.

## 4. Fontes validadas

### PNCP
Endpoint principal:
`https://pncp.gov.br/api/consulta/v1/contratos`

Campos-chave confirmados:
- `numeroControlePNCP` = chave do instrumento
- `numeroControlePNCPCompra` = vínculo com contratação
- `orgaoEntidade.cnpj` = comprador institucional principal
- `unidadeOrgao.codigoIbge`
- `niFornecedor`
- `tipoPessoa`
- `valorInicial`
- `valorGlobal`
- `dataAssinatura`
- `dataPublicacaoPncp`
- `tipoContrato.nome`
- `categoriaProcesso.nome`

Decisão crítica: **não deduplicar por `numeroControlePNCPCompra`**. Uma mesma contratação pode gerar vários instrumentos e fornecedores. A chave do instrumento é `numeroControlePNCP`.

Comprador principal = CNPJ institucional do órgão/entidade, não simplesmente município da unidade executora. Compras compartilhadas/origem externa ficam identificadas separadamente.

### SICONFI/DCA
Validado para 2025, com boa cobertura para a coorte PNCP. Variáveis usadas:
- despesa empenhada
- população
- controles fiscais derivados

Cobertura alcançou aproximadamente 99% nas coortes acumuladas até junho.

### IBGE
Usado para população/localidade e universo territorial. Cuidado: endpoint de localidades retorna 5.571 registros; para o universo municipal estrito do estudo devem ser excluídos Distrito Federal e Distrito Estadual de Fernando de Noronha, resultando em **5.569 municípios**.

## 5. Definição das métricas principais

Unidade principal atual: **comprador institucional (CNPJ) × ano** para concentração da carteira.

Para comprador `b`, fornecedor `s` e ano `t`:

`V_bst = soma dos valores dos instrumentos`

`q_bst = V_bst / soma_s V_bst`

### Concentração monetária
`PortfolioHHI = soma_s q_bst^2`

Número efetivo:
`N_eff = 1 / PortfolioHHI`

CR1 e CR4 também são calculados.

### Concentração por frequência
`CountHHI` usa a participação do fornecedor no número de instrumentos, não no valor.

### HHI normalizado
Usado obrigatoriamente como complemento porque o HHI bruto depende mecanicamente do número de fornecedores:

`HHI_norm = (HHI - 1/N) / (1 - 1/N)` para N > 1.

### Rede global
Rede bipartida comprador–fornecedor com peso por valor.

- `Degree`: número de compradores ligados ao fornecedor.
- `Strength`: valor total ligado ao fornecedor.
- `Reach`: compradores alcançados / compradores da rede.

Especificação principal de vulnerabilidade: **ranking por Strength global**.

`Degree` é complementar/robustez.

### Exposição estrutural
Exposição do comprador aos percentis de centralidade/Strength de seus fornecedores, ponderada por participação monetária.

### Exposição estrutural oculta
Compradores com HHI abaixo do quartil superior e exposição Strength acima do quartil superior. Usar como sinal de screening, não como rótulo permanente.

## 6. Simulações de choque

Remoção de fornecedores em 1%, 5% e 10% da rede.

Comparar:
- remoção aleatória, 1.000 simulações, semente fixa `20260818`;
- remoção direcionada por Strength global (principal);
- Degree global (complementar).

Para conjunto removido `R`:
`Loss_b(R) = soma_{s em R} q_bs`

Severidade principal: comprador perde pelo menos 50% da carteira observada.

Achado recorrente: choques direcionados ficam muito acima das remoções aleatórias. O efeito é **coletivo**, não dominado por um único superfornecedor.

## 7. Critérios de elegibilidade e robustez

Principal para diagnóstico: `>= 3 fornecedores` e `>= 5 instrumentos`.

Robustez:
- 5/10
- 5/20
- 10/20

A divergência valor–frequência e a exposição oculta permanecem nos cortes mais exigentes.

## 8. Robustezes já concluídas

- `valorInicial` vs `valorGlobal`: praticamente equivalentes na enorme maioria dos instrumentos; `valorInicial` permanece principal.
- lags negativos: impacto desprezível; manter na principal e excluir em sensibilidade.
- contratos vs empenhos: empenhos são materiais em contagem, mas pequenos em valor; exclusão quase não altera HHI/Strength.
- colapso conservador `compra × comprador × fornecedor`: conclusões permanecem.
- compras compartilhadas/origem externa: Strength mostrou maior robustez que Degree.
- ranking global vs ranking restrito: usar **global** como principal.
- fractional logit para HHI normalizado: confirma os sinais centrais do OLS.
- erros-padrão agrupados por município: especificação principal.
- efeitos de macrorregião preferíveis a UF em coortes menores.

## 9. Modelos associativos atuais

Respostas principais:
- HHI monetário normalizado
- gap valor–frequência
- exposição Strength

Controles principais:
- `log_populacao`
- `log_despesa_pc`
- `log_n_fornecedores`
- `log_instr_por_forn`
- efeitos de macrorregião

Inferência:
- OLS com erros agrupados por município
- fractional logit para HHI normalizado

Resultados que se mantiveram até janeiro–junho:
- população → HHI normalizado: positiva e significativa em 5/5 janelas;
- nº de fornecedores → HHI normalizado: negativa e significativa em 5/5;
- despesa per capita → HHI: não robusta;
- recorrência → HHI: frágil, 1/5 no OLS e 0/5 no fractional;
- recorrência → exposição Strength: positiva e significativa em 4/4.

Interpretação organizadora:
**diversificação reduz concentração local, mas não implica menor exposição estrutural a fornecedores globalmente centrais.**

## 10. Estado empírico validado até julho/2025

A PR #51 (julho) foi concluída e incorporada ao `main`.

Acumulado Jan–Jul:
- registros PJ acumulados: **128.444**
- instrumentos únicos: **128.444**
- instrumentos assinados em 2025: **120.609**
- compradores com métricas: **2.517**
- compradores elegíveis 3/5: **1.500**
- fornecedores na rede global: **24.160**
- HHI mediano: **0,234633**
- HHI normalizado mediano: **0,154575**
- CountHHI mediano: **0,076923**
- número efetivo mediano: **4,262**
- CR1 mediano: **37,65%**
- CR4 mediano: **80,21%**
- `PortfolioHHI > CountHHI`: **98,0%**
- exposição estrutural oculta: **14,13%** (212 compradores)
- Spearman HHI_norm × exposição Strength: **rho ≈ 0,380**

Choque Strength global, perda >=50%:
- remove 1%: direcionado **9,0%** dos compradores vs aleatório **0,31%** em média;
- remove 5%: direcionado **33,33%** vs aleatório **1,75%**;
- remove 10%: direcionado **47,73%** vs aleatório **3,96%**.

## 11. Diagnósticos longitudinais já estabelecidos

As coortes elegíveis têm permanência muito alta ao ampliar a janela mensal.

Exposição Strength apresenta alta estabilidade de ranking. Exemplos já observados:
- jan–fev → jan–mar: rho ≈ 0,921;
- mar → abr: rho ≈ 0,932;
- abr → mai: rho ≈ 0,938;
- mai → jun: rho ≈ 0,957.

Retenção do quartil superior e do quadrante de exposição oculta também é alta.

Efeito de composição: novos elegíveis tendem a entrar mais concentrados que incumbentes. Dentro dos compradores comuns, o HHI tende a cair à medida que entram novos fornecedores.

Decomposição de HHI já mostrou que a queda decorre principalmente da **entrada de novos fornecedores**, e não de mera reponderação dos antigos.

## 12. Cobertura/presença territorial — cuidado de linguagem

Diagnóstico preliminar até junho:
- universo municipal estrito: **5.569**;
- municípios observados pelo menos uma vez: **1.031** (~18,51%);
- observados em pelo menos metade dos 6 meses: **708**;
- observados em todos os 6 meses: **300**.

NÃO chamar isso de completude ou taxa de reporte. É **presença/continuidade observacional**. Município sem publicação em um mês pode simplesmente não ter instrumento naquele período.

A heterogeneidade por UF é elevada. Portanto, enquanto a janela anual + tardia não estiver concluída, evitar afirmar representatividade nacional dos municípios. Preferir: “compradores municipais observados no PNCP”.

Pendência: PR #54 de diagnóstico territorial precisa de validação final do mapeamento UF/região antes do merge.

## 13. Rotina genérica para agosto–dezembro

PR atual: **#60 — Cria rotina genérica PNCP para agosto-dezembro de 2025**

Branch: `research/pncp-restante-2025-rotina`

Configuração:
`config/pncp_mes_alvo_2025.txt`

Workflow genérico criado para usar o mesmo pipeline de agosto a dezembro:
1. lê mês-alvo 08..12;
2. cria partições de até 4 dias: 1–4, 5–8, 9–12, 13–16, 17–20, 21–24, 25–28, 29–fim;
3. tenta cada partição até 2 vezes;
4. grava imediatamente base PJ e resumos/checkpoints;
5. consolida o mês via `scripts/consolidar_mes_pncp_2025.py --month M`;
6. recalcula acumulado via `scripts/analisar_acumulado_2025_global.py --month M`;
7. executa diagnóstico longitudinal genérico mês anterior → mês atual;
8. gera artefato do Actions.

Runbook:
`docs/RUNBOOK_PNCP_AGO_DEZ_2025.md`

Estado da primeira execução (agosto):
- 01–04/08: concluído, 1.833 PJ;
- 05–08/08: concluído, 3.581 PJ;
- 09–12/08: concluído, 2.066 PJ;
- 13–16/08: concluído, 3.245 PJ;
- 17–20/08: **falhou após duas tentativas por indisponibilidade do endpoint PNCP**;
- consolidação/análise de agosto não rodaram nesse run.

Importante: os quatro primeiros checkpoints foram commitados na branch e NÃO devem ser recoletados. Na retomada, o workflow deve pular automaticamente os blocos já existentes e reiniciar em 17–20/08.

Run com falha: `32261662235`, job `96096119464`.

## 14. Scripts centrais que NÃO devem ser reinventados

- `scripts/coletar_pncp_periodo.py`
- `scripts/consolidar_mes_pncp_2025.py`
- `scripts/analisar_acumulado_2025_global.py`
- `scripts/diagnosticos_longitudinais_generico.py`
- `scripts/modelos_associativos_pncp_siconfi_generico.py`

Antes de criar script novo, procurar se um desses já cobre o caso.

## 15. Próximas ações na ordem correta

1. Retomar PR #60 e reexecutar a coleta de agosto a partir de 17–20/08, preservando 01–16/08.
2. Ao fechar agosto:
   - validar zero duplicidades;
   - validar janela de publicação;
   - conferir hash mensal;
   - ler `results/carteira_acumulada_2025_08_global/resumo.json`;
   - executar longitudinal julho→agosto;
   - rodar SICONFI incremental de agosto;
   - rodar modelos associativos genéricos `--month 8 --compare-month 7`.
3. Trocar config 08→09 e repetir exatamente o mesmo pipeline.
4. Repetir para 10, 11 e 12, sem mudar metodologia no meio da série.
5. Após dezembro, executar janela de captura tardia em 2026 para instrumentos assinados em 2025.
6. Só então congelar a base anual definitiva e produzir tabelas/gráficos finais do artigo.
7. Atualizar estrutura do artigo, documentação e pacote de replicação/Zenodo.

## 16. Regras de interpretação que devem ser preservadas

- Não chamar concentração da carteira de “concentração de mercado”.
- Não interpretar HHI isoladamente como fraude/favorecimento.
- Não tratar associação econométrica como causalidade.
- Não usar Degree como especificação principal do choque; principal = Strength global.
- Não republicar CPF/nome de pessoa física no GitHub.
- Não deduplicar por `numeroControlePNCPCompra`.
- Não chamar ausência de município no PNCP em um mês de falha de reporte.
- Não generalizar resultados parciais Jan–M para o ano completo.

## 17. PROMPT/SCRIPT PARA COLAR EM UM NOVO DIÁLOGO

Copie o bloco abaixo em um novo chat:

---

**CONTINUE O PROJETO “DEPENDÊNCIA ESTRUTURAL DE FORNECEDORES NAS COMPRAS PÚBLICAS”.**

Leia primeiro o arquivo do GitHub:
`research/dependencia-fornecedores-compras-publicas/docs/HANDOFF_CONTINUIDADE_2026-08-20.md`

Repositório: `Jacson-Nascimento/Jacson-Nascimento`.

Não reinvente a metodologia nem os scripts já validados. Preserve as decisões registradas no handoff.

Estado de retomada:
- Jan–Jul/2025 já consolidado no `main`;
- PR #60 é a rotina genérica para ago–dez/2025;
- agosto já possui checkpoints 01–04, 05–08, 09–12 e 13–16/08 commitados;
- o bloco 17–20/08 falhou por indisponibilidade do PNCP após duas tentativas;
- o próximo passo é retomar PR #60, reexecutar a partir de 17–20/08 sem recoletar os blocos existentes, concluir agosto, consolidar, recalcular a rede global, executar diagnóstico longitudinal Jul→Ago, SICONFI incremental e modelos associativos genéricos;
- depois avançar sequencialmente 09→10→11→12 usando a mesma rotina e sem mudar a especificação metodológica;
- após dezembro, executar captura tardia em 2026 para contratos assinados em 2025.

Sempre salvar scripts, resultados e documentação no GitHub e manter a documentação técnica/apoio na pasta específica do Google Drive do artigo.

Antes de responder com números novos, valide os outputs versionados e não invente resultados se um workflow ainda estiver em execução ou tiver falhado.

---
