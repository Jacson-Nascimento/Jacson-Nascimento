# Paper 2 — ano de 2025 completo

## Título provisório

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

### Título em inglês

**Temporal Persistence of Structural Supplier Dependency in Municipal Public Procurement: Annual Evidence, Networks, and Stress Tests**

## Papel do Paper 2

Este artigo não é uma simples atualização numérica do Paper 1. Ele utiliza o mesmo framework previamente definido para responder a uma pergunta diferente: **a exposição estrutural observada nas carteiras públicas municipais é estável ao longo do ano, resiste à expansão da rede e permanece relevante depois da incorporação de publicações tardias?**

A contribuição central é longitudinal e de validação externa no tempo.

## Janela e regra temporal

- período econômico: instrumentos assinados de 01/01/2025 a 31/12/2025;
- coleta operacional: por data de publicação no PNCP;
- meses de publicação: janeiro a dezembro de 2025;
- após dezembro: captura tardia em 2026 de instrumentos assinados em 2025;
- somente após essa captura a base anual será congelada.

O artigo deve distinguir permanentemente:

1. mês de publicação;
2. data de assinatura;
3. acumulado de publicações até o mês `M`;
4. base anual congelada após a janela tardia.

## Pergunta de pesquisa

Quão persistentes são, ao longo de um ano completo de contratação pública municipal, os rankings de exposição estrutural, a discordância entre concentração local e exposição global e a vulnerabilidade a choques de fornecedores centrais, e em que medida essas conclusões são sensíveis à expansão mensal da rede e às publicações tardias?

## Hipóteses descritivas / expectativas pré-definidas

O Paper 2 não deve formular hipóteses causais. As expectativas empíricas são:

- H1: os rankings de exposição Strength apresentam elevada persistência entre meses consecutivos;
- H2: a discordância entre HHI e exposição estrutural não desaparece com a expansão da rede;
- H3: ataques direcionados por Strength permanecem mais severos que contrafactuais aleatórios ao longo das janelas;
- H4: parte da variação das estatísticas agregadas decorre da entrada de novos compradores elegíveis;
- H5: os resultados principais permanecem qualitativamente estáveis após a captura tardia de 2026;
- H6: robustezes leave-one-buyer-out e stress tests alternativos não eliminam a conclusão de que concentração local e exposição estrutural são dimensões distintas.

## Contribuição distinta em relação ao Paper 1

O Paper 1 apresenta e testa inicialmente o framework com janeiro-junho.

O Paper 2 examina:

- trajetória mensal janeiro-dezembro;
- estabilidade de rankings e quadrantes;
- entrada e saída de compradores elegíveis;
- efeito de composição das coortes;
- evolução da rede global de fornecedores;
- estabilidade dos stress tests;
- estabilidade dos modelos associativos;
- sensibilidade à captura tardia;
- comparação da base dezembro-publicação versus base anual congelada.

O Paper 2 deve citar o Paper 1 como origem da especificação e evitar repetir longas descrições teóricas ou metodológicas.

## 1. Dados

A unidade do comprador permanece o CNPJ institucional do órgão municipal do Poder Executivo.

A chave de instrumento permanece `numeroControlePNCP`.

`numeroControlePNCPCompra` nunca é utilizado para deduplicar instrumentos.

A base pública identificada permanece restrita a fornecedores PJ. PF e PE aparecem apenas em diagnósticos agregados.

## 2. Métricas congeladas

A metodologia principal não muda durante a coleta mensal:

- HHI monetário e normalizado;
- CountHHI e normalizado;
- CR1, CR4 e número efetivo de fornecedores;
- Degree global;
- Strength global como ranking principal;
- exposição do comprador ponderada pela carteira;
- quadrante concentração-exposição;
- stress tests top 1%, 5% e 10%;
- 1.000 contrafactuais aleatórios na especificação principal;
- critérios de elegibilidade 3/5, 5/10, 5/20 e 10/20;
- modelos associativos SICONFI com especificação pré-fixada.

## 3. Robustezes adicionais fixadas antes do fechamento anual

As robustezes propostas em agosto de 2026 devem ser tratadas como pré-especificadas para o Paper 2:

### 3.1 Leave-one-buyer-out

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Recalcular exposição e retenção de quartis.

### 3.2 Discordância alternativa

Além do quadrante histórico, reportar:

- gap entre percentis de exposição e HHI;
- resíduo da exposição após HHI normalizado;
- estabilidade dessas classificações ao longo do tempo.

### 3.3 Stress tests alternativos

Além do nulo uniforme já congelado:

- randomização com probabilidade proporcional ao Strength;
- randomização com número variável de fornecedores até atingir massa sistêmica de Strength próxima à do ataque direcionado.

### 3.4 Robustez econométrica municipal

