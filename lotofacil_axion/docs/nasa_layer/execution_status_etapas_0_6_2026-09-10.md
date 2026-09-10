# AXION NASA Signal Analysis Layer - Status Consolidado Etapas 0 a 6

**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Base congelada:** concursos 1 a 3435, 29/09/2003 a 05/07/2025  
**Regra:** nenhum módulo altera seleção ou exclusão de jogos sem aprovação nos gates G0 a G8.

## 1. Síntese executiva

A primeira rodada da NASA Signal Analysis Layer foi concluída até a Etapa 6. O resultado mais relevante não é um preditor de dezenas. É uma anomalia agregada: a dispersão histórica das frequências entre as 25 dezenas é maior do que a esperada sob o modelo nulo uniforme 15/25. Essa diferença aparece em alguns recortes temporais e permanece no histórico acumulado.

Os testes desenhados para explicar essa diferença por mecanismos mais estruturados, entretanto, não confirmaram uma fonte preditiva. Bayesian Blocks não sustentou mudanças de regime após múltiplos testes. Sample/Multiscale Entropy não encontrou complexidade temporal aprovada. AXION-DST apresentou sinal limítrofe em um holdout, mas falhou na replicação rolling. AXION-COMP não encontrou compressibilidade adicional robusta.

Conclusão operacional: a dispersão de frequências passa a ser tratada como objeto de auditoria estatística e estabilidade de longo prazo, não como regra de números quentes/frios.

## 2. Status dos módulos

| Etapa | Módulo | Resultado | Decisão |
|---|---|---|---|
| 0 | Baseline e integridade | 3435 concursos íntegros | Aprovado |
| 1 | Matriz binária 25D e features | infraestrutura construída | Aprovado |
| 2 | Modelo nulo Monte Carlo | comparação real x sintético implementada | Aprovado |
| 3 | AXION-BB | 0 de 25 dezenas com q < 0,05 | Reprovado para integração |
| 4 | AXION-DST | holdout inicial q ~ 0,071 | Inconclusivo inicialmente |
| 5 | AXION-SE/MSE | 0 candidatos após BH | Reprovado para integração |
| G4/G5 | DST rolling | 0 de 5 splits significativos após BH | Sinal inicial não replicado |
| G4 | Estabilidade de frequências | vários recortes e histórico total significativos | Anomalia agregada permanece |
| 6 | AXION-COMP | 0 de 16 testes com q < 0,05 | Reprovado para integração |

## 3. Estabilidade da dispersão de frequências

Foi usada como métrica primária a dispersão qui-quadrado das contagens das 25 dezenas em relação à expectativa 0,6N. O nulo foi aproximado por normal multivariada construída com os momentos exatos de uma extração uniforme 15 de 25, com B = 100.000 por tamanho de amostra. A aproximação foi conferida contra o Monte Carlo exato da Etapa 2 no histórico completo.

Recortes que sobreviveram ao BH dentro da métrica primária:

| Desenho | Concursos | Chi2 real | q BH |
|---|---:|---:|---:|
| Janela 500 | 1-500 | 17,84 | 0,0471 |
| Janela 500 | 2001-2500 | 19,5133 | 0,0226 |
| Janela 1000 | 2001-3000 | 24,2633 | 0,00261 |
| Expanding | 1-500 | 17,84 | 0,0471 |
| Expanding | 1-3000 | 21,6933 | 0,00638 |
| Expanding | 1-3435 | 23,5449 | 0,00261 |

No histórico completo, as três medidas permanecem acima do esperado:

- desvio-padrão das frequências: 44,9657, q = 0,00261;
- amplitude: 182, q = 0,02736;
- qui-quadrado: 23,5449, q = 0,00261.

Interpretação: o desvio não é uniforme em todo o tempo, mas reaparece e se acumula. Isso justifica investigação de alocação de frequência entre dezenas, mas não autoriza inferência causal nem seleção prospectiva.

## 4. Replicação temporal do AXION-DST

O resultado inicial do DST havia apresentado duas diferenças nominais, média da distância e KS, ambas com q ~ 0,071. Para testar estabilidade, foram criados cinco cortes cronológicos, sempre ajustando a transformação no passado e avaliando o bloco seguinte.

Nenhum dos cinco splits apresentou q < 0,05 para a média da distância ou para o teste KS. O split final apresentou p nominal de 0,0403 para a média, mas q = 0,1916 após o controle sobre os cinco testes.

Decisão revisada: AXION-DST não é aprovado. O sinal inicial é classificado como instável e exploratório.

## 5. AXION-COMP

A matriz binária foi serializada em orientações por linha e por coluna e submetida a zlib e bz2, em blocos de 250, 500, 1000 e 3435 concursos. A hipótese era que estrutura temporal/global adicional tornaria o histórico real mais compressível que histórias sintéticas 15/25.

Nenhum dos 16 testes sobreviveu ao BH. O menor p nominal foi obtido para o histórico completo em layout por coluna com bz2, p = 0,03097, mas q = 0,4955.

Decisão: não há evidência robusta de compressibilidade global adicional.

## 6. Leitura conjunta

Os resultados criam uma assimetria metodologicamente importante:

1. existe evidência de dispersão excessiva das frequências acumuladas entre dezenas;
2. essa evidência é temporalmente irregular, mas persiste no agregado;
3. não foi confirmada uma explicação por mudanças discretas de regime;
4. não foi confirmada complexidade temporal multiescala por dezena;
5. não foi confirmada estrutura global compressível;
6. a transformação multivariada DST não replicou de forma estável.

Portanto, o fenômeno sobrevivente é mais simples do que as hipóteses alternativas testadas. O próximo risco é o projeto tentar explicar à força uma anomalia real de amostra com um mecanismo que os dados não sustentam.

## 7. Gates após a Etapa 6

- G0 Integridade: APROVADO.
- G1 Reprodutibilidade: APROVADO.
- G2 Modelo nulo: APROVADO.
- G3 Múltiplos testes: APROVADO nos experimentos executados.
- G4 Estabilidade: APROVADO apenas para a existência agregada de dispersão em parte relevante dos recortes; REPROVADO para DST.
- G5 Fora da amostra: DST não replicou; demais hipóteses não chegaram a sinal aprovado.
- G6 Incrementalidade: PENDENTE para a arquitetura de geração.
- G7 Parcimônia: APROVADO, nenhum módulo complexo foi incorporado sem evidência.
- G8 Auditabilidade: APROVADO, scripts e saídas preservados.

## 8. Próxima etapa, AXION-MC de sensibilidade e ablation

A Etapa 7 deve auditar o gerador de combinações existente, retirando um filtro de cada vez e variando seus parâmetros para medir contribuição marginal sobre cobertura, diversidade, sobrevivência do espaço residual e desempenho prospectivo.

Há uma condição de governança antes da execução: usar exatamente a configuração atual do gerador. O `run_full_cycle.py` do repositório está armazenado em um wrapper comprimido. A análise de sensibilidade não deve ser executada com filtros reconstruídos de documentação antiga, porque isso criaria uma baseline diferente da efetivamente usada.

Assim, o próximo passo é extrair de forma auditável a configuração do runner atual ou localizar a configuração canônica equivalente. Só depois será executada a matriz de ablation.

## 9. Decisão atual

Nenhuma técnica NASA testada até aqui aumenta a probabilidade matemática atribuída a uma combinação específica. Nenhuma delas foi autorizada a alterar os jogos gerados.

O achado que permanece sob investigação é a dispersão agregada das frequências. Ela será tratada como hipótese de auditoria estatística, com prioridade para estabilidade, origem operacional e eventual incrementalidade fora da amostra.
