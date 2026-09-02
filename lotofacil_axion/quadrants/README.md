# Axion - análise de quadrantes

Autor: **Jacson Cruz do Nascimento**

Este módulo enumera as `3.268.760` combinações possíveis da Lotofácil e cria duas representações independentes:

1. **Mapa espacial**: momentos horizontal e vertical das dezenas no volante 5x5.
2. **Mapa estrutural**: soma das dezenas e quantidade de pares consecutivos.

Os cortes são as medianas calculadas no espaço combinatório completo. Como existe massa sobre os eixos, a probabilidade de referência de cada quadrante é calculada por enumeração exata, sem pressupor 25% por quadrante.

## Validação

O histórico é confrontado com o espaço completo por:

- teste qui-quadrado de aderência;
- dependência serial nos lags 1 a 20;
- correção Benjamini-Hochberg conjunta para 40 testes;
- previsão walk-forward marginal e por transição, ambas suavizadas para a distribuição combinatória;
- log loss e Brier score contra o baseline estático;
- intervalo por bootstrap em blocos.

Um quadrante só pode ser tratado como sinal preditivo quando melhora simultaneamente log loss e Brier score fora da amostra, com o limite superior dos dois intervalos de 95% abaixo de zero.

## Execução

```bash
python lotofacil_axion/quadrants/quadrant_analysis.py \
  --history lotofacil_axion/data/lotofacil_history.csv \
  --output-dir quadrants_output \
  --write-map
```

Resultados prospectivos, mapas completos e arquivos intermediários não devem ser adicionados ao repositório público. O repositório deve manter somente código, método e documentação agregada compatíveis com `PUBLIC_DATA_POLICY.md`.

## Limite interpretativo

Quadrantes podem revelar concentração, desvio operacional ou dependência temporal. Eles não tornam uma combinação específica mais provável em um sorteio justo. Quando não houver validação fora da amostra, sua aplicação adequada é diversificação de carteira e auditoria de aleatoriedade, não previsão.
