# HANDOFF - Continuidade do projeto ciclos eleitorais e bancos

Data: 21/08/2026

## Fonte de verdade desta etapa

Este arquivo resume o estado atual da reconstrução da dissertação e deve ser consultado antes de continuar a análise.

## Repositório

`Jacson-Nascimento/Jacson-Nascimento`

Branch de trabalho:

`research/ciclos-eleitorais-bancos-reprodutibilidade`

Diretório:

`research/ciclos-eleitorais-bancos/`

PR de trabalho:

`#63 - Pesquisa: reconstrução reprodutível da dissertação sobre ciclos eleitorais e bancos`

## Objetivo

Transformar a dissertação de mestrado sobre eleições e desempenho bancário em uma linha de pesquisa reprodutível e definir, a partir dos resultados reestimados, o artigo científico derivado mais defensável.

## Estado confirmado da base

1. A versão textual final da dissertação é a versão de 21/09/2024.
2. As bases `dataset_290624_11.csv`, `_12.csv` e `_13.csv` possuem 3.072 linhas, 32 bancos e 96 trimestres, sem duplicidades banco-data e sem valores ausentes.
3. V11 -> V12 altera somente `taxa_selic_`.
4. A Selic de V12/V13 foi reconciliada com `TB_selic_4390_acum_mes_trim.xlsx`: taxa trimestral composta a partir da série mensal Bacen 4390.
5. V12 -> V13 altera somente `Taxa_IPCA`, convertendo percentual para proporção decimal.
6. A V13, SHA-256 `058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f`, é a base arquivística que reproduz as tabelas finais da dissertação.
7. O script estático arquivado aponta para V11, mas os coeficientes finais publicados, especialmente a escala do IPCA, identificam inequivocamente V13 como a base efetivamente usada nas tabelas finais.

## Reconciliação das tabelas fechada

A reprodução independente por transformação within e covariância HC1 clusterizada por banco reproduz os Apêndices D, E, F, G, J e K até o arredondamento impresso.

Achados:

- Apêndice D: ROA estático 2000-2023, V13.
- Apêndice E: ROE estático 2000-2023, V13.
- Apêndice F: ROA dinâmico 2000-2023, V13.
- Apêndice G: ROE dinâmico 2000-2023, V13.
- Apêndice H: rotulado ROA estático 2012-2023, mas contém uma cópia integral do ROE.
- Apêndice I: ROE estático 2012-2023, V13 correto.
- Apêndice J: ROA dinâmico 2012-2023, V13.
- Apêndice K: ROE dinâmico 2012-2023, V13.

O verdadeiro ROA estático 2012-2023 foi reconstruído e salvo em `results/auditoria/modelo_estatico_roa_2012_2023_corrigido.csv`.

## Erro na contagem dos modelos dinâmicos

Os scripts calculam `N` antes de criar a defasagem e executar `na.omit()`.

Amostras efetivas:

- 2000-2023: 3.040 observações, 32 bancos x 95 trimestres úteis, não 3.072.
- 2012-2023: 1.504 observações, 32 bancos x 47 trimestres úteis, não 1.536.

Os graus de liberdade publicados confirmam as amostras efetivas.

## Ajuste necessário na variável ROA

A comparação com `dataset_2024_3.csv` mostrou, em 2.852 observações banco-trimestre comuns:

`ROA_V13 = 1 + ROA_antigo`

com erro numérico máximo em torno de `4,44e-16`.

A dissertação define ROA como `Lucro Líquido / Ativo Total`. Portanto, para o novo artigo:

`ROA_limpo = ROA_V13 - 1`

A soma de 1 não altera os coeficientes within dos modelos publicados, mas distorce as estatísticas descritivas de nível e a interpretação literal da variável.

Regra de versionamento:

- V13 fica preservada como base arquivística de replicação.
- A base canônica do artigo será derivada por script e preservará `ROA_arquivistico` para rastreabilidade.

Script: `scripts/preparacao/01_construir_base_canonica.py`.

## Achado econométrico central: efeito marginal

A especificação original contém simultaneamente:

- `dummy_EG`;
- `DPCDL x dummy_EG`;
- `Endividamento x dummy_EG`;
- `TipoControle x dummy_EG`.

Logo, o coeficiente isolado de `dummy_EG` não é o efeito médio de uma eleição geral.

No modelo estático:

- coeficiente condicional `dummy_EG`: `0,028378`, p `0,0337`;
- efeito marginal médio de eleição, considerando as interações: `0,001069`, SE `0,000675`, p `0,1135`.

No modelo dinâmico:

- coeficiente condicional: `0,022566`, p `0,0340`;
- efeito marginal médio: `0,000952`, SE `0,000637`, p `0,1349`.

O coeficiente condicional corresponde ao caso DPCDL=0, endividamento=0 e banco privado. O endividamento observado não chega a zero, de modo que esse ponto de referência não representa a observação típica da amostra.

Também foi confirmado erro narrativo de notação científica: `2,837812e-02` corresponde a `0,02837812`, não a `2,8378`.

