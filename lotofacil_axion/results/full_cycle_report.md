# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-10-09T21:11:36.622574-03:00
Histórico: concursos 1 a 3800, 3800 observações, de 2003-09-29 a 2026-10-08.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `c51bbca10dcd04054397ba639cca9ee213cfd1e5a069efabe1e9c15e93d23291`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3300 em 9 blocos.
- Aposta única: média 9.0427, IC95% [8.99939393939394, 9.084242424242424], p contra 9 = 0.0462.
- Repetição do concurso anterior: média 8.9724, p contra 9 = 0.1962.
- Carteira de 10: melhor jogo médio 10.8061.
- Benchmark aleatório diversificado: 10.8846.
- Diferença pareada modelo menos benchmark: -0.0786, IC95% [-0.10711909090909108, -0.05058090909090925], p = 6.498e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3800, `marg_w60_hl30.0_pr100.0`, single 8.900, carteira 10.780, aleatória 10.885.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3801.
- Último concurso observado: 3800.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 03 04 05 08 10 11 12 13 14 15 19 20 24 25.
- Manifesto: `results/prediction_3801_manifest.json`.
- Hash interno: `8670f14ba69c457103216d7ce4f86c2ad295e17d1012d842501edbffc4f15298`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
