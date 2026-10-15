# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-10-15T20:12:54.278573-03:00
Histórico: concursos 1 a 3804, 3804 observações, de 2003-09-29 a 2026-10-14.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `d1a8753f65f1d623ba7dd9e9936b75b461ab125a8bba136d3953c19632b8e788`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3304 em 9 blocos.
- Aposta única: média 9.0442, IC95% [9.003026634382566, 9.08595641646489], p contra 9 = 0.03916.
- Repetição do concurso anterior: média 8.9731, p contra 9 = 0.2064.
- Carteira de 10: melhor jogo médio 10.8066.
- Benchmark aleatório diversificado: 10.8847.
- Diferença pareada modelo menos benchmark: -0.0781, IC95% [-0.1059570217917677, -0.04921277239709461], p = 7.501e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3804, `marg_w60_hl30.0_pr100.0`, single 8.952, carteira 10.798, aleatória 10.888.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3805.
- Último concurso observado: 3804.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 03 04 05 07 08 11 12 13 14 15 19 20 24 25.
- Manifesto: `results/prediction_3805_manifest.json`.
- Hash interno: `c1635b73006998fe974b2c357beaca1b4420bbc2e41474164fefbdf06138c16e`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
