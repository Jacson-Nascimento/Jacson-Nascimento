# Plano de artigo derivado da dissertação

Status: versão revisada após auditoria de reprodutibilidade e efeitos marginais.

## Título provisório preferencial

**Ciclos Eleitorais e Rentabilidade Bancária no Brasil: Uma Reavaliação dos Efeitos, do Timing e da Inferência**

Título em inglês:

**Electoral Cycles and Bank Profitability in Brazil: Reassessing Effects, Timing, and Inference**

## Pergunta central

A associação positiva entre eleições gerais e ROA encontrada na dissertação permanece quando:

1. a base e os modelos são reproduzidos de forma rastreável;
2. os termos de interação são interpretados por efeitos marginais, e não apenas pelo coeficiente principal da dummy;
3. a eleição é localizada no trimestre efetivo;
4. sazonalidade e dinâmica temporal são tratadas explicitamente;
5. a inferência considera que o choque eleitoral é comum a todos os bancos no mesmo período?

## Motivação empírica

A reprodução confirmou o coeficiente condicional de `dummy_EG` no modelo original de ROA. Entretanto, o modelo também inclui interações de `dummy_EG` com DPCDL, endividamento e tipo de controle.

Assim, o coeficiente principal de `dummy_EG` não é o efeito médio da eleição. O efeito marginal correto varia com características observadas do banco.

Na amostra completa:

- coeficiente condicional estático de `dummy_EG`: aproximadamente `0,02838`, p `0,0337`;
- efeito marginal médio estático: aproximadamente `0,00107`, p `0,1135`;
- efeito marginal médio dinâmico: aproximadamente `0,00095`, p `0,1349`.

Essa divergência cria a contribuição central do novo artigo: separar coeficiente condicional, efeito marginal médio e dinâmica temporal.

## Contribuições propostas

### 1. Reprodutibilidade

Reconstruir integralmente a cadeia `base -> especificação -> coeficientes -> inferência`, identificando a V13 como base arquivística efetivamente compatível com as tabelas finais.

### 2. Interpretação de modelos interagidos

Mostrar que a interpretação econômica de uma dummy eleitoral em presença de interações exige combinações lineares e efeitos marginais no suporte da amostra.

### 3. Timing

Substituir a dummy anual, usada durante os quatro trimestres do ano eleitoral, por indicadores associados ao trimestre efetivo da eleição e por tempo relativo ao evento.

### 4. Inferência temporal

Comparar erros-padrão por banco, tempo, two-way e Driscoll-Kraay, além de diagnósticos de calendário e leave-one-election-out.

## Hipóteses de trabalho

As hipóteses abaixo são perguntas testáveis, não conclusões pré-definidas.

### H1

O efeito marginal médio de eleição geral sobre ROA é diferente de zero após considerar as interações do modelo.

### H2

Existe dinâmica diferenciada de ROA nos trimestres imediatamente anteriores e posteriores às eleições gerais, além da sazonalidade típica do quarto trimestre.

### H3

Os resultados não são explicados por uma única eleição específica.

### H4

Se houver associação eleitoral, mecanismos bancários como provisões, spread ou crédito apresentam dinâmica temporal coerente com o resultado de rentabilidade.

## Base

Referência arquivística:

`dataset_290624_13.csv`

SHA-256:

`058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f`

Painel:

- 32 bancos;
- 96 trimestres;
- 2000T1 a 2023T4;
- 3.072 observações na especificação estática;
- 3.040 observações efetivas no modelo dinâmico de período completo.

Para o artigo será criada base canônica derivada, preservando `ROA_arquivistico` e usando:

`ROA = ROA_arquivistico - 1`

A correção de nível não altera as estimações within reproduzidas, mas corrige a interpretação e as estatísticas descritivas.

## Estratégia empírica

### Bloco 1 - replicação

Reproduzir os modelos estático e dinâmico da dissertação com V13.

Objetivo: estabelecer benchmark auditável, não tratá-lo automaticamente como modelo preferencial.

### Bloco 2 - efeitos marginais

Para o modelo com interações:

