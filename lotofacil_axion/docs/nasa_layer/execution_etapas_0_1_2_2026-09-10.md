# AXION NASA Signal Analysis Layer - Execução das Etapas 0, 1 e 2

**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Base:** `data/lotofacil_history.csv`  
**Período:** 29/09/2003 a 05/07/2025, concursos 1 a 3435  
**Status:** Etapas 0, 1 e 2 executadas. Nenhuma regra de seleção foi alterada.

## 1. Objetivo

Construir a infraestrutura comum para os novos módulos do AXION:

1. congelar e mensurar o baseline histórico;
2. transformar os concursos em representação binária 25D e matriz multidimensional de atributos;
3. construir e executar um modelo nulo uniforme Lotofácil 15/25 por Monte Carlo;
4. identificar candidatos a investigação sem converter diferenças descritivas em sinal preditivo.

A regra de decisão permanece: um resultado só pode entrar na geração ou exclusão de combinações após estabilidade temporal, controle de múltiplos testes e validação fora da amostra.

## 2. Etapa 0 - baseline e integridade

Foram processados **3.435 concursos**. A base passou nas checagens de integridade:

- 3.435 concursos únicos;
- nenhuma lacuna na sequência;
- nenhuma linha com dezena duplicada;
- nenhuma dezena fora de 1 a 25;
- nenhuma linha fora de ordem crescente.

**G0 - Integridade: aprovado.**

### Baseline agregado

| Métrica | Histórico | Referência |
|---|---:|---:|
| Média da soma | 195,1671 | 195,0 |
| DP da soma | 17,8878 | ~18,0278 |
| Média de pares | 7,2058 | 7,2 |
| Média de primos | 5,3872 | 5,4 |
| Média de borda | 9,6332 | 9,6 |
| Pares consecutivos, média | 8,3718 | modelo nulo |
| Repetidos do concurso anterior, média | 8,9688 | 9,0 |
| DP das frequências das 25 dezenas | 44,9657 | modelo nulo |
| Amplitude das frequências | 182 | modelo nulo |
| Dispersão de frequências | 23,5449 | modelo nulo |

As métricas combinatórias usuais ficaram próximas das referências esperadas. A exceção preliminar está na dispersão acumulada das frequências individuais.

## 3. Etapa 1 - representação 25D e feature matrix

Foram gerados dois artefatos principais.

### Matriz binária

`binary_matrix.csv`

Dimensão lógica: **3.435 x 25**, além de concurso e data. Cada dezena recebe `1` quando sorteada e `0` quando ausente.

### Feature matrix

`feature_matrix.csv`

Foram calculados **32 atributos**, além de concurso e data:

- soma, média, desvio padrão, mínimo, máximo e amplitude;
- pares e ímpares;
- primos;
- baixas e altas;
- borda e centro;
- pares consecutivos e maior sequência;
- média, DP, máximo e entropia dos gaps;
- distância média par a par;
- repetição e Jaccard em relação ao concurso anterior;
- contagem por cinco linhas e cinco colunas do volante.

A matriz passa a ser a entrada comum para AXION-DST, AXION-BB, AXION-SE/MSE, compressibilidade, PCA/anomalias e recorrência.

**G1 - Reprodutibilidade: aprovado.** Scripts, seed, parâmetros e hash da base foram preservados.

## 4. Etapa 2 - modelo nulo Monte Carlo

Foi implementado um gerador uniforme de subconjuntos de **15 dezenas entre 25, sem reposição**.

Parâmetros:

- 3.435 concursos por história sintética;
- **10.000 histórias sintéticas**;
- seed `20260910`;
- batch size 50;
- p-valores empíricos bicaudais;
- correção Benjamini-Hochberg entre as métricas avaliadas.

### Resultados

| Métrica | Real | Média nula | IC empírico 95% | z | p | q BH | Triagem |
|---|---:|---:|---:|---:|---:|---:|---|
| DP frequência | 44,9657 | 29,0539 | 21,0553 a 37,6077 | 3,77 | 0,00040 | 0,00200 | Sim |
| Amplitude frequência | 182,0 | 115,3289 | 79 a 160 | 3,20 | 0,00350 | 0,01167 | Sim |
| Dispersão frequência | 23,5449 | 10,0372 | 5,1625 a 16,4698 | 4,65 | 0,00040 | 0,00200 | Sim |
| Média soma | 195,1671 | 195,0034 | 194,3909 a 195,6055 | 0,53 | 0,5931 | 0,6590 | Não |
| DP soma | 17,8878 | 18,0289 | 17,6230 a 18,4362 | -0,68 | 0,5051 | 0,6590 | Não |
| Média pares | 7,2058 | 7,2001 | 7,1587 a 7,2422 | 0,27 | 0,7913 | 0,7913 | Não |
| Média primos | 5,3872 | 5,3999 | 5,3604 a 5,4396 | -0,62 | 0,5385 | 0,6590 | Não |
| Média borda | 9,6332 | 9,6001 | 9,5607 a 9,6408 | 1,63 | 0,1079 | 0,2697 | Não |
| Pares consecutivos | 8,3718 | 8,4004 | 8,3590 a 8,4411 | -1,36 | 0,1738 | 0,2896 | Não |
| Repetidos anterior | 8,9688 | 9,0000 | 8,9595 a 9,0408 | -1,50 | 0,1351 | 0,2702 | Não |

