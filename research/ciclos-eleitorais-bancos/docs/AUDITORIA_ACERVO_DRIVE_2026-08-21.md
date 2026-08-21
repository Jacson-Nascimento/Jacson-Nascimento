# Auditoria do acervo da dissertação

Data: 21/08/2026

Autor: Jacson Cruz do Nascimento

## 1. Escopo

Esta nota registra a auditoria do material localizado no Google Drive para a dissertação sobre eleições e desempenho bancário. O objetivo é identificar a cadeia de dados e scripts efetivamente utilizada, reproduzir as tabelas finais e preparar um pipeline reprodutível para artigo científico.

## 2. Versão textual de referência

A versão textual de referência é:

`Dissertação - Impacto das Eleições Presidenciais na Lucratividade de Bancos Brasileiros - Versão Final - 2024-09-21.pdf`

Versões anteriores são tratadas como histórico e evidência de proveniência.

## 3. Bases finais auditadas

| Arquivo | Linhas | Bancos | Trimestres | SHA-256 |
|---|---:|---:|---:|---|
| `dataset_290624_11.csv` | 3.072 | 32 | 96 | `8f2a06bae81e80a58fe1acadc38fe7982594ca3a489e22cd64ef4bb40d4388e2` |
| `dataset_290624_12.csv` | 3.072 | 32 | 96 | `3b45c30d2352f04c3b1c8b070d91678f41964f95e683e615fcf72449f7220a5d` |
| `dataset_290624_13.csv` | 3.072 | 32 | 96 | `058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f` |

As três bases têm as mesmas chaves `Instituição` e `Data`, sem duplicidades banco-data e sem valores ausentes.

## 4. Proveniência das diferenças

### V11 -> V12

Apenas `taxa_selic_` muda. A V12/V13 usa Selic trimestral composta a partir da série mensal Bacen 4390:

```text
TaxaTrimestre = (1 + r1) * (1 + r2) * (1 + r3) - 1
```

A transformação foi reconciliada com `TB_selic_4390_acum_mes_trim.xlsx`.

### V12 -> V13

Apenas `Taxa_IPCA` muda. A V13 expressa IPCA em proporção decimal.

## 5. Base efetivamente usada nas tabelas finais

A reprodução fechou a proveniência: a **V13** é a base arquivística compatível com as tabelas finais.

Embora os scripts estáticos arquivados apontem para V11, os resultados publicados, especialmente o coeficiente do IPCA, estão na escala produzida pela V13.

A matriz completa está em:

`results/auditoria/reconciliacao_bases_tabelas.csv`

## 6. Reprodução econométrica

Foi implementada reprodução independente equivalente à lógica do `plm`:

- transformação within por banco;
- OLS sobre variáveis demeaned;
- covariância cluster por banco;
- ajuste HC1 `N/(N-k)`;
- graus de liberdade `N - bancos - k`.

Script:

`scripts/auditoria/02_reproduzir_modelos.py`

A V13 reproduz, até o arredondamento impresso, os Apêndices D, E, F, G, I, J e K.

## 7. Apêndice H duplicado

O Apêndice H está rotulado como `Modelo Estático - ROA - 2012-2023`, mas contém exatamente o mesmo output de ROE do Apêndice I.

O verdadeiro ROA estático 2012-2023 foi reconstruído em:

`results/auditoria/modelo_estatico_roa_2012_2023_corrigido.csv`

Trata-se de erro de montagem/transcrição documental.

## 8. Contagem incorreta nos modelos dinâmicos

Os scripts calculam `N` antes da criação da defasagem e do `na.omit()`.

Amostras efetivas:

- 2000-2023: 3.040 observações, não 3.072;
- 2012-2023: 1.504 observações, não 1.536.

Os graus de liberdade publicados confirmam essas contagens.

## 9. ROA deslocado por +1

A comparação com `dataset_2024_3.csv` mostrou, em 2.852 observações banco-trimestre comuns:

