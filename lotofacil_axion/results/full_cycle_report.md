# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-10-21T20:33:40.581625-03:00
Histórico: concursos 1 a 3809, 3809 observações, de 2003-09-29 a 2026-10-20.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `e62e81637bd0ff779b027e9113621d5115d2059058dde7543b6f91c194485869`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3309 em 9 blocos.
- Aposta única: média 9.0441, IC95% [9.00271985494107, 9.08582653369598], p contra 9 = 0.03932.
- Repetição do concurso anterior: média 8.9731, p contra 9 = 0.2068.
- Carteira de 10: melhor jogo médio 10.8072.
- Benchmark aleatório diversificado: 10.8847.
- Diferença pareada modelo menos benchmark: -0.0775, IC95% [-0.10575098216984001, -0.04885947416137823], p = 9.196e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3809, `marg_w60_hl30.0_pr100.0`, single 8.954, carteira 10.817, aleatória 10.887.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3810.
- Último concurso observado: 3809.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 03 04 05 07 08 10 11 12 13 15 19 20 24 25.
- Manifesto: `results/prediction_3810_manifest.json`.
- Hash interno: `4e2b5c3e69f1854fed073172510c52d10cc4ccb8cc6f6939cea8f6ffbc6eb6a3`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
