# Plano de artigo derivado da dissertação

## Título provisório

**Ciclos Eleitorais e Heterogeneidade do Desempenho Bancário no Brasil: Bancos Públicos e Privados, 2000-2023**

Título em inglês:

**Electoral Cycles and Heterogeneous Bank Performance in Brazil: Public and Private Banks, 2000-2023**

## Pergunta central

Bancos públicos apresentam comportamento de rentabilidade diferente dos bancos privados em torno das eleições gerais e municipais brasileiras?

## Por que este recorte é preferível

A dummy eleitoral é comum a todos os bancos em cada trimestre. Um coeficiente agregado de eleição, sem efeitos fixos completos de tempo, pode confundir eleição com outros choques nacionais que ocorram nos mesmos períodos.

Ao incluir efeitos fixos de banco e de trimestre, os efeitos principais de `Public_i` e `Election_t` são absorvidos, mas a interação `Public_i × Election_t` permanece identificável. O artigo passa a medir uma diferença relativa entre bancos públicos e privados em períodos eleitorais, o que é econometricamente mais defensável.

## Especificação baseline

Para banco `i` e trimestre `t`:

```text
Y_it = alpha_i + lambda_t
       + beta1 (Public_i x GeneralElection_t)
       + beta2 (Public_i x MunicipalElection_t)
       + gamma' X_it
       + epsilon_it
```

Onde:

- `Y_it`: ROA ou ROE;
- `alpha_i`: efeito fixo do banco;
- `lambda_t`: efeito fixo do trimestre;
- `X_it`: controles bancários que variam entre banco e tempo;
- `beta1` e `beta2`: diferenças relativas de bancos públicos frente aos privados em períodos eleitorais.

Variáveis macroeconômicas comuns a todos os bancos no trimestre não precisam entrar simultaneamente com efeitos fixos completos de trimestre, porque são absorvidas por `lambda_t`.

## Event study

A extensão principal será um estudo de evento em torno das eleições gerais:

```text
Y_it = alpha_i + lambda_t
       + sum_k beta_k [Public_i x 1(t - eleição = k)]
       + gamma' X_it
       + epsilon_it
```

Janela inicial sugerida: `k = -4,...,+4` trimestres, omitindo `k=-1` como referência.

Objetivos:

1. verificar pré-tendências diferenciais;
2. localizar temporalmente a divergência entre públicos e privados;
3. distinguir antecipação, trimestre eleitoral e pós-eleição.

## Outcomes

### Principais

- ROA
- ROE

### Mecanismos candidatos

- carteira de crédito / ativos (`MCAT`, confirmar definição)
- despesa de provisão / ativos
- spread bancário
- endividamento
- eficiência

O artigo não deve transformar todos os mecanismos em outcomes principais. A prioridade é ROA/ROE; mecanismos entram para explicar os resultados, se houver sinal consistente.

## Hipóteses

### H1

A diferença de desempenho entre bancos públicos e privados se altera durante eleições gerais.

### H2

A heterogeneidade associada às eleições gerais é maior que a associada às eleições municipais, dado o maior vínculo da política federal com bancos públicos federais e condições macrofinanceiras nacionais.

### H3

Se existir heterogeneidade eleitoral, ela será acompanhada por mudanças em variáveis de mecanismo, como crédito, provisões ou spread, em vez de aparecer apenas como variação contábil de ROA/ROE.

## Robustezes previstas

- ROA e ROE separadamente;
- erros-padrão agrupados por banco;
- avaliação de dependência temporal e cross-sectional para inferência;
- tendências específicas por grupo, se justificadas;
- exclusão de crises ou choques extremos apenas como robustez, nunca como especificação principal;
- winsorização apenas com regra pré-definida e relatório do número de observações afetadas;
- especificação 2012-2023 como comparação com período regulatório mais recente;
- modelos dinâmicos como robustez, não como baseline;
- avaliação de sensibilidade a bancos públicos federais versus demais públicos, se a classificação permitir.

## Pontos que não serão afirmados sem evidência adicional

- efeito causal agregado das eleições sobre todos os bancos;
- manipulação política de crédito;
- gerenciamento de resultados;
- interferência política direta;
- fraude ou irregularidade.

Essas interpretações exigiriam variáveis e desenhos adicionais.

## Sequência de trabalho

1. reproduzir a dissertação;
2. escolher base canônica;
3. reconstruir dicionário de variáveis;
4. estimar baseline two-way fixed effects;
5. executar event study;
6. testar mecanismos;
7. fazer robustezes;
8. atualizar literatura;
9. redigir versão de periódico;
10. preparar pacote reprodutível e Zenodo.
