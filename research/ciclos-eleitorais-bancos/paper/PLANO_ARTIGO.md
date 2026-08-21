# Plano de artigo derivado da dissertação

## Status em 21/08/2026

O desenho inicialmente preferido, centrado na heterogeneidade simples entre bancos públicos e privados durante anos eleitorais, **não recebeu apoio nos primeiros testes two-way fixed effects**. Por isso, o projeto não fixará ainda uma narrativa de artigo.

A prioridade passa a ser reproduzir integralmente a dissertação e testar se o efeito agregado de eleição geral sobre ROA resiste a uma estratégia de inferência temporal mais exigente.

## Título de trabalho provisório

**Ciclos Eleitorais e Rentabilidade Bancária no Brasil: Reavaliação com Dados Trimestrais, 2000-2023**

Título em inglês:

**Electoral Cycles and Bank Profitability in Brazil: A Reassessment Using Quarterly Data, 2000-2023**

O título será alterado se os testes mostrarem que outro mecanismo oferece uma pergunta mais forte.

## Pergunta central provisória

A associação positiva entre eleições gerais e ROA identificada na dissertação permanece quando a dimensão temporal, os placebos e a dependência dos erros são tratados de forma mais rigorosa?

## Problema de identificação

As dummies de eleição geral e municipal são comuns a todos os bancos em determinado trimestre/ano. Isso implica que:

1. o painel possui muitas observações banco-trimestre, mas o tratamento eleitoral varia apenas no tempo;
2. efeitos fixos completos de trimestre absorvem o efeito principal das eleições;
3. uma regressão com apenas efeitos fixos de banco pode atribuir à eleição outros choques nacionais ocorridos nos mesmos anos;
4. a inferência não deve tratar as 3.072 observações como 3.072 variações independentes do tratamento eleitoral.

Esse ponto deve ser enfrentado diretamente no paper, e não escondido por uma especificação mais conveniente.

## Evidência inicial a explicar

Na reconstrução aproximada da especificação original:

- eleição geral permanece associada positivamente ao ROA, com coeficiente próximo de 0,02838;
- eleição municipal não apresenta o mesmo padrão;
- ROE não confirma resultado agregado equivalente.

Na especificação com efeitos fixos de banco e de trimestre:

- as interações `Público x Eleição Geral` e `Público x Eleição Municipal` não são estatisticamente significativas para ROA ou ROE;
- uma triagem de mecanismos também não mostrou heterogeneidade público x privado forte.

Portanto, a heterogeneidade por controle passa a ser robustez secundária.

## Estratégia empírica a desenvolver

### Etapa 1 - reprodução histórica

Reproduzir exatamente as tabelas da dissertação com:

- V11;
- V12;
- V13;
- scripts originais;
- erros-padrão originais.

Objetivo: estabelecer qual combinação `base + script` gerou cada tabela publicada.

### Etapa 2 - baseline reavaliado

Manter efeitos fixos de banco e controles bancários, mas tratar explicitamente a baixa dimensão temporal efetiva do tratamento.

Alternativas de inferência a comparar:

- Driscoll-Kraay;
- erros agrupados adequadamente à estrutura do painel, quando identificáveis;
- bootstrap temporal por blocos, se tecnicamente justificável;
- randomization/permutation inference sobre a posição dos anos eleitorais.

A escolha final deverá ser justificada, não selecionada pelo menor p-valor.

### Etapa 3 - estudo de evento temporal

Recodificar o evento pelo trimestre efetivo das eleições, em vez de marcar os quatro trimestres do ano eleitoral como equivalentes.

Janela inicial:

```text
k = -4, -3, -2, -1, 0, +1, +2, +3, +4
```

onde `k=0` é o trimestre da eleição e `k=-1` poderá ser a referência.

Objetivos:

1. verificar se o padrão aparece antes da eleição;
2. identificar se a associação está concentrada no trimestre eleitoral ou pós-eleitoral;
3. comparar eleições gerais e municipais;
4. verificar estabilidade entre os seis ciclos gerais observados.

### Etapa 4 - placebos

Construir pseudo-eleições em anos/trimestres não eleitorais, preservando número e espaçamento aproximado dos eventos.

Pergunta:

`O coeficiente observado para eleições reais é incomum em relação ao que obteríamos com calendários placebo?`

Esse teste é central porque o tratamento eleitoral possui poucos eventos temporais.

### Etapa 5 - heterogeneidade e mecanismos

Somente após o resultado agregado ser compreendido serão explorados:

- bancos públicos versus privados;
- bancos públicos federais versus demais bancos;
- carteira de crédito / ativos;
- provisões / ativos;
- spread;
- eficiência.

Não será construída narrativa de mecanismo a partir de significância isolada.

## Outcomes

### Principais

- ROA
- ROE

### Secundários

- MCAT, após confirmar definição e construção;
- despesa de provisão sobre ativos;
- spread bancário;
- eficiência;
- endividamento.

## Robustezes previstas

- comparação V11/V12/V13;
- 2000-2023 versus 2012-2023;
- eleições gerais e municipais separadamente;
- trimestre eleitoral versus ano eleitoral;
- análise por ciclo individual;
- Driscoll-Kraay e alternativas de inferência temporal;
- placebos e permutation inference;
- winsorização somente com regra pré-definida;
- modelos dinâmicos como robustez, com discussão do viés de Nickell;
- interação público x eleição como resultado secundário.

## Pontos que não serão afirmados sem evidência adicional

- causalidade eleitoral;
- manipulação política de crédito;
- gerenciamento de resultados;
- interferência política direta;
- fraude ou irregularidade.

## Critério de decisão do artigo

Após a reprodução e os testes temporais:

### Se o efeito geral sobre ROA sobreviver

O artigo será uma reavaliação fortalecida da evidência de ciclo eleitoral na rentabilidade bancária.

### Se o efeito desaparecer

O resultado pode sustentar um artigo de reassessment mostrando que a conclusão original era sensível ao tratamento da dimensão temporal e da inferência.

### Se surgir mecanismo consistente

O paper poderá ser reorientado para esse mecanismo, desde que a hipótese seja economicamente justificável e validada em diferentes ciclos.

## Sequência de trabalho

1. reproduzir a dissertação;
2. fechar base canônica;
3. reconciliar tabela publicada x script x base;
4. confirmar dicionário de variáveis;
5. estimar inferência robusta ao tempo;
6. executar event study;
7. executar placebos/permutation inference;
8. avaliar mecanismos e heterogeneidade;
9. atualizar literatura;
10. definir a pergunta final do paper;
11. redigir versão journal;
12. preparar pacote reprodutível GitHub/Zenodo.
