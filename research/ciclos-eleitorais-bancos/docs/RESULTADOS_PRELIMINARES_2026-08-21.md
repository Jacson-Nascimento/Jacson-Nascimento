# Resultados econométricos preliminares

Data: 21/08/2026

Status: **diagnóstico exploratório, não resultado final do paper**.

## Objetivo

Testar rapidamente se os resultados centrais da dissertação são reproduzíveis e se a hipótese de heterogeneidade simples entre bancos públicos e privados oferece uma base promissora para o novo artigo.

A reprodução exata em R ainda é necessária porque os scripts originais foram escritos com `plm` e `vcovHC`. Os testes abaixo foram reconstruídos independentemente em Python para triagem metodológica.

## 1. Especificação próxima da dissertação

Com efeitos fixos de banco e a estrutura de covariáveis/interações do script original, o resultado central de ROA permanece próximo do reportado na dissertação:

- eleição geral: coeficiente aproximado `0,02838`, positivo e estatisticamente significativo;
- eleição municipal: coeficiente negativo, sem a mesma precisão estatística;
- ROE: não reproduz padrão eleitoral agregado equivalente.

A estimativa de eleição geral em V12/V13 coincide, até as casas exibidas, com o coeficiente `2,837812e-02` registrado no texto/tabela final. Isso é relevante porque o script estático arquivado aponta para V11, sugerindo que a tabela publicada pode ter vindo de uma execução posterior ou intermediária.

## 2. Heterogeneidade público x privado com two-way fixed effects

Foi testado um modelo com:

- efeito fixo de banco;
- efeito fixo de trimestre;
- controles bancários que variam no tempo;
- interações `Público x Eleição Geral` e `Público x Eleição Municipal`;
- erros-padrão agrupados por banco.

Resultados:

| Outcome | Interação | Coeficiente | Erro-padrão | p-valor |
|---|---|---:|---:|---:|
| ROA | Público x Eleição Geral | -0,001462 | 0,001231 | 0,235 |
| ROA | Público x Eleição Municipal | 0,001134 | 0,001098 | 0,302 |
| ROE | Público x Eleição Geral | -0,005461 | 0,009374 | 0,560 |
| ROE | Público x Eleição Municipal | 0,004292 | 0,007648 | 0,575 |

Não há evidência preliminar de heterogeneidade simples de rentabilidade entre bancos públicos e privados nos anos eleitorais.

## 3. Teste exploratório de mecanismos

Também foi feita uma triagem two-way fixed effects, sem seleção ex post de significância, para:

- eficiência;
- endividamento;
- spread;
- PC;
- PCC;
- MCAT;
- despesa de provisão sobre ativos.

As interações simples `Público x Eleição Geral` e `Público x Eleição Municipal` não apresentaram evidência estatística forte nesses outcomes no primeiro teste.

Esse resultado reduz a atratividade de um paper centrado apenas em `banco público versus privado`.

## 4. Consequência para a estratégia de pesquisa

O resultado não deve ser tratado como fracasso do projeto. Ele muda a pergunta.

A dissertação contém um efeito agregado de eleição geral sobre ROA sob efeitos fixos de banco, mas esse efeito é de natureza exclusivamente temporal. Ao inserir efeitos fixos completos de trimestre, o efeito principal da eleição deixa de ser identificável porque é comum a todos os bancos.

O problema científico passa a ser:

**o resultado agregado originalmente observado representa um ciclo eleitoral específico ou está capturando choques macroeconômicos nacionais coincidentes com anos de eleição?**

Essa pergunta permite um artigo de reavaliação empírica mais defensável, desde que sejam acrescentados testes de robustez temporal e inferência apropriada.

## 5. Caminhos candidatos

### Caminho A - Reavaliação do efeito eleitoral agregado

Pergunta:

`Há evidência robusta de um ciclo eleitoral na rentabilidade bancária brasileira quando se trata adequadamente a dimensão temporal?`

Testes necessários:

- Driscoll-Kraay ou alternativas adequadas à dependência transversal e serial;
- placebos de calendário;
- randomization/permutation inference sobre anos eleitorais;
- estudo de evento em torno do trimestre eleitoral;
- tendências e controles macroeconômicos parcimoniosos;
- sensibilidade por subperíodo.

### Caminho B - Ciclos eleitorais e composição dos resultados bancários

Em vez de ROA/ROE como único foco, decompor possíveis mecanismos:

- margem/spread;
- provisões;
- carteira de crédito;
- eficiência.

Só avançar se os mecanismos mostrarem padrão temporal consistente e economicamente interpretável, não apenas significância pontual.

### Caminho C - Artigo de replicação e reprodutibilidade

Reconstruir integralmente a dissertação, documentar as versões da base e mostrar como escolhas de frequência, escala macroeconômica, efeitos fixos e inferência alteram ou preservam a conclusão.

Esse caminho é metodologicamente legítimo, mas a escolha de periódico deve considerar o espaço editorial para replication/reassessment papers.

## 6. Regra para a próxima rodada

Não escolher a narrativa do artigo antes de concluir:

1. reprodução exata em R;
2. event study;
3. inferência temporal robusta;
4. placebos;
5. análise de sensibilidade por ciclo eleitoral.

A hipótese de heterogeneidade público x privado permanece como robustez secundária, não mais como hipótese central provisória.
