# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-10-05T22:24:38.237314-03:00
Histórico: concursos 1 a 3797, 3797 observações, de 2003-09-29 a 2026-10-05.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `610d8226aecd7c965748452658b7a30c8f90dae4f8f318fe85e01b901012cb55`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3297 em 9 blocos.
- Aposta única: média 9.0428, IC95% [9.001819836214741, 9.084319077949651], p contra 9 = 0.0462.
- Repetição do concurso anterior: média 8.9709, p contra 9 = 0.1723.
- Carteira de 10: melhor jogo médio 10.8053.
- Benchmark aleatório diversificado: 10.8846.
- Diferença pareada modelo menos benchmark: -0.0793, IC95% [-0.10788019411586305, -0.05115923566879002], p = 4.858e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3797, `marg_w60_hl30.0_pr100.0`, single 8.897, carteira 10.753, aleatória 10.882.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3798.
- Último concurso observado: 3797.
- Configuração: `blend_w60_lw0.5`.
- Jogo de maior escore: 01 03 04 05 08 10 11 12 13 14 15 19 20 24 25.
- Manifesto: `results/prediction_3798_manifest.json`.
- Hash interno: `6416e8f4fb297a82a1d63f07753b3cd16bed80d885a1c0954153b2eead18e976`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
