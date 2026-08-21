# Achado de auditoria: coeficiente de eleição não é o efeito médio da eleição

Data: 21/08/2026

## 1. Problema

A especificação publicada para ROA contém simultaneamente:

- `dummy_EG`;
- `Desp_Provisao_At x dummy_EG`;
- `Indice_individamento x dummy_EG`;
- `dummy_tp x dummy_EG`.

Consequentemente, o coeficiente isolado de `dummy_EG` não representa o efeito geral ou médio de uma eleição geral.

No modelo estático reproduzido com V13:

`beta_deg = 0.0283781177`

Esse coeficiente é o efeito condicional quando:

- `Desp_Provisao_At = 0`;
- `Indice_individamento = 0`;
- `dummy_tp = 0`, ou seja, banco privado.

O índice de endividamento observado na base não chega a zero. Portanto, interpretar `beta_deg` como o efeito típico da eleição envolve extrapolação para um ponto fora do suporte empírico relevante.

## 2. Efeito marginal correto

No modelo original, o efeito marginal de mudar `dummy_EG` de 0 para 1 é:

```text
ME_it = beta_deg
      + beta_dpcdl:deg * DPCDL_it
      + beta_iend:deg  * IEND_it
      + beta_deg:dtc   * DTC_i
```

Como o modelo é linear, o efeito marginal médio pode ser calculado pela combinação linear dos coeficientes nos valores médios das variáveis. O erro-padrão foi calculado pelo método delta usando a mesma matriz robusta clusterizada por banco utilizada na reprodução do modelo.

## 3. Resultados para ROA

### Modelo estático, 2000-2023

| Grupo/amostra | Efeito marginal médio | Erro-padrão | p-valor |
|---|---:|---:|---:|
| Todos os bancos, toda a amostra | 0,001069 | 0,000675 | 0,1135 |
| Todos os bancos, apenas observações de anos de eleição geral | 0,001116 | 0,000696 | 0,1090 |
| Bancos privados | 0,001445 | 0,000906 | 0,1109 |
| Bancos públicos | 0,000109 | 0,000754 | 0,8853 |

### Modelo dinâmico, 2000-2023

| Grupo/amostra | Efeito marginal médio | Erro-padrão | p-valor |
|---|---:|---:|---:|
| Todos os bancos, toda a amostra | 0,000952 | 0,000637 | 0,1349 |
| Todos os bancos, apenas observações de anos de eleição geral | 0,001004 | 0,000670 | 0,1343 |
| Bancos privados | 0,001138 | 0,000809 | 0,1596 |
| Bancos públicos | 0,000479 | 0,000797 | 0,5473 |

## 4. Consequência para a conclusão da dissertação

A significância estatística de `beta_deg` isoladamente não demonstra que o efeito médio das eleições gerais sobre ROA seja estatisticamente diferente de zero no modelo que contém interações.

A reprodução indica que:

- o coeficiente condicional `dummy_EG` é positivo e significativo;
- o efeito marginal médio resultante do conjunto `dummy_EG + interações` é muito menor, aproximadamente 0,10 ponto percentual;
- esse efeito marginal médio não é estatisticamente significativo a 5% com a mesma estrutura de inferência utilizada no modelo original.

Assim, a frase de que eleições gerais elevam o ROA em `0,0284` não é uma interpretação correta da especificação estimada.

## 5. Distribuição do efeito marginal

No modelo estático, os efeitos marginais calculados para as 3.072 observações têm:

- média: `0,001069`;
- mediana: aproximadamente `0,000037`;
- 25º percentil: aproximadamente `-0,001115`;
- 75º percentil: aproximadamente `0,001816`;
- proporção de efeitos pontuais positivos: aproximadamente 50,9%.

Isso reforça que o efeito implícito na especificação é heterogêneo e próximo de zero para uma grande parcela da amostra.

## 6. Implicação para o novo artigo

Este achado muda a prioridade analítica.

Antes de procurar uma especificação nova que preserve a conclusão original, o paper deve separar três questões:

1. o coeficiente condicional de `dummy_EG`;
2. o efeito marginal médio de eleição na presença das interações;
3. a robustez temporal desse efeito a placebos, sazonalidade e diferentes formas de inferência.

O novo artigo não deve reportar `beta_deg` como efeito agregado de eleição quando houver interações com `dummy_EG`.

Os resultados numéricos estão registrados em:

`results/auditoria/efeitos_marginais_eleicao_geral_roa.csv`
