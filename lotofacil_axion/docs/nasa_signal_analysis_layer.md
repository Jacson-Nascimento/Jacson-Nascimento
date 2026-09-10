# AXION - Novos Modelos Inspirados em Métodos NASA

**Roadmap técnico e protocolo de validação**  
**Versão:** 0.1  
**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento

## 1. Objetivo

Registrar a nova camada experimental do Modelo AXION para a Lotofácil, inspirada em técnicas usadas pela NASA e pelo JPL em análise de sinais, imagens, telemetria, detecção de anomalias e séries temporais.

O objetivo não é assumir capacidade preditiva sobre sorteios independentes. O objetivo é testar se o histórico real contém estrutura estatística que permaneça distinguível de histórias sintéticas geradas sob aleatoriedade perfeita.

### Princípio de decisão

Um método só entra no processo de geração ou exclusão de combinações se produzir informação estável, replicável e fora do comportamento esperado no modelo nulo aleatório.

## 2. Posição na arquitetura AXION

Fluxo proposto:

```text
Histórico Lotofácil
        |
Representação binária 25D
        |
Matriz de atributos
        |
NASA Signal Analysis Layer
        |
Comparação com modelo nulo
        |
Validação fora da amostra
        |
AXION residual / geração de combinações
```

A nova camada complementa, e não substitui, os componentes já utilizados no projeto, como entropia, PCA, clustering, DBSCAN, coocorrências, heurísticas combinatórias e otimização.

## 3. Módulos prioritários

### 3.1 AXION-DST - Decorrelation Transform

**Prioridade:** muito alta.  
**Inspiração:** Decorrelation Stretch aplicado pelo JPL em processamento multiespectral.

**Objetivo:** remover correlações lineares entre atributos do sorteio e ampliar dimensões estatísticas pouco visíveis na representação original.

**Entrada:** matriz de atributos por concurso, incluindo soma, paridade, primos, altas/baixas, gaps, consecutivos, repetição do concurso anterior, entropia, métricas de rede, linhas/colunas e borda/centro.

**Método:** centralização, matriz de covariância, decomposição em autovetores/autovalores e whitening.

```text
Z = (X - mu) P Lambda^(-1/2)
```

**Saídas:** componentes descorrelacionadas, scores por concurso, distâncias no espaço transformado e ranking de anomalia.

**Teste obrigatório:** comparar distribuição dos scores e distâncias com milhares ou milhões de histórias sintéticas 15/25.

**Risco:** amplificação de ruído. Nenhum score será tratado como sinal preditivo sem validação contra o modelo nulo.

### 3.2 AXION-BB - Bayesian Blocks

**Prioridade:** muito alta.  
**Inspiração:** método de Jeffrey Scargle, NASA Ames.

**Objetivo:** detectar mudanças de regime determinadas pelos próprios dados, reduzindo dependência de janelas arbitrárias como 10, 30, 50 ou 100 concursos.

**Aplicações:** presença/ausência de cada dezena, soma, repetição entre concursos, paridade, gaps, entropia e coocorrência de pares.

**Saídas:** pontos de mudança, segmentos estatisticamente homogêneos, duração dos regimes e tamanho do efeito.

**Teste obrigatório:** taxa de falsos regimes em séries sintéticas equivalentes e estabilidade dos pontos de mudança em reamostragem.

**Critério de aceitação:** mudança persistente e efeito maior do que o observado no intervalo central do modelo nulo.

### 3.3 AXION-SE/MSE - Sample Entropy e Multiscale Entropy

**Prioridade:** muito alta.  
**Inspiração:** aplicações NASA de Approximate Entropy, Sample Entropy e análise multiescala.

**Objetivo:** medir regularidade e complexidade temporal além da entropia de Shannon já utilizada.

**Entrada principal:** séries binárias de cada dezena, 1 se sorteada e 0 se ausente. Entradas adicionais: séries de paridade, soma, gaps, repetição, pares e trios.

**Saídas:** SampEn, ApEn quando útil, curvas de entropia por escala e comparação real versus sintética.

**Teste obrigatório:** sensibilidade aos parâmetros `m` e `r`, tamanho mínimo da série, estabilidade temporal e distribuição sob o modelo nulo.

**Critério de aceitação:** diferença persistente em várias escalas, não apenas em uma parametrização isolada.

