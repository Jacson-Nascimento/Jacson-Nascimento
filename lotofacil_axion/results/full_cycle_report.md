# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-11-11T22:59:13.334748-03:00
Histórico: concursos 1 a 3827, 3827 observações, de 2003-09-29 a 2026-11-11.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `58e50c5558387cafff41b54db7fd318876ab1688983e7b1728ffbbc096007a4b`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3327 em 9 blocos.
- Aposta única: média 9.0451, IC95% [9.00299819657349, 9.08746618575293], p contra 9 = 0.03509.
- Repetição do concurso anterior: média 8.9714, p contra 9 = 0.1788.
- Carteira de 10: melhor jogo médio 10.8058.
- Benchmark aleatório diversificado: 10.8847.
- Diferença pareada modelo menos benchmark: -0.0788, IC95% [-0.1075939284640819, -0.050916140667267976], p = 4.838e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3827, `marg_w60_hl30.0_pr100.0`, single 8.992, carteira 10.780, aleatória 10.886.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3828.
- Último concurso observado: 3827.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 03 05 06 08 10 11 12 13 15 19 20 23 24 25.
- Manifesto: `results/prediction_3828_manifest.json`.
- Hash interno: `8ee770e748ce881bd04b0ce58a215e7cb8948c913733e3247c1165708b4c67e0`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
