# Adendo Metodológico — Strength como ordenação principal dos choques

Data: 18/08/2026

## Motivo

O teste de robustez que excluiu instrumentos com `origem_externa = True` mostrou que as medidas de concentração da carteira permanecem praticamente invariantes em amostra comum de compradores, e que os choques direcionados por `Strength` continuam muito acima da distribuição aleatória.

Em contraste, os resultados de choque por `Degree` foram mais sensíveis à definição da rede e à exclusão de compras com origem externa.

## Decisão

A especificação principal das simulações passa a ser:

1. calcular `Strength` dos fornecedores na rede global observada;
2. ordenar os fornecedores de forma decrescente por `Strength`;
3. remover 1%, 5% e 10% dos fornecedores mais fortes;
4. medir `Loss_b(R)` e a proporção de compradores com perdas >=25%, >=50% e >=75%;
5. comparar cada choque direcionado com 1.000 ou mais remoções aleatórias da mesma quantidade de fornecedores.

## Especificações complementares

`Degree` global continua sendo reportado como métrica de alcance relacional e como teste de robustez. O artigo não deverá tratá-lo isoladamente como medida definitiva de criticidade sistêmica.

Também será obrigatória a robustez:

- rede completa;
- exclusão de `origem_externa`;
- ranking global versus ranking restrito à subamostra elegível.

## Evidência diagnóstica jan-fev

Na amostra comum de 361 compradores, a exclusão de origem externa produziu praticamente os mesmos níveis de HHI, HHI normalizado, CR1, CR4 e divergência valor-frequência.

Choques por `Strength`, perda >=50%:

- 1% removido: 7,48% de compradores severamente expostos tanto na rede completa quanto sem origem externa, contra cerca de 0,35% no aleatório;
- 5%: 24,93% na rede completa e 22,44% sem origem externa, contra cerca de 1,9% no aleatório;
- 10%: 40,44% e 38,50%, respectivamente, contra cerca de 4,3% no aleatório.

## Interpretação

`Strength` representa centralidade econômica observada, não substituibilidade técnica. A remoção simulada mede exposição contratual da carteira e não demonstra interrupção real de serviço.

Esta decisão deverá ser reavaliada com a rede anual de 2025, mas passa a ser a especificação preferida nas análises intermediárias.
