# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-10-31T20:32:36.435279-03:00
Histórico: concursos 1 a 3818, 3818 observações, de 2003-09-29 a 2026-10-30.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `a38ca7a362b517f2d413541fb9b45710c5a4d38a11c80881250711e29f8e09a6`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3318 em 9 blocos.
- Aposta única: média 9.0458, IC95% [9.00481464737794, 9.088306208559374], p contra 9 = 0.03218.
- Repetição do concurso anterior: média 8.9729, p contra 9 = 0.2021.
- Carteira de 10: melhor jogo médio 10.8065.
- Benchmark aleatório diversificado: 10.8845.
- Diferença pareada modelo menos benchmark: -0.0780, IC95% [-0.10611211573236906, -0.05022121760096463], p = 7.059e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3818, `marg_w60_hl30.0_pr100.0`, single 9.008, carteira 10.797, aleatória 10.882.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3819.
- Último concurso observado: 3818.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 03 04 05 06 08 10 11 12 13 15 19 20 23 24 25.
- Manifesto: `results/prediction_3819_manifest.json`.
- Hash interno: `be3f69fbd483092586993440d553128928ed94ff9839b44e45865a59250d1693`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