```text
ROA_V13 = 1 + ROA_antigo
```

com diferença numérica máxima próxima de `4,44e-16`.

Para ROE:

```text
ROE_V13 = ROE_antigo
```

A dissertação define ROA como `Lucro Líquido / Ativo Total`. Portanto, a base canônica do artigo deve usar:

```text
ROA = ROA_arquivistico - 1
```

O deslocamento constante não altera os coeficientes within reproduzidos, mas altera estatísticas descritivas de nível e a interpretação literal do indicador.

## 10. Coeficiente eleitoral e efeito marginal

O modelo original inclui `dummy_EG` e interações de `dummy_EG` com DPCDL, endividamento e tipo de controle.

Assim, `beta_EG` é um coeficiente condicional, não o efeito médio da eleição.

### Estático

- `beta_EG = 0,028378`, p `0,0337`;
- efeito marginal médio = `0,001069`, p `0,1135`.

### Dinâmico

- `beta_EG = 0,022566`, p `0,0340`;
- efeito marginal médio = `0,000952`, p `0,1349`.

O coeficiente principal corresponde ao ponto DPCDL=0, endividamento=0 e banco privado. O endividamento observado não atinge zero, então esse ponto de referência não representa uma observação típica.

Documento específico:

`docs/ACHADO_EFEITO_MARGINAL_ELEICAO_2026-08-21.md`

## 11. Notação científica

`2,837812e-02` equivale a `0,02837812`, não a `2,8378`.

Trechos narrativos que convertem o primeiro valor no segundo incorrem em erro de escala por fator 100.

## 12. Interpretação das interações

A interação `dpcdl:dtc` representa:

`Despesa de Provisão sobre Ativos x Tipo de Controle`

Ela não contém dummy eleitoral. Interpretações que acrescentam `durante períodos eleitorais` não são sustentadas por esse termo econométrico.

## 13. Robustez temporal inicial

O coeficiente condicional de `dummy_EG` permanece relativamente estável sob:

- diferentes matrizes de covariância;
- retirada individual de cada eleição geral;
- efeitos fixos de trimestre do ano;
- tendências temporal linear e quadrática.

Entretanto, o efeito marginal médio permanece próximo de `0,001` e não significativo a 5%.

O ROA apresenta sazonalidade positiva de T4 também em anos não eleitorais. Quando a eleição é marcada apenas no trimestre efetivo e as interações eleitorais são retiradas, o resultado não é significativo nos testes iniciais.

Documento:

`docs/ROBUSTEZ_TEMPORAL_PRELIMINAR_2026-08-21.md`

## 14. Decisão de versionamento

### V13 arquivística

Preservar sem modificações para reprodução histórica.

SHA-256:

`058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f`

### Base canônica limpa

Derivar por script, inicialmente com:

- `ROA = ROA_arquivistico - 1`;
- Selic trimestral composta mantida;
- IPCA em proporção decimal mantido;
- coluna `ROA_arquivistico` preservada;
- validações de domínio e hashes registradas.

Script:

`scripts/preparacao/01_construir_base_canonica.py`

## 15. Consequência para o artigo

A prioridade é distinguir:

1. coeficiente condicional de eleição;
2. efeito marginal médio;
3. timing do evento;
4. sazonalidade;
5. robustez da inferência temporal.

Título provisório preferencial:

**Ciclos Eleitorais e Rentabilidade Bancária no Brasil: Uma Reavaliação dos Efeitos, do Timing e da Inferência**

## 16. Próximas entregas

1. gerar e manifestar a base canônica limpa;
2. validar fórmulas de DPCDL, MCAT, spread, CAPAT e CCAT contra fontes de origem;
3. construir event study `k=-4...+4`;
4. comparar análise em painel com série setorial agregada;
5. aplicar placebos temporais pré-especificados;
6. decidir a narrativa final do artigo somente após esses testes.
