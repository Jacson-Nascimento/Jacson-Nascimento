# AXION NASA Signal Analysis Layer - Etapa 7 e Gate G5

**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Freeze histórico para hipótese:** concurso 3435, 05/07/2025  
**Holdout genuíno:** concursos 3436 a 3779, até 03/09/2026

## 1. Etapa 7 - AXION-MC Sensitivity / Ablation

A biblioteca AXION 0.3 possui 40 configurações: 22 marginais, 9 blend, 6 pair e 3 repeat. A validação nested temporal foi reproduzida com 2.935 previsões externas pré-freeze.

### Resultado do modelo completo

- média de acertos: **9,04736**;
- 334 resultados com >=11 acertos, 52 com >=12 e 6 com >=13;
- Brier médio: **0,240159**;
- teste nominal da média contra 9: p = **0,0373**;
- Brier contra o baseline constante 0,24: p = **0,0248**, com direção ligeiramente pior que 0,24.

O ganho nominal de acertos não foi acompanhado por melhora de calibração probabilística.

### Ablations

Nenhuma remoção produziu diferença estatisticamente defensável em relação ao modelo completo após BH.

- `no_pair`: resultado idêntico ao full;
- `no_repeat`: resultado idêntico ao full;
- `prior100_only` / `no_prior25`: resultado idêntico ao full;
- `no_blend`: delta médio de -0,00750 acerto, q = 1,0;
- `marginal_only`: delta médio de -0,00988, q = 1,0;
- `no_decay`: delta médio de -0,00920, q = 1,0.

Nos oito folds, o full selecionou apenas famílias marginal e blend. Pair e repeat nunca foram escolhidos. Configurações com prior 25 também não foram escolhidas.

**Decisão:** pair, repeat e prior 25 não demonstraram contribuição incremental no período auditado. Não serão apagados, mas passam a candidatos de desativação operacional para redução de custo e complexidade.

## 2. Persistência da dispersão de frequências no período pré-freeze

A anomalia de dispersão acumulada motivou teste específico de persistência.

- correlação Pearson dos vetores de desvio entre primeira e segunda metade: **r = 0,41415**;
- p paramétrico: **0,03957**;
- Spearman: **rho = 0,55115**, p = **0,00430**;
- estratégia rolling 1000 concursos, top-15 por frequência: média **9,05133**;
- teste nominal contra 9: p = **0,03607**.

Três simulações nulas independentes, 5.000 histórias cada, foram executadas. Pool B = **15.000**:

- p empírico da correlação >= observada: **0,01967**;
- p empírico do fixed 50% >= observado: **0,01447**;
- p empírico do rolling >= observado: **0,01987**;
- conjunção correlação + rolling: **0,00140**.

Esses resultados justificaram o Gate G5 em dados posteriores ao concurso 3435. Não justificaram integração preditiva.

## 3. Gate G5 - holdout genuíno pós-3435

A base corrente do repositório permitiu um teste particularmente forte: 344 concursos posteriores ao dataset originalmente usado para definir a hipótese, concursos 3436 a 3779.

### Regra fixa top-15, congelada no concurso 3435

Top-15 pré-freeze: **01 02 03 04 05 09 10 11 12 13 14 20 22 24 25**.

- média no holdout: **9,08721**;
- p empírico Monte Carlo, B = 200.000: **0,09741**;
- Brier: **0,239974**, sem diferença de 0,24.

Direção positiva, porém sem replicação estatística.

### Regra rolling 1000

- média no holdout: **9,02035**;
- p empírico: **0,38745**.

O efeito observado no período pré-freeze praticamente desapareceu.

### Persistência do vetor de viés

- Pearson pré-freeze vs holdout: **r = 0,33466**, p = **0,10202**;
- Spearman: **rho = 0,28338**, p = **0,16986**.

A direção permaneceu positiva, mas o efeito não passou o Gate G5.

### AXION 0.3 no mesmo holdout

- 344 previsões nested externas, sem concursos faltantes;
- single game: média **9,01744**, p empírico = **0,40244**;
- Brier médio: **0,240231**;
- carteira 10: **10,80233**;
- benchmark aleatório carteira 10: **10,89349**;
- diferença pareada: **-0,09116**, p nominal = **0,04492**.

Após correção BH dos cinco testes principais, nenhum resultado permaneceu significativo. O menor q foi **0,17003**.

## 4. Conclusão de gate

**G5 REPROVADO para uso preditivo.**

A dispersão e a persistência aparente pré-freeze foram reais enquanto descrição daquele histórico e passaram por testes nulos razoáveis. Porém a vantagem não se reproduziu de forma estatisticamente suficiente nos 344 concursos genuinamente posteriores.

Isso altera a interpretação do projeto:

1. não há suporte atual para promover frequências persistentes a regra de seleção;
2. o AXION 0.3 completo não demonstrou vantagem no holdout genuíno;
3. complexidade adicional, especialmente pair/repeat, não se justificou;
4. o caminho metodológico passa a ser simplificação, registro prospectivo e novos testes apenas quando houver evidência externa ou novo mecanismo testável;
5. módulos exploratórios de alto risco de data mining, como GP, RQA, Hurst e Lomb-Scargle, não serão promovidos automaticamente só para manter o roadmap.

A preservação dos resultados negativos é parte do protocolo de reprodutibilidade e evita viés de publicação interno.
