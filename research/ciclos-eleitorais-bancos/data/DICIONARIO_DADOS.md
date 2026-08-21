# Dicionário de dados da base analítica

Status: preliminar e auditado contra a dissertação final e as bases históricas disponíveis.

## Identificação

| Campo | Definição |
|---|---|
| `Data` | trimestre da observação, 2000T1 a 2023T4 |
| `Instituição` | nome da instituição bancária |
| `dummy_tp` | 1 para banco público; 0 para privado nacional ou privado com controle estrangeiro |

## Outcomes

| Campo | Definição declarada | Situação de auditoria |
|---|---|---|
| `ROA` | Lucro Líquido / Ativo Total | na V13 arquivística está deslocado por +1; na base canônica será `ROA_arquivistico - 1` |
| `ROA_arquivistico` | não é variável econômica nova; preserva o valor de ROA usado na dissertação | criado apenas na base canônica para rastreabilidade |
| `ROE` | Lucro Líquido / Patrimônio Líquido | coincide com a base histórica nas observações comuns verificadas |

## Variáveis bancárias

| Campo na base | Sigla no texto | Definição informada na dissertação | Observação |
|---|---|---|---|
| `IND_EFICIENCIA` | ieo | Despesas Administrativas / Receitas de Intermediação Financeira | validar rubricas COSIF antes do paper final |
| `Indice_individamento` | iend | Dívida Total / Ativo Total | validar construção a partir das rubricas |
| `Spread Bancário` | spread | (Receitas de Crédito - Despesas de Captação) / Ativo Total | validar sinais e rubricas |
| `Desp_Provisao_At` | dpcdl | Resultado/Despesa de Provisão para Créditos de Difícil Liquidação / Ativo Total | a nomenclatura textual varia; revisar sinal econômico |
| `MCAT` | mcat | margem/resultado de operações de câmbio em relação ao Ativo Total | a fórmula impressa na dissertação está textual e matematicamente ambígua; não usar como mecanismo principal antes da validação |
| `PC` | capat | Captações / Ativo Total | o nome da coluna não explicita a sigla usada no texto |
| `PCC` | ccat | Carteira de Crédito Classificada / Ativo Total | o nome da coluna não explicita a sigla usada no texto |

## Variáveis eleitorais

| Campo | Definição original |
|---|---|
| `dummy_EG` | 1 para todos os trimestres do ano em que ocorre eleição geral; 0 caso contrário |
| `dummy_EM` | 1 para todos os trimestres do ano em que ocorre eleição municipal; 0 caso contrário |

Para o novo artigo, as dummies anuais serão preservadas apenas para replicação. O desenho de event study deve criar indicadores trimestrais com tempo relativo à data efetiva da eleição.

## Variáveis macroeconômicas

| Campo | Definição | Auditoria |
|---|---|---|
| `taxa_selic_` | Selic trimestral | V12/V13 usam composição das taxas mensais da série Bacen 4390: `(1+r1)(1+r2)(1+r3)-1` |
| `Taxa_IPCA` | inflação trimestral | V13 expressa o IPCA em proporção decimal; V12 estava na escala percentual |

## Interações do modelo original

- `dpcdl x dummy_EG`
- `dpcdl x dummy_EM`
- `dpcdl x dummy_tp`
- `iend x dummy_EG`
- `iend x dummy_EM`
- `dummy_tp x dummy_EG`
- `dummy_tp x dummy_EM`
- `dummy_tp x spread`
- `dummy_tp x capat`
- `dummy_tp x ccat`

## Regras para o novo paper

1. Não reutilizar nomes abreviados sem um mapeamento explícito entre coluna, fórmula e rubrica de origem.
2. Não interpretar uma interação como eleitoral se o termo não contém `dummy_EG`, `dummy_EM` ou indicador de tempo relativo à eleição.
3. Preservar a V13 sem alterações para replicação e gerar a base canônica por script.
4. Revalidar MCAT, DPCDL, spread, CAPAT e CCAT diretamente contra os arquivos de origem antes de tratá-los como mecanismos econômicos.
