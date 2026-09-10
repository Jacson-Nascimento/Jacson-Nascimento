# AXION NASA Signal Analysis Layer - Execução das Etapas 3, 4 e 5

**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Base congelada:** concursos 1 a 3435, 29/09/2003 a 05/07/2025  
**Status:** AXION-BB, AXION-DST e AXION-SE/MSE executados. Nenhuma regra de seleção/exclusão foi alterada.

## 1. Objetivo

Executar os três primeiros módulos analíticos da NASA Signal Analysis Layer após a construção do baseline, da matriz binária 25D e do modelo nulo Monte Carlo.

A hipótese nula permanece a aleatoriedade. Um resultado exploratório só pode entrar na geração de combinações se sobreviver aos gates de múltiplos testes, estabilidade temporal, validação fora da amostra e incrementalidade.

## 2. Etapa 3 - AXION-BB, mudanças de regime

Foi aplicada uma adaptação para séries Bernoulli de presença/ausência das 25 dezenas. O procedimento possui duas camadas:

1. segmentação exata observada por programação dinâmica, com log-verossimilhança Bernoulli por bloco e penalidade inicial de Scargle;
2. gate inferencial pela maior evidência de uma mudança de taxa, calibrada contra 20.000 sequências Bernoulli(0,6) com o mesmo comprimento do histórico.

Parâmetros principais:

- p0 = 0,05;
- penalidade Scargle = 6,5898059012;
- tamanho mínimo do bloco para o teste de split = 30 concursos;
- B = 20.000 sequências nulas;
- seed = 20260910;
- correção de Benjamini-Hochberg sobre 25 dezenas.

### Resultado

Nenhuma dezena sobreviveu a q < 0,05.

Principais resultados nominais:

| Dezena | p empírico | q BH | Melhor mudança estimada |
|---|---:|---:|---|
| 1 | 0,0168 | 0,3534 | taxa 0,7326 antes do concurso 173 e 0,5967 depois |
| 20 | 0,0343 | 0,3534 | taxa 0,5868 antes do concurso 1170 e 0,6465 depois |
| 10 | 0,0483 | 0,3534 | taxa 0,5611 antes do concurso 541 e 0,6366 depois |
| 23 | 0,0565 | 0,3534 | não significativo |
| 7 | 0,0873 | 0,4365 | não significativo |

A segmentação exata, quando observada sem o gate nulo, cria blocos para as dezenas 1, 6, 7 e 22. Esses blocos não devem ser interpretados como regimes reais porque a evidência não sobrevive ao controle inferencial. Há inclusive blocos curtos e extremos, comportamento compatível com seleção de coincidências em séries longas.

### Decisão AXION-BB

**REPROVADO para integração preditiva nesta versão.**

A hipótese de que os desvios acumulados das dezenas 10, 16 e 20 sejam explicados por mudanças de regime discretas não foi sustentada após correção de múltiplos testes.

## 3. Etapa 4 - AXION-DST, Decorrelation Transform

A feature matrix original possui 32 atributos. O módulo foi ajustado em uma amostra cronológica de treinamento de 80% e testado nos 20% finais.

Procedimento:

- treinamento: concursos 1 a 2748;
- holdout: concursos 2749 a 3435, 687 concursos;
- padronização baseada apenas no treinamento;
- decomposição espectral da matriz de correlação/covariância padronizada;
- 23 componentes não degeneradas retidas;
- whitening no subespaço PCA;
- score por distância quadrática no espaço descorrelacionado;
- calibração com 100.000 sorteios sintéticos 15/25;
- bootstrap B = 5.000;
- correção BH sobre quatro testes globais do módulo.

### Resultado

| Métrica | Histórico holdout | Modelo nulo | p | q BH |
|---|---:|---:|---:|---:|
| Distância quadrática média | 24,2051 | 23,3736 | 0,0356 | 0,0712 |
| Quantil 95% | 41,9565 | 41,7023 | 0,8776 | 0,8776 |
| Excedências do q99 nulo | 5 de 687, 0,73% | esperado 1% | 0,6982 | 0,8776 |
| KS da distribuição | 0,0580 | - | 0,0197 | 0,0712 |

Há uma pequena diferença global na região central da distribuição, mas não há excesso de cauda ou anomalias extremas. As duas diferenças nominais, média e KS, deixam de atingir 5% após correção BH.

