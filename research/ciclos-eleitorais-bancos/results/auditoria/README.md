# Resultados da auditoria econométrica

Este diretório reúne outputs reconstruídos a partir das bases históricas da dissertação. Eles são resultados de auditoria e diagnóstico, não resultados finais do novo artigo.

## Arquivos

- `reconciliacao_bases_tabelas.csv`: compara V11, V12 e V13 com as tabelas publicadas e identifica V13 como base arquivística final.
- `modelo_estatico_roa_2012_2023_corrigido.csv`: output de ROA que deveria ter aparecido no Apêndice H.
- `efeitos_marginais_eleicao_geral_roa.csv`: efeitos marginais médios de eleição geral nos modelos estático e dinâmico.
- `sensibilidade_interacoes_roa.csv`: compara coeficiente condicional, efeito marginal médio e especificação sem interações eleitorais.
- `inferencia_alternativa_dummy_EG_roa.csv`: matrizes de covariância alternativas para o coeficiente condicional.
- `leave_one_election_out_roa_static.csv`: sensibilidade à retirada individual dos ciclos gerais.
- `sensibilidade_sazonalidade_ame_roa.csv`: efeitos fixos de trimestre do ano e tendências linear/quadrática.
- `evento_trimestre_eleitoral_roa.csv`: recodificação de eleição geral para o trimestre efetivo, T4.

## Regra

A V13 original deve ser preservada como referência de replicação. Resultados do novo paper devem ser gerados sobre a base canônica derivada por script e identificada por hash.
