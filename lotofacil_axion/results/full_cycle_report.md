# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-09-18T19:44:32.826459-03:00
Histórico: concursos 1 a 3782, 3782 observações, de 2003-09-29 a 2026-09-17.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `a53b5095679d9b73e5dd32a494bb0c41beced440950f3b01939ca049da045a45`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3282 em 9 blocos.
- Aposta única: média 9.0445, IC95% [9.002125228519196, 9.085923217550274], p contra 9 = 0.03869.
- Repetição do concurso anterior: média 8.9704, p contra 9 = 0.1669.
- Carteira de 10: melhor jogo médio 10.8050.
- Benchmark aleatório diversificado: 10.8846.
- Diferença pareada modelo menos benchmark: -0.0796, IC95% [-0.10832419256550897, -0.05198019500304711], p = 4.558e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3782, `marg_w60_hl30.0_pr100.0`, single 8.939, carteira 10.732, aleatória 10.881.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3783.
- Último concurso observado: 3782.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 02 03 04 05 09 11 12 13 14 15 17 21 24 25.
- Manifesto: `results/prediction_3783_manifest.json`.
- Hash interno: `1e8a8f31e18160b6205ed1bc6111c91f97f522a7cce0be4ef9680e08d9acb846`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