```text
ME_it(EG) = beta_EG
          + beta_DPCDLxEG * DPCDL_it
          + beta_IENDxEG  * IEND_it
          + beta_PUBLICxEG * PUBLIC_i
```

Reportar:

- efeito marginal médio;
- intervalo de confiança;
- efeitos por tipo de controle;
- distribuição dos efeitos individuais implícitos;
- suporte das covariáveis usadas para interpretar o coeficiente principal.

### Bloco 3 - recodificação do evento

Criar indicador de eleição geral no trimestre efetivo, T4 nos ciclos 2002, 2006, 2010, 2014, 2018 e 2022.

A especificação simples, sem interações eleitorais, será usada como benchmark interpretável.

### Bloco 4 - event study

Janela inicial:

`k = -4,...,+4`

Referência:

`k = -1`

Como todas as instituições recebem o mesmo choque eleitoral nacional, o event study será apresentado como análise de dinâmica temporal associativa, não como desenho clássico de tratamento versus controle.

Será comparado com:

- sazonalidade de trimestre do ano;
- tendências temporais;
- médias setoriais agregadas por trimestre;
- ciclos individuais.

### Bloco 5 - inferência

Avaliar:

- HC1 cluster por banco, para reprodução;
- cluster por trimestre;
- two-way cluster banco e trimestre;
- Driscoll-Kraay;
- inferência em séries agregadas, quando apropriada;
- leave-one-election-out.

Permutações de calendário poderão ser usadas somente como diagnóstico, com ressalva explícita de que o calendário eleitoral não é aleatoriamente atribuído.

## Resultados preliminares já estabelecidos

1. V13 reproduz as tabelas finais relevantes da dissertação.
2. O Apêndice H contém uma duplicação do ROE e não o ROA estático 2012-2023.
3. A linha de observações dos modelos dinâmicos usa contagem pré-defasagem.
4. O ROA arquivístico da V13 contém deslocamento de +1 frente à definição contábil.
5. O coeficiente condicional eleitoral é estável a várias matrizes de covariância e ao leave-one-election-out.
6. O efeito marginal médio eleitoral é muito menor e não significativo a 5% nas especificações já avaliadas.
7. O quarto trimestre apresenta sazonalidade positiva relevante mesmo fora de anos eleitorais.
8. A dummy restrita ao trimestre efetivo da eleição, sem interações eleitorais, não apresenta efeito significativo nos primeiros testes.

## Mecanismos

Somente serão desenvolvidos se houver fundamento empírico após o event study.

Candidatos:

- despesa de provisão sobre ativos;
- spread;
- carteira de crédito sobre ativos;
- eficiência;
- endividamento.

Antes disso, as fórmulas de DPCDL, MCAT, spread, CAPAT e CCAT devem ser reconciliadas com as fontes/rubricas de origem.

## Estrutura prevista do paper

1. Introdução
2. Contexto institucional e ciclos eleitorais no Brasil
3. Literatura
4. Dados e reconstrução da base
5. Estratégia empírica
6. Replicação do resultado original
7. Efeitos marginais e interpretação das interações
8. Timing eleitoral e event study
9. Robustez e inferência
10. Discussão
11. Conclusão
12. Apêndice de reprodutibilidade

## Regra de interpretação

O artigo não deve afirmar, sem evidência adicional:

- causalidade eleitoral;
- manipulação política de crédito;
- interferência política direta;
- gerenciamento de resultados;
- efeito médio a partir de um coeficiente principal de dummy que participe de interações.

## Critério para decidir a narrativa final

### Cenário A

Event study, efeitos marginais e robustez sustentam padrão eleitoral consistente.

Narrativa: evidência revisada e mais bem identificada de associação entre eleições e rentabilidade bancária.

### Cenário B

O coeficiente condicional permanece, mas efeitos marginais e timing não sustentam efeito economicamente relevante.

Narrativa: reassessment da evidência, mostrando como interpretação de interações e estrutura temporal alteram a conclusão.

### Cenário C

Surge mecanismo específico e consistente.

Narrativa: reorientar o paper para o mecanismo, mantendo a replicação como ponto de partida.

## Próxima etapa

Executar o event study e validar as fórmulas das variáveis de mecanismo antes da redação da versão journal.
