# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-11-18T22:59:03.158734-03:00
Histórico: concursos 1 a 3833, 3833 observações, de 2003-09-29 a 2026-11-18.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `3572ab190e38fbd37019513d3cdda82c620eceec3c11eb07db41e9d9f2ebd019`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3333 em 9 blocos.
- Aposta única: média 9.0447, IC95% [9.002700270027002, 9.086108610861086], p contra 9 = 0.03642.
- Repetição do concurso anterior: média 8.9703, p contra 9 = 0.1616.
- Carteira de 10: melhor jogo médio 10.8059.
- Benchmark aleatório diversificado: 10.8847.
- Diferença pareada modelo menos benchmark: -0.0788, IC95% [-0.10691959195919608, -0.05122112211221138], p = 4.711e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3833, `marg_w60_hl30.0_pr100.0`, single 8.985, carteira 10.782, aleatória 10.885.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3834.
- Último concurso observado: 3833.
- Configuração: `marg_w30_hlNone_pr100.0`.
- Jogo de maior escore: 01 05 06 11 13 15 16 17 18 19 20 22 23 24 25.
- Manifesto: `results/prediction_3834_manifest.json`.
- Hash interno: `a4c86028c37d5e784b0040f7ae8d230a1ad309df9c1f5a4c6b6178d2cd6067a8`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
