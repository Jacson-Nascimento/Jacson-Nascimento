# Robustez temporal preliminar do resultado eleitoral

Data: 21/08/2026

Status: diagnóstico antes do event study final.

## 1. Ponto de partida

A reprodução da especificação original com a V13 confirma o coeficiente condicional de `dummy_EG` no ROA estático:

- coeficiente: `0,0283781`;
- erro-padrão HC1 clusterizado por banco: `0,0133561`;
- p-valor: `0,03369`.

Entretanto, como o modelo contém `dummy_EG` interagida com DPCDL, endividamento e tipo de controle, esse número não é o efeito médio da eleição. O efeito marginal médio correto foi estimado em aproximadamente `0,001069`, com p-valor `0,1135`.

A robustez temporal abaixo deve, portanto, ser lida em duas camadas distintas: estabilidade do coeficiente condicional e estabilidade do efeito marginal médio.

## 2. Formas alternativas de inferência para o coeficiente condicional

Para `dummy_EG`, o sinal positivo não depende apenas do erro-padrão HC1 por banco.

### Modelo estático

| Inferência | Erro-padrão | p-valor |
|---|---:|---:|
| HC1 cluster por banco, reprodução do `plm` | 0,013356 | 0,0337 |
| cluster por trimestre | 0,009143 | 0,0025 |
| cluster two-way banco e trimestre | 0,013756 | 0,0476 |
| Driscoll-Kraay, lag 4 | 0,011078 | 0,0120 |
| Driscoll-Kraay, lag 8 | 0,009879 | 0,0050 |

### Modelo dinâmico

O coeficiente condicional de `dummy_EG` é `0,0225663`. Os p-valores variam aproximadamente entre `0,011` e `0,050` nas alternativas avaliadas.

Conclusão desta etapa: a principal fragilidade identificada não é uma simples escolha de matriz de covariância. O coeficiente condicional é relativamente estável, mas sua interpretação como efeito médio é inadequada.

Resultados completos:

`results/auditoria/inferencia_alternativa_dummy_EG_roa.csv`

## 3. Leave-one-election-out

Foi retirada, uma de cada vez, cada eleição geral da amostra e reestimado o modelo estático original.

| Eleição retirada | Coeficiente `dummy_EG` | p-valor |
|---|---:|---:|
| nenhuma | 0,028378 | 0,0337 |
| 2002 | 0,021175 | 0,0470 |
| 2006 | 0,030512 | 0,0546 |
| 2010 | 0,027289 | 0,0388 |
| 2014 | 0,030974 | 0,0174 |
| 2018 | 0,029681 | 0,0271 |
| 2022 | 0,028557 | 0,0493 |

O coeficiente condicional não é explicado por uma única eleição específica. A retirada de 2006 leva o p-valor ligeiramente acima de 5%, mas o sinal e a magnitude permanecem próximos.

Resultados completos:

`results/auditoria/leave_one_election_out_roa_static.csv`

## 4. Sazonalidade trimestral

No ROA limpo, a média setorial por trimestre do ano é:

| Trimestre | ROA médio |
|---|---:|
| T1 | 0,002680 |
| T2 | 0,006109 |
| T3 | 0,003280 |
| T4 | 0,007582 |

Há, portanto, forte padrão de nível no quarto trimestre.

Nas seis eleições gerais, a diferença média `T4 - T3` é `0,004735`. Nos demais anos, a mesma diferença é `0,004158`. A diferença entre esses dois grupos é somente `0,000578`, com p-valor de Welch de aproximadamente `0,630`.

O salto bruto no trimestre eleitoral não pode ser atribuído à eleição sem controlar a sazonalidade típica de T4.

## 5. Sazonalidade e tendências no modelo original

Foram adicionados efeitos fixos de trimestre do ano e tendências temporal linear e quadrática.

### Modelo estático

- coeficiente condicional de `dummy_EG`: permanece entre `0,02838` e `0,02896`, com p-valores entre `0,028` e `0,034`;
- efeito marginal médio: permanece perto de `0,00110`, com p-valores entre `0,095` e `0,113`.

### Modelo dinâmico

- coeficiente condicional: permanece entre `0,02251` e `0,02291`, com p-valores perto de `0,030-0,035`;
- efeito marginal médio: permanece perto de `0,00095-0,00099`, com p-valores perto de `0,112-0,135`.

Assim, o controle adicional por sazonalidade e tendência não resolve a divergência entre o coeficiente condicional significativo e o efeito marginal médio não significativo.

Resultados completos:

`results/auditoria/sensibilidade_sazonalidade_ame_roa.csv`

## 6. Recodificação para o trimestre efetivo da eleição

A dummy anual original marca todos os quatro trimestres do ano de eleição geral. Foi criado um indicador alternativo igual a 1 apenas no quarto trimestre dos anos 2002, 2006, 2010, 2014, 2018 e 2022, quando ocorrem as eleições gerais.

A especificação inclui efeitos fixos de trimestre do ano e tendência linear.

### Sem interações eleitorais

- estático: `0,001442`, p `0,3577`;
- dinâmico: `0,001177`, p `0,4050`.

### Mantendo as interações eleitorais

O coeficiente condicional do trimestre eleitoral torna-se alto e significativo, mas o efeito marginal médio continua pequeno e não significativo:

- estático, AME: `0,001360`, p `0,4053`;
- dinâmico, AME: `0,001068`, p `0,4538`.

Resultados completos:

`results/auditoria/evento_trimestre_eleitoral_roa.csv`

## 7. Placebo de calendário, diagnóstico exploratório

Como teste exploratório, foram sorteados conjuntos de seis pseudo-anos eleitorais dentro de 2000-2023 e reestimada a especificação estática. Em 20.000 sorteios, a posição do coeficiente observado produziu frequência empírica bilateral em torno de `0,064`. Restringindo os pseudo-anos a anos que não são municipais, a frequência bilateral ficou em torno de `0,089`.

Este procedimento não deve ser descrito como randomization inference formal. As datas eleitorais brasileiras são institucionais e não foram aleatoriamente atribuídas, portanto a hipótese de permutabilidade é discutível. O resultado serve apenas como diagnóstico de quão incomum é o padrão observado frente a calendários artificiais.

## 8. Leitura provisória

Até aqui, os dados sustentam quatro afirmações distintas:

1. o coeficiente condicional de `dummy_EG` do modelo original é reproduzível e relativamente estável;
2. esse coeficiente não é o efeito médio da eleição na especificação com interações;
3. o efeito marginal médio de eleição sobre ROA é aproximadamente `0,10` ponto percentual e não é estatisticamente significativo a 5% nas especificações avaliadas;
4. a elevação bruta do ROA no quarto trimestre também ocorre em anos não eleitorais e é majoritariamente compatível com sazonalidade de T4.

A próxima etapa não deve buscar preservar a conclusão original. Deve testar, com event study e placebos pré-especificados, se existe alguma dinâmica eleitoral identificável além dessa sazonalidade e da heterogeneidade embutida nas interações.