**G2 - Modelo nulo: aprovado.**  
**G3 - Múltiplos testes: aplicado.**

## 5. Achado de triagem

A única família de métricas que permaneceu fora da distribuição nula após a correção foi a **heterogeneidade acumulada das frequências das dezenas**.

A frequência esperada por dezena no histórico é:

`3435 x 15/25 = 2061`

Três dezenas apresentaram q BH inferior a 0,05 nos testes binomiais individuais:

| Dezena | Frequência | Desvio | z aprox. | p | q BH |
|---|---:|---:|---:|---:|---:|
| 16 | 1.969 | -92 | -3,20 | 0,00144 | 0,02147 |
| 20 | 2.151 | +90 | 3,13 | 0,00172 | 0,02147 |
| 10 | 2.146 | +85 | 2,96 | 0,00307 | 0,02557 |

**Interpretação:** isso não é evidência de previsibilidade. O resultado pode decorrer de flutuação extrema, efeitos de período, mudanças operacionais, múltiplas explorações ou outras características do processo.

Uma divisão preliminar do histórico em três blocos mostra que o padrão não é constante desde o início. As dezenas 10 e 20 concentram o excesso principalmente nos dois terços mais recentes; a dezena 16 apresenta déficit mais forte no terço final. Isso torna **AXION-BB, Bayesian Blocks**, uma prioridade imediata para testar formalmente mudanças de regime.

## 6. Decisão metodológica

Nenhum filtro, peso ou regra de seleção do AXION foi alterado.

| Gate | Status |
|---|---|
| G0 Integridade | Aprovado |
| G1 Reprodutibilidade | Aprovado |
| G2 Modelo nulo | Aprovado |
| G3 Múltiplos testes | Aplicado |
| G4 Estabilidade temporal | Parcial, ainda não formal |
| G5 Fora da amostra | Não executado |
| G6 Incrementalidade | Não executado |
| G7 Parsimônia | Não executado |
| G8 Auditabilidade | Aprovado nesta execução |

O achado sobre frequências fica classificado como **CANDIDATO DE INVESTIGAÇÃO**, não como sinal operacional.

## 7. Artefatos

### Código

- `scripts/nasa_layer/build_features.py`
- `scripts/nasa_layer/null_simulator.py`

### Resultados compactos versionados no GitHub

- `results/nasa_layer/baseline/baseline_metrics.csv`
- `results/nasa_layer/baseline/frequency_by_number.csv`
- `results/nasa_layer/baseline/baseline_metadata.json`
- `results/nasa_layer/null_distributions/null_summary_B10000.csv`
- `results/nasa_layer/null_distributions/null_run_metadata_B10000.json`

As matrizes completas `binary_matrix.csv`, `feature_matrix.csv` e a distribuição completa de 10.000 simulações foram arquivadas no Google Drive do projeto. Elas são reprodutíveis pelos scripts e não precisam ser duplicadas no GitHub.

## 8. Próxima execução

Ordem proposta:

1. **AXION-BB**, Bayesian Blocks, para localizar e testar mudanças de regime;
2. **AXION-DST**, Decorrelation Transform, na feature matrix;
3. **AXION-SE/MSE**, Sample Entropy e Multiscale Entropy;
4. AXION-COMP e análise de sensibilidade.

A prioridade entre BB e DST foi ajustada após a Etapa 2: a dispersão temporal das frequências precisa ser esclarecida antes de qualquer uso de frequência acumulada.

## 9. Reprodutibilidade

SHA-256 da base usada na execução:

`ebe7f2b6058eb2a6a533516fb6f6ee2cd2f329bf94589f1fbbec9baea5aca271`

A base encerra no concurso **3435, de 05/07/2025**. Concursos posteriores não foram incorporados nesta execução.