### 3.4 AXION-COMP - Compressibility Analysis

**Prioridade:** alta.

**Objetivo:** operacionalizar a aproximação da complexidade de Kolmogorov já prevista no AXION.

**Entrada:** matriz binária `N x 25` e sequências derivadas.

**Método:** medir taxa de compressão de blocos de 20, 50, 100, 250 e mais concursos. Comparar `C_real` com a distribuição `C_random` de histórias sintéticas.

```text
DeltaC = C_real - E(C_random)
```

**Teste obrigatório:** múltiplos algoritmos de compressão, controle por tamanho de bloco e replicação com seeds independentes.

**Critério de aceitação:** desvio estável, material e replicável em relação ao modelo nulo.

### 3.5 AXION-MC - Monte Carlo e Sensitivity Analysis

**Prioridade:** muito alta.

**Objetivo:** identificar quais filtros, pesos e módulos efetivamente alteram cobertura, diversidade, estabilidade e distribuição de acertos, evitando manter regras apenas por plausibilidade intuitiva.

**Entradas:** pesos e limites de todos os filtros AXION.

**Saídas:** métricas de sensibilidade, ablation tests, influência marginal dos filtros e ranking de contribuição.

**Aplicações:** cobertura de dezenas, pares e trios; diversidade entre jogos; entropia; sobrevivência do espaço residual; similaridade entre jogos; desempenho fora da amostra.

**Critério de aceitação:** contribuição incremental estável e não explicada apenas por redução artificial do espaço amostral.

## 4. Módulos exploratórios secundários

### 4.1 AXION-PCA-AD - PCA Anomaly Detection

Transformar o PCA atual, hoje principalmente descritivo/visual, em módulo formal de detecção probabilística de anomalias multivariadas. Utilizar scores, resíduos, Hotelling T2, distância de Mahalanobis e comparação com simulações.

### 4.2 AXION-RQA - Recurrence Quantification Analysis

Investigar recorrências, determinismo aparente, laminaridade e persistência no espaço de estados. Uso exploratório devido ao alto risco de interpretar coincidências como dinâmica real.

### 4.3 AXION-HURST

Estimar persistência ou antipersistência em séries derivadas. Exigir intervalos de confiança e comparação com sequências aleatórias de mesmo tamanho.

### 4.4 AXION-LS - Lomb-Scargle

Investigar periodicidades, principalmente quando forem usadas datas reais dos concursos. Exigir correção de múltiplos testes, controle de false discovery rate e validação em simulações.

### 4.5 AXION-GP - Gaussian Processes

Modelar estruturas suaves ou quase periódicas apenas quando uma evidência anterior justificar o teste. Não será utilizado como preditor direto de dezenas sem evidência fora da amostra.

## 5. Modelo nulo obrigatório

A referência de todos os experimentos será um gerador sintético Lotofácil 15/25 sem reposição, com probabilidade uniforme para todas as combinações.

Para cada técnica:

1. calcular a estatística no histórico real;
2. gerar `B` histórias sintéticas com o mesmo número de concursos;
3. recalcular a mesma estatística em cada história;
4. obter a distribuição empírica do modelo nulo;
5. calcular posição percentual, z-score quando aplicável, p-valor empírico e tamanho de efeito;
6. corrigir múltiplos testes quando houver varredura de dezenas, períodos, frequências ou parâmetros;
7. repetir com seeds independentes;
8. reservar período final do histórico para validação fora da amostra.

Valor inicial recomendado: `B >= 10.000` para triagem e `B >= 100.000` para resultados candidatos. Milhões de simulações serão usados apenas quando o ganho de precisão justificar o custo computacional.

## 6. Gates de validação

| Gate | Critério |
|---|---|
| G0 | Integridade dos dados, sem duplicidades, colunas validadas e concursos ordenados |
| G1 | Reprodutibilidade, seed, versão do código e parâmetros registrados |
| G2 | Estatística real comparada à distribuição sintética equivalente |
| G3 | Correção de múltiplos testes quando necessária |
| G4 | Resultado persiste em recortes temporais e reamostragem |
| G5 | Efeito não desaparece no período fora da amostra |
| G6 | Módulo acrescenta informação além das métricas AXION existentes |
| G7 | Ganho justifica complexidade adicional |
| G8 | Saídas, parâmetros, logs e resultados intermediários preservados |

