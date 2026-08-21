# Resultados econométricos da auditoria

Data: 21/08/2026

Status: **resultados de reconstrução e diagnóstico, ainda não resultados finais do paper**.

## 1. Reprodução histórica

A reprodução independente por transformação within e matriz HC1 clusterizada por banco reproduz as tabelas finais da dissertação a partir da V13.

A correspondência foi fechada para os Apêndices D, E, F, G, J e K.

Principais resultados de referência:

### ROA estático, 2000-2023

- `dummy_EG`: `0,0283781177`;
- erro-padrão: `0,0133560698`;
- p-valor: `0,0336897`.

### ROA dinâmico, 2000-2023

- `ROA_lag`: `0,2839385018`;
- `dummy_EG`: `0,0225663011`;
- p-valor de `dummy_EG`: `0,0340390`.

## 2. Qual versão da base gerou as tabelas finais

A V13 é identificada como base arquivística final porque:

- V11 usa uma representação anterior da Selic;
- V12 já possui a Selic trimestral corrigida, mas IPCA ainda está em escala percentual;
- V13 mantém a Selic trimestral composta e expressa IPCA em proporção decimal;
- os coeficientes publicados do IPCA estão exatamente na escala produzida pela V13.

SHA-256 V13:

`058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f`

## 3. Apêndice H

O Apêndice H, rotulado como ROA estático 2012-2023, contém na realidade uma duplicação integral do output de ROE do Apêndice I.

O verdadeiro output de ROA foi reconstruído e salvo em:

`results/auditoria/modelo_estatico_roa_2012_2023_corrigido.csv`

Esse é um erro de montagem/transcrição do documento, não um erro na estimação dos demais apêndices.

## 4. Observações dos modelos dinâmicos

Os scripts registram o número de observações antes de gerar a defasagem.

Amostra efetiva:

- período 2000-2023: 3.040, não 3.072;
- período 2012-2023: 1.504, não 1.536.

Os graus de liberdade das próprias tabelas são compatíveis com essas contagens efetivas.

## 5. ROA deslocado por +1

A comparação da V13 com `dataset_2024_3.csv` mostra exatamente, nas 2.852 observações comuns verificadas:

`ROA_V13 = 1 + ROA_antigo`

Enquanto:

`ROE_V13 = ROE_antigo`

A dissertação define ROA como `Lucro Líquido / Ativo Total`. Para o paper, a base canônica deve usar:

`ROA = ROA_arquivistico - 1`

Esse deslocamento constante não altera os coeficientes dos modelos within reproduzidos, mas altera o nível da estatística descritiva e a interpretação literal do indicador.

## 6. Achado econométrico mais relevante

O coeficiente de `dummy_EG` não pode ser interpretado isoladamente como efeito médio da eleição porque a especificação inclui interações:

- `DPCDL x dummy_EG`;
- `Endividamento x dummy_EG`;
- `TipoControle x dummy_EG`.

O efeito marginal é:

```text
ME_it = beta_EG
      + beta_DPCDLxEG * DPCDL_it
      + beta_IENDxEG  * IEND_it
      + beta_PUBLICxEG * PUBLIC_i
```

### ROA estático

- coeficiente condicional `dummy_EG`: `0,028378`, p `0,0337`;
- efeito marginal médio: `0,001069`, SE `0,000675`, p `0,1135`.

### ROA dinâmico

- coeficiente condicional `dummy_EG`: `0,022566`, p `0,0340`;
- efeito marginal médio: `0,000952`, SE `0,000637`, p `0,1349`.

A conclusão publicada de aumento de ROA próximo a `0,0284` trata um coeficiente condicional como se fosse efeito médio. A reconstrução não sustenta essa interpretação.

Além disso, a notação científica `2,837812e-02` corresponde a `0,02837812`, não a `2,8378`.

## 7. Sensibilidade à retirada de interações eleitorais

Quando se estima uma versão sem as interações que contêm `dummy_EG`:

### Estático

- `dummy_EG`: `0,001119`;
- p `0,1496`.

### Dinâmico

- `dummy_EG`: `0,001017`;
- p `0,1429`.

Esse resultado é coerente com o efeito marginal médio do modelo interagido e reforça que a magnitude de `0,0284` é específica ao ponto de referência das interações.

## 8. Inferência alternativa

O coeficiente condicional de `dummy_EG` permanece positivo e significativo ou limítrofe em:

- cluster por banco;
- cluster por trimestre;
- cluster two-way;
- Driscoll-Kraay com diferentes lags.

Portanto, o problema principal não parece ser exclusivamente a escolha de erro-padrão.

## 9. Leave-one-election-out

Retirar individualmente 2002, 2006, 2010, 2014, 2018 ou 2022 não altera o sinal do coeficiente condicional.

A retirada de 2006 produz p próximo de `0,0546`; as demais exclusões mantêm resultado próximo de 5% ou abaixo.

## 10. Sazonalidade

ROA limpo médio por trimestre do ano:

- T1: `0,002680`;
- T2: `0,006109`;
- T3: `0,003280`;
- T4: `0,007582`.

O aumento `T4-T3` ocorre também em anos não eleitorais. A diferença entre anos eleitorais e demais anos nesse salto é pequena e não significativa em teste simples, p aproximadamente `0,630`.

Adicionar efeitos fixos de trimestre do ano e tendências temporal linear/quadrática preserva o coeficiente condicional, mas o efeito marginal médio continua perto de `0,001` e não significativo a 5%.

## 11. Trimestre efetivo da eleição

Ao marcar apenas T4 dos anos de eleição geral:

### Sem interações eleitorais

- estático: `0,001442`, p `0,3577`;
- dinâmico: `0,001177`, p `0,4050`.

### Com interações eleitorais

O coeficiente condicional permanece significativo, mas:

- AME estático: `0,001360`, p `0,4053`;
- AME dinâmico: `0,001068`, p `0,4538`.

## 12. Implicação para o paper

O projeto não deve ser estruturado para confirmar a frase original de que eleições gerais aumentam o ROA em aproximadamente 0,0284.

A pergunta mais defensável é:

**Existe uma associação eleitoral economicamente relevante na rentabilidade bancária brasileira quando os efeitos marginais, o timing do evento e a estrutura temporal são tratados explicitamente?**

O próximo teste decisivo é o event study, acompanhado da validação das fórmulas das variáveis de mecanismo.
