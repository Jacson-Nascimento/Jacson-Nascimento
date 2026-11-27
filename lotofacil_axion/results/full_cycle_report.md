# Modelo Axion Lotofácil 0.3, ciclo integral

Execução: 2026-11-27T00:02:49.047629-03:00
Histórico: concursos 1 a 3839, 3839 observações, de 2003-09-29 a 2026-11-26.
Fonte principal: https://gist.githubusercontent.com/jovakf1/0efbe4f3cfde6d4308ade85178f23e1a/raw/lotofacil.txt.
SHA-256 da fonte bruta: `45a4b656e63b65a22bf11bfac6d38a42a5c6e7828e04e0bdfcf60a8d25cc5251`.

## Desenho da validação

- Validação aninhada temporal, com treino expansivo e blocos externos de até 400 concursos.
- Cada configuração foi selecionada somente em uma janela interna anterior ao bloco externo.
- Carteiras externas com 10 jogos, distância Johnson mínima de cinco substituições.
- Benchmark pareado: média de 25 carteiras aleatórias diversificadas por concurso.

## Resultados agregados fora da amostra

- Previsões externas: 3339 em 9 blocos.
- Aposta única: média 9.0443, IC95% [9.000598981731057, 9.087151841868822], p contra 9 = 0.03798.
- Repetição do concurso anterior: média 8.9712, p contra 9 = 0.1752.
- Carteira de 10: melhor jogo médio 10.8056.
- Benchmark aleatório diversificado: 10.8846.
- Diferença pareada modelo menos benchmark: -0.0790, IC95% [-0.10778137166816427, -0.05084037136867344], p = 4.117e-08.

## Configurações selecionadas por bloco

- Bloco 1: concursos 501 a 900, `marg_w500_hl250.0_pr100.0`, single 8.995, carteira 10.780, aleatória 10.892.
- Bloco 2: concursos 901 a 1300, `marg_w500_hl250.0_pr100.0`, single 9.043, carteira 10.723, aleatória 10.875.
- Bloco 3: concursos 1301 a 1700, `blend_w120_lw0.25`, single 9.092, carteira 10.805, aleatória 10.888.
- Bloco 4: concursos 1701 a 2100, `blend_w120_lw0.75`, single 9.015, carteira 10.830, aleatória 10.887.
- Bloco 5: concursos 2101 a 2500, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.770, aleatória 10.877.
- Bloco 6: concursos 2501 a 2900, `marg_w500_hlNone_pr100.0`, single 9.070, carteira 10.870, aleatória 10.886.
- Bloco 7: concursos 2901 a 3300, `marg_w500_hlNone_pr100.0`, single 9.107, carteira 10.860, aleatória 10.884.
- Bloco 8: concursos 3301 a 3700, `marg_w500_hlNone_pr100.0`, single 8.985, carteira 10.818, aleatória 10.888.
- Bloco 9: concursos 3701 a 3839, `marg_w60_hl30.0_pr100.0`, single 8.978, carteira 10.777, aleatória 10.885.

## Regimes e mudanças detectadas

- Quebras de frequência candidatas, índices: [].
- Quebras de cadência candidatas, índices: [160, 710, 2000].
- Essas quebras são diagnósticas. Não foram usadas para olhar o futuro durante a seleção aninhada.

## Previsão prospectiva registrada

- Próximo concurso: 3840.
- Último concurso observado: 3839.
- Configuração: `marg_w30_hlNone_pr100.0`.
- Jogo de maior escore: 03 05 11 12 13 15 16 17 18 19 20 22 23 24 25.
- Manifesto: `results/prediction_3840_manifest.json`.
- Hash interno: `ea4e8d58cc1af32e1f56be7561a7ecaab7b11367ddcd3f86d1b05c5700ca1766`.

## Conclusão metodológica

Uma vantagem só deve ser reconhecida quando a diferença fora da amostra superar o benchmark, possuir intervalo de confiança positivo e persistir entre blocos temporais. A seleção de uma carteira não constitui garantia de premiação.
