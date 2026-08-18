# Dicionário de Variáveis

## Chaves e identificação

| Variável | Fonte | Definição | Uso |
|---|---|---|---|
| `numeroControlePNCP` | PNCP | identificador do instrumento | chave primária |
| `numeroControlePncpCompra` | PNCP | contratação de origem | vínculo contratação-instrumentos |
| `numeroRetificacao` | PNCP | versão ou retificação | controle de versões |
| `orgao_cnpj` | PNCP | CNPJ do órgão/entidade do instrumento | **comprador institucional principal** |
| `orgao_compra_cnpj` | PNCP/derivada | CNPJ extraído do identificador da contratação de origem | compras compartilhadas |
| `unidade_codigo` | PNCP | código da unidade executora | dimensão operacional |
| `municipio_ibge` | PNCP/IBGE | município da unidade executora | integração territorial |
| `fornecedor_id` | PNCP | CNPJ/CPF/identificador do fornecedor | nó fornecedor, sempre texto |
| `tipo_pessoa` | PNCP | PJ, PF ou PE | filtros e política de publicação |
| `categoria` | PNCP | categoria administrativa do processo | composição e análise secundária |
| `ano_assinatura` | PNCP | ano da assinatura | período econômico |

## Comprador

`buyer_id = orgao_cnpj`

A rede principal é construída como:

`orgao_cnpj × fornecedor × ano`

O município não substitui o comprador. Ele permanece como dimensão territorial e fonte de controles.

Variáveis auxiliares:

- `n_municipios_orgao`: municípios distintos observados para o CNPJ comprador;
- `orgao_multimunicipal = 1[n_municipios_orgao > 1]`;
- `n_orgaos_municipio`: CNPJs compradores distintos observados no município.

## Compras compartilhadas

`origem_externa = 1[orgao_cnpj != orgao_compra_cnpj]`

`SharedProcurementShare_bt = valor de instrumentos com origem_externa / valor total da carteira do comprador`

A variável indica contratação originada por outra entidade e não constitui sinal de irregularidade por definição.

## Valores contratuais

| Variável | Fonte | Definição | Regra inicial |
|---|---|---|---|
| `valorInicial` | PNCP | valor na celebração | medida principal após classificação do instrumento |
| `valorGlobal` | PNCP | valor global informado | robustez |
| `valorAcumulado` | PNCP | valor acumulado informado | análise separada |

## Qualidade e cobertura

| Variável | Fórmula/definição |
|---|---|
| `lag_publicacao_dias` | dataPublicacaoPncp - dataAssinatura |
| `flag_lag_negativo` | 1 quando data de assinatura é posterior à publicação |
| `coverage_meses` | meses com registros válidos / 12, após coleta integral |
| `coverage_trimestres` | trimestres com registros válidos / 4 |
| `presenca_sentinela` | presença nas datas de teste, apenas diagnóstico |
| `n_instrumentos_compra` | instrumentos associados à mesma contratação |
| `n_fornecedores_compra` | fornecedores associados à mesma contratação |

## Relação comprador-fornecedor anual

`V_bst = soma do valor elegível dos instrumentos do comprador b com fornecedor s no ano t`

`V_bt = soma_s V_bst`

`q_bst = V_bst / V_bt`

## Concentração da carteira por valor

| Variável | Definição |
|---|---|
| `PortfolioHHI_bt` | Σ_s q_bst² |
| `PortfolioCR1_bt` | maior participação financeira de fornecedor |
| `PortfolioCR4_bt` | soma das quatro maiores participações |
| `PortfolioNeff_bt` | 1 / PortfolioHHI |
| `PortfolioEntropy_bt` | entropia normalizada das participações financeiras |

Essas variáveis medem concentração da carteira de fornecedores, não concentração antitruste de mercado.

## Concentração por frequência

`n_bst = número de instrumentos elegíveis do comprador b com fornecedor s`

`p_bst = n_bst / soma_s n_bst`

`CountHHI_bt = Σ_s p_bst²`

A comparação `PortfolioHHI × CountHHI` distingue concentração monetária de recorrência contratual.

## Composição por categoria administrativa

`V_bct = valor da categoria c na carteira do comprador b`

`w_bct = V_bct / V_bt`

`CategoryMixHHI_bt = Σ_c w_bct²`

Também poderá ser calculado `PortfolioHHI_bct` como concentração da carteira de fornecedores dentro de uma categoria administrativa, sem interpretação automática de mercado econômico.

## Persistência

- `Jaccard_bt = |S_bt ∩ S_b,t-1| / |S_bt ∪ S_b,t-1|`
- `Turnover_bt = 1 - Jaccard_bt`
- persistência do fornecedor dominante;
- variação anual de `PortfolioHHI`, `CR1` e `CountHHI`.

## Rede de fornecedores

| Variável | Definição |
|---|---|
| `Degree_st` | compradores institucionais distintos do fornecedor |
| `Strength_st` | valor total das relações do fornecedor |
| `Reach_st` | Degree / número de compradores observados no ano |
| `SystemShare_st` | participação do fornecedor no valor total da rede observada |
| `pct_degree_st` | percentil anual de Degree |
| `pct_strength_st` | percentil anual de Strength |
| `Edegree_bt` | Σ_s q_bst × pct_degree_st |
| `Estrength_bt` | Σ_s q_bst × pct_strength_st |

## Dependência bilateral

`r_bst = V_bst / soma_b V_bst`

`BuyerHHI_st = Σ_b r_bst²`

## Choques estruturais

`Loss_bt(R) = Σ_{s em R} q_bst`

`Severe_t(R,tau) = proporção de compradores com Loss >= tau`

## Controles externos previstos

- população, IBGE;
- PIB e PIB per capita defasados, IBGE;
- despesa empenhada, liquidada e paga, SICONFI/DCA;
- composição da despesa, SICONFI;
- UF e região;
- características cadastrais de fornecedores PJ, Receita Federal/CNPJ.

`ProcurementIntensity_it = ValorContratadoPNCP_it / DespesaEmpenhadaSICONFI_it`

Essa razão é controle de escala, não identidade contábil.

## Taxonomia de itens

Nos probes realizados, `itemCategoriaNome` esteve preenchido mas apresentou `Não se aplica` nos itens de 2025 testados; NCM/NBS e códigos de catálogo tiveram cobertura nula. Portanto, esses campos não serão usados como mercado relevante sem nova validação de cobertura e conteúdo.

## Privacidade

O GitHub público não republicará CPF ou nome associado a fornecedor PF. Bases públicas identificadas serão, nesta etapa, restritas a fornecedores PJ. PF e PE poderão participar de análises de robustez privadas e resultados agregados.

## Observação metodológica

Indicadores de concentração, recorrência e rede descrevem dependência e exposição estrutural. Não constituem prova de irregularidade, favorecimento, poder de mercado ou interrupção efetiva do fornecimento.
