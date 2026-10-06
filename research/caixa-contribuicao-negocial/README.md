# Distribuição de empregados da CAIXA e contribuição negocial por base sindical

Projeto de pesquisa em andamento para estimar, com dados exclusivamente públicos, a distribuição territorial dos empregados da Caixa Econômica Federal e a ordem de grandeza da contribuição negocial potencial de 2026.

## Status

**Fase atual:** construção e validação da base de dados. O artigo ainda não foi redigido.

A redação será iniciada somente depois de:

1. consolidar os principais denominadores por base sindical;
2. reconciliar fontes conflitantes;
3. concluir análise de sensibilidade;
4. revisar a terminologia para distinguir arrecadação potencial, desconto potencial e receita efetiva.

## Regra fundamental

Este projeto usa somente informações publicamente acessíveis. Dados internos da CAIXA, informações obtidas por acesso funcional, listas internas, consultas corporativas ou conhecimento não demonstrável por fonte pública não podem ser usados como evidência.

A regra completa está em `SPEC.md`.

## Estrutura

```text
caixa-contribuicao-negocial/
├── README.md
├── SPEC.md
├── METHODOLOGY.md
├── RESEARCH_LOG.md
├── data/
│   ├── source_register.csv
│   ├── raw/
│   │   ├── national_totals.csv
│   │   ├── uf_conecef_2017.csv
│   │   ├── base_counts_2026.csv
│   │   ├── bases_unresolved.csv
│   │   └── contribution_rules.csv
│   └── processed/
│       ├── uf_estimate_2026.csv
│       └── base_estimate_2026.csv
├── src/
│   └── estimate.py
└── tests/
    └── test_estimates.py
```

## Evidência

- **A:** quantitativo publicado diretamente para a variável e base analisada.
- **B:** quantitativo reconstruído matematicamente de informação pública suficiente.
- **C:** estimativa baseada em proxy territorial ou estrutura histórica.
- **D:** informação insuficiente. Não recebe estimativa pontual.

## Denominador nacional

O cenário corrente utiliza **84.136 empregados em 30/06/2026**, valor divulgado publicamente por entidades sindicais ao comentar o balanço semestral da CAIXA. Como a fonte usada nesta etapa é secundária, o total está classificado como evidência B até ser substituído ou confirmado por documento primário da CAIXA para a mesma data.

O total oficial de 2025 é **84.394 empregados**, conforme apresentação pública de resultados da CAIXA.

## Proxy estadual

A distribuição estadual parte da tabela do 33º CONECEF, que registra 92.596 empregados como base de representação por UF. O próprio Relatório de Sustentabilidade da CAIXA registra 87.654 empregados no fechamento de 2017. Portanto, os 92.596 não são tratados como estoque oficial de empregados em 31/12/2017.

A tabela do CONECEF é usada somente para obter pesos territoriais históricos. Esses pesos são aplicados ao total nacional de junho de 2026 e reconciliados pelo método de maiores restos, de modo que as 27 estimativas somem exatamente 84.136.

## Contribuição negocial

O cenário principal da remuneração fixa segue os parâmetros publicamente divulgados para o dissídio coletivo da CAIXA em 2026:

- alíquota: 1,5%;
- mínimo por empregado: R$ 63,00;
- máximo por empregado: R$ 310,00;
- sindicato da base: 70%;
- federação: 15%;
- confederação: 10%;
- central: 5%.

Sem uma distribuição pública da base remuneratória individual compatível com a cláusula, este projeto **não usa uma contribuição média pontual**. O resultado principal é um intervalo.

Para 84.136 empregados, somente a parcela ligada à remuneração fixa implica, antes de oposições:

- contribuição bruta mínima teórica: **R$ 5.300.568,00**;
- contribuição bruta máxima teórica: **R$ 26.082.160,00**;
- parcela de 70% dos sindicatos: **R$ 3.710.397,60 a R$ 18.257.512,00**.

Esses valores são limites normativos teóricos, não previsão de arrecadação e muito menos receita efetivamente recebida. O resultado real depende da remuneração de cada empregado, oposição ao desconto, devoluções eventualmente praticadas por entidades e demais regras aplicáveis.

## Bases sindicais já documentadas

O arquivo `data/raw/base_counts_2026.csv` registra denominadores públicos localizados para São Paulo/Osasco, SBBA/Bahia, Juiz de Fora, Londrina, Patos de Minas, Criciúma, Campina Grande e Pelotas.

Bases relevantes sem denominador público validado permanecem em `data/raw/bases_unresolved.csv`. Elas não recebem rateio arbitrário.

## Reprodução

A rotina `src/estimate.py` implementa:

1. rateio por maiores restos;
2. reconciliação exata ao total nacional;
3. cálculo dos limites mínimo e máximo da contribuição;
4. cálculo da parcela de 70% destinada ao sindicato.

Os testes estão em `tests/test_estimates.py`.

## Interpretação correta

Evitar expressões como "o sindicato arrecadará" quando o dado representa apenas exposição potencial. Preferir:

- "intervalo potencial sob os parâmetros normativos";
- "valor máximo teórico antes de oposições";
- "estimativa baseada em proxy territorial";
- "denominador público da assembleia".

A metodologia detalhada está em `METHODOLOGY.md`.