Um módulo reprovado não será apagado. Permanecerá documentado como experimento rejeitado ou inconclusivo, preservando o histórico metodológico.

## 7. Roadmap de implementação

1. **Etapa 0:** congelar o baseline AXION atual e registrar métricas de referência.
2. **Etapa 1:** construir matriz binária concurso x 25 dezenas e feature matrix padronizada.
3. **Etapa 2:** implementar gerador nulo uniforme e pipeline Monte Carlo.
4. **Etapa 3:** implementar AXION-DST e testes de distância/anomalia.
5. **Etapa 4:** implementar AXION-BB e estudar mudanças de regime.
6. **Etapa 5:** implementar AXION-SE/MSE nas 25 séries binárias e variáveis agregadas.
7. **Etapa 6:** implementar AXION-COMP com múltiplas janelas e algoritmos de compressão.
8. **Etapa 7:** implementar AXION-MC com sensibilidade e ablation tests dos filtros existentes.
9. **Etapa 8:** avaliar PCA-AD, RQA, Hurst, Lomb-Scargle e GP.
10. **Etapa 9:** integrar somente módulos aprovados à camada residual de exclusão/seleção.
11. **Etapa 10:** executar backtest temporal estritamente prospectivo e comparar com baseline e seleção aleatória.

## 8. Métricas de comparação

Não usar apenas quantidade de acertos. Registrar também:

- distribuição de 11, 12, 13, 14 e 15 acertos;
- média e variância de acertos;
- cobertura de dezenas, pares e trios;
- distância média entre jogos;
- proporção do espaço residual sobrevivente;
- estabilidade temporal;
- tamanho de efeito versus aleatório;
- custo computacional;
- sensibilidade a parâmetros;
- taxa de falsos positivos;
- desempenho fora da amostra.

## 9. Regra de governança metodológica

O AXION não deverá converter uma técnica sofisticada em evidência preditiva apenas porque ela produz um padrão visual, cluster, regime ou score extremo. A hipótese prioritária continuará sendo a aleatoriedade. O ônus da evidência fica com o novo método.

Pergunta operacional de cada módulo:

> A estrutura encontrada no histórico real é estatisticamente distinguível daquela produzida por histórias Lotofácil perfeitamente aleatórias, e essa diferença sobrevive fora da amostra?

## 10. Estrutura de arquivos sugerida

```text
lotofacil_axion/
  docs/
    nasa_signal_analysis_layer.md
  scripts/
    nasa_layer/
      build_features.py
      null_simulator.py
      axion_dst.py
      axion_bayesian_blocks.py
      axion_entropy.py
      axion_compression.py
      axion_sensitivity.py
  results/
    nasa_layer/
      baseline/
      null_distributions/
      validation/
```

A criação dos scripts ocorrerá por etapas. Esta especificação é registrada antes da implementação para reduzir o risco de ajuste retrospectivo dos critérios aos resultados.

## 11. Referências de partida

- NASA/JPL, Decorrelation Stretch e processamento multiespectral.
- NASA Technical Reports Server, Decorrelation Stretch Algorithm Theoretical Basis: https://ntrs.nasa.gov/citations/20060034467
- NASA Ames / Scargle, Bayesian Blocks: https://ntrs.nasa.gov/citations/20020054342
- NASA Goddard, Approximate Entropy e Sample Entropy: https://ntrs.nasa.gov/citations/20190025788
- NASA, Multiscale entropy em análise de sistemas: https://ntrs.nasa.gov/citations/20220004950
- NASA/JPL, PCA e detecção de anomalias: https://ntrs.nasa.gov/citations/20220000760
- NASA Langley, compressão e detecção de anomalias: https://ntrs.nasa.gov/citations/20130011182
- NASA, Recurrence Quantification Analysis: https://ntrs.nasa.gov/citations/20170000421
- NASA, Monte Carlo e sensitivity analysis: https://ntrs.nasa.gov/citations/20180000063
- NASA, Lomb-Scargle: https://ntrs.nasa.gov/citations/19830035792

## 12. Status

**Status geral:** PLANEJADO / EXPERIMENTAL.  
**Próxima execução técnica:** Etapas 0, 1 e 2, seguidas pelo AXION-DST, AXION-BB e AXION-SE/MSE.