Conclusão: a afirmação de que eleições gerais elevam o ROA em aproximadamente `0,0284` não é uma interpretação correta do modelo com interações.

## Robustez temporal já executada

### Inferência alternativa

O coeficiente condicional permanece positivo e significativo ou limítrofe sob:

- cluster por banco;
- cluster por trimestre;
- two-way cluster;
- Driscoll-Kraay com lags 4 e 8.

Portanto, o principal problema identificado não é apenas a matriz de covariância.

### Leave-one-election-out

A retirada individual das eleições de 2002, 2006, 2010, 2014, 2018 ou 2022 não altera o sinal do coeficiente condicional. A retirada de 2006 produz p-valor de aproximadamente `0,0546`; nos demais casos, o resultado permanece próximo do limiar de 5% ou abaixo dele.

### Sazonalidade

Média setorial de ROA limpo por trimestre:

- T1: `0,002680`;
- T2: `0,006109`;
- T3: `0,003280`;
- T4: `0,007582`.

A diferença média `T4-T3` é `0,004735` em anos de eleição geral e `0,004158` nos demais anos. A diferença entre esses grupos não é estatisticamente relevante no teste simples, p aproximadamente `0,630`.

### Sazonalidade e tendências na regressão

Com efeitos fixos de trimestre do ano e tendências linear/quadrática:

- o coeficiente condicional de `dummy_EG` permanece significativo;
- o efeito marginal médio permanece perto de `0,001` e não significativo a 5%.

### Trimestre efetivo da eleição

Ao recodificar eleição geral como 1 apenas no T4 dos anos 2002, 2006, 2010, 2014, 2018 e 2022, com sazonalidade e tendência:

- sem interações eleitorais: efeito em ROA não significativo;
- com interações: coeficiente condicional significativo, mas efeito marginal médio não significativo.

## Placebo de calendário

Foi feito diagnóstico exploratório com 20.000 calendários artificiais de seis pseudo-anos eleitorais.

- frequência bilateral aproximada para coeficientes tão extremos quanto o observado: `0,064`;
- restringindo os pseudo-anos a anos não municipais: aproximadamente `0,089`.

Não tratar isso como randomization inference formal, pois o calendário eleitoral não é aleatoriamente atribuído e a hipótese de permutabilidade é discutível.

## Leitura científica provisória

A auditoria separou dois resultados que a dissertação tratava como se fossem um só:

1. existe um coeficiente condicional positivo e reproduzível para `dummy_EG` na especificação interagida;
2. o efeito marginal médio implícito pela mesma especificação é muito menor e não é estatisticamente significativo a 5%.

A pergunta do paper deve ser reformulada para avaliar se existe uma associação eleitoral economicamente relevante e temporalmente identificável, não para simplesmente confirmar o coeficiente condicional publicado.

## Arquivos de referência

- `docs/RECONCILIACAO_TABELAS_2026-08-21.md`
- `docs/ACHADO_EFEITO_MARGINAL_ELEICAO_2026-08-21.md`
- `docs/ROBUSTEZ_TEMPORAL_PRELIMINAR_2026-08-21.md`
- `results/auditoria/reconciliacao_bases_tabelas.csv`
- `results/auditoria/efeitos_marginais_eleicao_geral_roa.csv`
- `results/auditoria/inferencia_alternativa_dummy_EG_roa.csv`
- `results/auditoria/leave_one_election_out_roa_static.csv`
- `results/auditoria/sensibilidade_sazonalidade_ame_roa.csv`
- `results/auditoria/evento_trimestre_eleitoral_roa.csv`
- `scripts/auditoria/02_reproduzir_modelos.py`
- `scripts/preparacao/01_construir_base_canonica.py`
- `data/DICIONARIO_DADOS.md`

## Próximos passos

### Etapa A - fechar base canônica

1. gerar a base derivada limpa a partir de V13 pelo script versionado;
2. validar fórmulas de DPCDL, MCAT, spread, CAPAT e CCAT contra as rubricas/fontes de origem;
3. registrar manifesto e hashes da base derivada.

### Etapa B - event study

1. construir tempo relativo à eleição geral, janela inicial `k=-4...+4`;
2. usar T-1 como referência;
3. explicitar que os eventos são choques nacionais comuns e que não há grupo geográfico não tratado;
4. testar pré-padrões e pós-padrões;
5. comparar estimativas em painel e em séries agregadas por trimestre;
6. aplicar inferência compatível com o baixo número efetivo de eventos.

### Etapa C - decidir o paper

Caminho preferencial, sujeito ao event study:

**reavaliação empírica da associação entre ciclos eleitorais e rentabilidade bancária no Brasil, com foco em efeitos marginais, timing e inferência.**

Se aparecer dinâmica temporal consistente e economicamente relevante, o paper poderá sustentar evidência de ciclo eleitoral. Se não aparecer, o resultado será um reassessment da evidência original e das consequências de interpretação de modelos interagidos.

## Regra de continuidade

Não copiar tabelas ou coeficientes da dissertação para o artigo. Todo resultado do novo paper deve ser gerado novamente por script e vinculado a uma base identificada por hash.