### Decisão AXION-DST

**INCONCLUSIVO, manter em observação.**

O módulo não foi aprovado para influenciar jogos, mas apresentou o sinal mais próximo do limiar dentre os três módulos desta fase. O próximo teste adequado é replicar essa diferença em cortes temporais independentes e em holdouts sucessivos, sem recalibrar a regra retrospectivamente.

## 4. Etapa 5 - AXION-SE/MSE, Sample Entropy e Multiscale Entropy

Foram analisadas as 25 séries binárias individuais.

Parâmetros:

- m = 2;
- escalas = 1, 2, 3, 5, 10 e 20;
- r/SD = 0,15 e 0,20;
- coarse-graining por médias de blocos não sobrepostos;
- B = 5.000 sequências Bernoulli(0,6);
- p empírico bicaudal por escala;
- teste multiescala conjunto por distância padronizada T;
- BH em 25 dezenas dentro de cada parametrização.

### Resultado

Nenhuma dezena sobreviveu a q < 0,05 no teste multiescala e nenhum resultado por escala foi aprovado no gate correspondente.

Menores p-valores multiescala, r/SD = 0,15:

| Dezena | T | p empírico | q BH |
|---|---:|---:|---:|
| 7 | 21,1341 | 0,0080 | 0,1650 |
| 25 | 19,3241 | 0,0132 | 0,1650 |
| 23 | 16,1168 | 0,0300 | 0,2137 |
| 20 | 15,6285 | 0,0342 | 0,2137 |
| 10 | 13,4144 | 0,0586 | 0,2929 |
| 16 | 11,4314 | 0,0960 | 0,3999 |

Os resultados com r/SD = 0,20 foram essencialmente idênticos nas escalas avaliadas, o que reduz preocupação com sensibilidade imediata ao parâmetro, mas não cria evidência de estrutura temporal não aleatória.

### Decisão AXION-SE/MSE

**REPROVADO para integração preditiva nesta versão.**

Não foi encontrada evidência suficiente de regularidade temporal ou complexidade multiescala nas séries individuais que exceda o comportamento de sequências Bernoulli marginais sob o modelo nulo.

## 5. Síntese dos três módulos

| Módulo | Gate atual | Leitura |
|---|---|---|
| AXION-BB | Reprovado | mudanças de regime não sobrevivem a múltiplos testes |
| AXION-DST | Inconclusivo | pequeno deslocamento multivariado global, q = 0,0712 |
| AXION-SE/MSE | Reprovado | complexidade temporal compatível com o modelo nulo |

O achado anterior de dispersão excessiva das frequências acumuladas continua existindo no baseline, mas não foi explicado por mudanças discretas de regime nem por complexidade temporal individual detectável com os testes desta fase.

Isso muda a interpretação. A evidência acumulada sugere, por enquanto, que o desvio de frequência deve ser investigado como fenômeno agregado de distribuição entre dezenas e estabilidade de longo prazo, e não convertido diretamente em regra de números quentes/frios.

## 6. Gates metodológicos após a Etapa 5

- G0 Integridade: APROVADO.
- G1 Reprodutibilidade: APROVADO.
- G2 Modelo nulo: APROVADO para os módulos executados.
- G3 Múltiplos testes: APROVADO, BH aplicado.
- G4 Estabilidade temporal: PENDENTE para AXION-DST e para a dispersão de frequências.
- G5 Fora da amostra: PARCIAL. O DST utilizou holdout, mas ainda requer replicações sucessivas.
- G6 Incrementalidade: PENDENTE.
- G7 Parcimônia: nenhum módulo foi integrado prematuramente.
- G8 Auditabilidade: APROVADO, scripts, parâmetros e saídas preservados.

## 7. Próxima decisão técnica

A ordem recomendada passa a ser:

1. testar estabilidade temporal da dispersão de frequências em janelas e holdouts sucessivos;
2. replicar AXION-DST em múltiplos cortes cronológicos;
3. implementar AXION-COMP, compressibilidade, como teste de estrutura global da matriz 25D;
4. somente depois executar AXION-MC de sensibilidade e ablation dos filtros de geração;
5. manter BB e SE/MSE documentados como experimentos não aprovados, sem apagar resultados.

Nenhum resultado desta fase justifica aumentar a probabilidade matemática atribuída a uma combinação específica da Lotofácil.
