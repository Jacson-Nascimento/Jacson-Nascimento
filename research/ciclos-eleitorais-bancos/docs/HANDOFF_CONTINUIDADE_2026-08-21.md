# HANDOFF - Continuidade do projeto ciclos eleitorais e bancos

Data: 21/08/2026

## Fonte de verdade desta etapa

Este arquivo resume o estado atual da reconstrução da dissertação e deve ser consultado antes de continuar a análise.

## Repositório

`Jacson-Nascimento/Jacson-Nascimento`

Branch de trabalho:

`research/ciclos-eleitorais-bancos-reprodutibilidade`

Diretório:

`research/ciclos-eleitorais-bancos/`

PR de trabalho:

`#63 - Pesquisa: reconstrução reprodutível da dissertação sobre ciclos eleitorais e bancos`

## Objetivo

Transformar a dissertação de mestrado sobre eleições e desempenho bancário em uma linha de pesquisa reprodutível e definir, a partir dos resultados reestimados, o artigo científico derivado mais defensável.

## Estado confirmado

1. A versão textual final da dissertação é a versão de 21/09/2024.
2. O acervo do Drive contém bases brutas, Power BI, bases analíticas, scripts R, literatura, qualificação, defesa e versões históricas.
3. As bases `dataset_290624_11.csv`, `_12.csv` e `_13.csv` foram recuperadas e auditadas.
4. Todas possuem 3.072 linhas, 32 bancos, 96 trimestres, zero duplicidades banco-data e zero NA.
5. V11 e V12 diferem apenas em `taxa_selic_`.
6. V12 e V13 diferem apenas em `Taxa_IPCA`.
7. A Selic da V12/V13 foi reconciliada com `TB_selic_4390_acum_mes_trim.xlsx`: taxa trimestral composta a partir da série mensal 4390.
8. A V13 converte IPCA de percentual para proporção decimal.
9. O script `if_ols_estatico_2.R` usa V11.
10. O script `if_ols_dinamico_2.R` usa V13.
11. O arquivo `if_ols_estatico.R` modificado em 06/08/2024 também usa V11.
12. O `.Rhistory` de 06/08/2024 confirma execução dos scripts finais estático e dinâmico.
13. A reconstrução preliminar do modelo original encontra eleição geral positiva para ROA, próxima de 0,02838.
14. O coeficiente publicado `2,837812e-02` é numericamente compatível com a reconstrução V12/V13, apesar de o script estático arquivado apontar para V11. Isso precisa de reconciliação exata em R.
15. O primeiro teste two-way fixed effects não encontrou heterogeneidade simples estatisticamente forte entre bancos públicos e privados para ROA, ROE ou mecanismos avaliados.

## Risco metodológico identificado

A dissertação não possui um único pipeline final plenamente consistente porque os modelos estático e dinâmico usam versões diferentes da base.

Além disso:

- dummies eleitorais são choques comuns no tempo;
- efeitos fixos completos de trimestre absorvem o efeito principal dessas dummies;
- o efeito agregado de eleição sem efeitos fixos completos de tempo é vulnerável a confundimento por choques macroeconômicos simultâneos;
- a quantidade efetiva de variação do tratamento eleitoral é temporal, muito menor que as 3.072 observações banco-trimestre;
- interações `eleição x banco público` permanecem identificáveis com efeitos fixos de banco e trimestre, mas o teste inicial foi nulo;
- o modelo dinâmico within com variável dependente defasada exige discussão de viés de Nickell;
- GMM não deve ser adotado automaticamente porque o painel possui N=32 e T=96.

## Decisão de desenho para o artigo

A hipótese `banco público x eleição` deixa de ser a pergunta central provisória e passa a robustez secundária.

A pergunta prioritária agora é:

**A associação positiva entre eleições gerais e ROA identificada na dissertação permanece quando a dimensão temporal e a inferência são tratadas de forma mais rigorosa?**

O paper será definido somente depois de:

- reprodução histórica;
- event study por trimestre efetivo da eleição;
- placebos de calendário;
- permutation/randomization inference;
- inferência adequada à dependência temporal e transversal;
- comparação entre ciclos eleitorais.

## Próximos passos operacionais

### Etapa A - fechar base canônica

A proveniência da Selic e do IPCA foi substancialmente resolvida. A V13 é a candidata preferencial.

Restam:

1. localizar, se possível, o script exato que materializou V12 e V13;
2. reproduzir as regressões em R para confirmar que a escala e a transformação não alteram resultados fora do esperado;
3. declarar formalmente a base canônica e incorporá-la ao pacote reprodutível.

### Etapa B - reproduzir a dissertação

1. executar modelo estático com V11, V12 e V13;
2. executar modelo dinâmico com V11, V12 e V13;
3. comparar coeficientes, erros-padrão e p-valores;
4. montar matriz `tabela publicada x script x base`;
5. identificar a origem do erro de duplicação dos apêndices H/I;
6. registrar resultados reproduzidos sem transcrição manual.

### Etapa C - testar a robustez temporal

1. recodificar o trimestre efetivo das eleições gerais e municipais;
2. event study `k=-4...+4`;
3. placebos temporais;
4. permutation/randomization inference;
5. Driscoll-Kraay e alternativas justificadas;
6. análise por ciclo eleitoral individual.

### Etapa D - definir o paper

1. se o efeito de ROA sobreviver, paper de evidência fortalecida de ciclo eleitoral;
2. se desaparecer, paper de reassessment sobre sensibilidade da evidência à dimensão temporal;
3. se surgir mecanismo consistente, reorientar para o mecanismo;
4. atualizar literatura;
5. redigir journal version;
6. pacote reprodutível GitHub/Zenodo.

## Regra de continuidade

Não copiar tabelas ou coeficientes da dissertação para o artigo. Todo resultado do novo paper deve ser gerado novamente por script e vinculado a uma base identificada por hash.