- WLS no comprador com peso `1/N_m`;
- modelo agregado ao município;
- CR1 e CR4 como outcomes alternativos;
- interpretação do número de fornecedores como controle estrutural, não determinante causal.

## 4. Painel longitudinal principal

Para cada transição `M-1 -> M`, reportar:

- compradores elegíveis em cada mês acumulado;
- compradores comuns;
- entrantes;
- saídas;
- rho de Spearman dos rankings Strength e Degree;
- retenção no quartil superior;
- retenção da discordância HHI-exposição;
- taxa de estabilidade do quadrante completo;
- mudança do HHI nos compradores comuns;
- perfil dos entrantes.

Evitar comparar apenas medianas transversais, pois elas misturam mudança individual e composição.

## 5. Evolução da rede

Para cada mês acumulado, reportar:

- compradores;
- fornecedores;
- relações comprador-fornecedor;
- instrumentos;
- distribuição de Degree;
- distribuição de Strength;
- concentração do Strength sistêmico nos maiores fornecedores;
- correlação HHI-exposição;
- percentual no quadrante de discordância.

O objetivo é verificar se a expansão da rede altera materialmente os sinais detectados no primeiro semestre.

## 6. Estabilidade dos stress tests

Construir uma tabela mensal com:

- top 1%, 5%, 10%;
- perda severa direcionada em 25%, 50% e 75%;
- contrafactual aleatório uniforme;
- randomização ponderada por Strength;
- contrafactual de massa sistêmica aproximada;
- diferença absoluta e razão entre cenários.

O argumento substantivo deve ser baseado na persistência do padrão, não em uma única janela.

## 7. Publicações tardias como teste de sensibilidade

Depois de dezembro de 2025, executar janela tardia em 2026 e identificar instrumentos:

- assinados em 2025;
- publicados em 2026;
- ainda não presentes na base congelada de dezembro-publicação.

Comparar antes e depois da captura tardia:

- número de instrumentos;
- compradores elegíveis;
- fornecedores globais;
- HHI, CR1, CR4, Neff;
- exposição Strength e Degree;
- ranking dos compradores;
- quadrante de discordância;
- stress tests;
- coeficientes associativos.

A captura tardia é parte da definição do período anual, não correção ad hoc.

## 8. Integração SICONFI

A integração permanece incremental. Para cada mês, coletar apenas municípios sem DCA bem-sucedida no cache anterior.

Cobertura de despesa empenhada deve permanecer pelo menos 95% antes dos modelos.

No Paper 2, os modelos servem para avaliar **estabilidade associativa** dos sinais ao longo das janelas, não para explicar causalmente a concentração.

Priorizar:

- persistência de sinal;
- ordem de grandeza;
- intervalos de confiança;
- robustez entre OLS e fractional logit;
- robustez com peso municipal e agregação municipal.

Não priorizar significância isolada em um mês.

## 9. Estratégia de comparação Paper 1 versus Paper 2

O Paper 2 deve incluir uma seção curta intitulada “Validação anual do framework previamente definido”. Nela, comparar a base anual com os resultados do primeiro semestre sem reproduzir integralmente o Paper 1.

A comparação deve responder:

- quais sinais permaneceram;
- quais se enfraqueceram;
- quais se fortaleceram;
- quais dependiam de composição da amostra;
- quais foram sensíveis à captura tardia.

## 10. Estrutura recomendada

1. Introdução: por que persistência temporal importa para screening de dependência.
2. Framework previamente definido e desenho de validação anual.
3. Dados, calendário de publicação e captura tardia.
4. Evolução mensal da rede.
5. Persistência de concentração e exposição.
6. Efeito de composição.
7. Estabilidade dos stress tests.
8. Robustezes LOO, discordância alternativa e nulos alternativos.
9. Estabilidade das associações fiscais.
10. Efeito da captura tardia.
11. Discussão e implicações para monitoramento contínuo.
12. Limitações e conclusão.

## 11. Critério de prontidão

O Paper 2 somente poderá ser tratado como empiricamente fechado quando:

- janeiro-dezembro estiverem consolidados;
- duplicidades de `id_contrato` forem zero;
- janelas de publicação forem validadas;
- hashes estiverem registrados;
- captura tardia de 2026 estiver concluída;
- métricas anuais forem recalculadas;
- diagnósticos longitudinais estiverem completos;
- SICONFI anual estiver integrado;
- modelos e robustezes estiverem executados;
- documentação técnica estiver versionada no GitHub e espelhada na pasta específica do Google Drive.

## 12. Regra editorial contra publicação redundante

O Paper 2 deve apresentar pergunta, contribuição, tabelas e discussão próprias. O Paper 1 será citado sempre que a definição do framework puder ser remetida ao estudo anterior. Texto idêntico deve ser limitado a definições matemáticas indispensáveis e devidamente referenciado.
