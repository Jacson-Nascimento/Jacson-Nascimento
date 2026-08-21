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

## Objetivo

Transformar a dissertação de mestrado sobre eleições e desempenho bancário em uma linha de pesquisa reprodutível e, inicialmente, em um artigo sobre heterogeneidade entre bancos públicos e privados durante ciclos eleitorais.

## Estado confirmado

1. A versão textual final da dissertação é a versão de 21/09/2024.
2. O acervo do Drive contém bases brutas, Power BI, bases analíticas, scripts R, literatura, qualificação, defesa e versões históricas.
3. As bases `dataset_290624_11.csv`, `_12.csv` e `_13.csv` foram recuperadas e auditadas.
4. Todas possuem 3.072 linhas, 32 bancos, 96 trimestres, zero duplicidades banco-data e zero NA.
5. V11 e V12 diferem apenas em `taxa_selic_`.
6. V12 e V13 diferem apenas em `Taxa_IPCA`.
7. A V13 converte IPCA de percentual para proporção decimal.
8. O script `if_ols_estatico_2.R` usa V11.
9. O script `if_ols_dinamico_2.R` usa V13.
10. O `.Rhistory` de 06/08/2024 confirma execução dos scripts finais estático e dinâmico.

## Risco metodológico identificado

A dissertação não possui um único pipeline final plenamente consistente porque os modelos estático e dinâmico usam versões diferentes da base.

Além disso:

- dummies eleitorais são choques comuns no tempo;
- efeitos fixos completos de trimestre absorvem o efeito principal dessas dummies;
- o efeito agregado de eleição sem efeitos fixos completos de tempo é vulnerável a confundimento por choques macroeconômicos simultâneos;
- interações `eleição x banco público` permanecem identificáveis com efeitos fixos de banco e trimestre;
- o modelo dinâmico within com variável dependente defasada exige discussão de viés de Nickell.

## Decisão de desenho para o artigo

Priorizar a seguinte pergunta:

**Bancos públicos apresentam comportamento de rentabilidade diferente dos bancos privados em torno das eleições gerais e municipais brasileiras?**

Baseline previsto:

- efeitos fixos de banco;
- efeitos fixos de trimestre;
- interações `Public x Eleição Geral` e `Public x Eleição Municipal`;
- controles bancários que variam no nível banco-trimestre;
- ROA e ROE como outcomes principais.

Extensão principal:

- event study de `Public x tempo relativo à eleição`.

## Próximos passos operacionais

### Etapa A - fechar proveniência da base

1. localizar o script que gerou V11, V12 e V13;
2. documentar a transformação da Selic;
3. verificar o Power BI final `pbi_dre_resumo_macro_eleicao.pbix` apenas se necessário para reconciliar a transformação;
4. declarar a base canônica.

### Etapa B - reproduzir a dissertação

1. executar modelo estático com V11, V12 e V13;
2. executar modelo dinâmico com V11, V12 e V13;
3. comparar coeficientes, erros-padrão e p-valores;
4. reconciliar tabelas do PDF final;
5. identificar a origem do erro de duplicação dos apêndices H/I.

### Etapa C - construir o paper

1. two-way fixed effects;
2. event study;
3. mecanismos;
4. robustezes;
5. atualização da literatura;
6. redação journal version;
7. pacote reprodutível GitHub/Zenodo.

## Regra de continuidade

Não copiar tabelas ou coeficientes da dissertação para o artigo. Todo resultado do novo paper deve ser gerado novamente por script e vinculado a uma base identificada por hash.
