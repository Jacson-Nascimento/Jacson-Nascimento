# Dicionário de Variáveis

## Chaves e identificação

| Variável | Fonte | Definição | Uso |
|---|---|---|---|
| `numeroControlePNCP` | PNCP | Identificador do instrumento contratual | chave primária do instrumento |
| `numeroControlePncpCompra` | PNCP | Identificador da contratação de origem | relacionamento contratação-instrumentos |
| `numeroRetificacao` | PNCP | versão/retificação observada | controle de versões |
| `orgao_cnpj` | PNCP | CNPJ do órgão/entidade do contrato ou empenho | **identificador principal do comprador institucional** |
| `orgao_razao_social` | PNCP | razão social do órgão/entidade | identificação do comprador |
| `unidade_codigo` | PNCP | código da unidade executora | identificação da unidade operacional |
| `unidade_nome` | PNCP | nome da unidade executora | identificação da unidade operacional |
| `municipio_ibge` | PNCP/IBGE | código IBGE da localidade da unidade executora | integração territorial, não substitui o CNPJ do comprador |
| `fornecedor_id` | PNCP | CNPJ/CPF/identificador do fornecedor | nó fornecedor, armazenado como texto |
| `categoria` | PNCP | categoria do processo/contratação | definição inicial de mercado, sujeita a refinamento por item |
| `ano_assinatura` | PNCP | ano derivado da data de assinatura | período econômico |

## Definição do comprador

O PNCP distingue o órgão/entidade contratante da unidade executora. Portanto, o comprador da rede não será definido automaticamente pelo município da unidade.

### Análise institucional principal

`buyer_id = orgao_cnpj`

A rede institucional será construída como:

`orgao_cnpj × fornecedor × categoria × ano`

### Análise municipal

Será restrita, em princípio, aos órgãos municipais que possam ser associados de forma não ambígua a um único município no período analisado.

Definiremos:

`n_municipios_orgao = número de municipios_ibge distintos observados para orgao_cnpj`

`orgao_multimunicipal = 1[n_municipios_orgao > 1]`

Órgãos multi-municipais, especialmente consórcios públicos e estruturas compartilhadas, serão analisados separadamente ou excluídos da amostra municipal principal, salvo se houver regra auditável para alocar os instrumentos aos municípios participantes.

Essa regra evita atribuir automaticamente a um município uma contratação cujo proprietário institucional é um consórcio ou outra entidade compartilhada.

## Valores contratuais

| Variável | Fonte | Definição | Regra inicial |
|---|---|---|---|
| `valorInicial` | PNCP | valor no instrumento na celebração | medida principal inicial, após classificação do tipo de instrumento |
| `valorGlobal` | PNCP | valor global informado | teste de robustez |
| `valorAcumulado` | PNCP | valor acumulado informado | análise separada, não substituir automaticamente valor inicial |

## Qualidade e cobertura

| Variável | Fórmula/definição |
|---|---|
| `lag_publicacao_dias` | dataPublicacaoPncp - dataAssinatura |
| `coverage_meses` | número de meses com registros válidos / 12, calculado somente após coleta integral dos meses |
| `coverage_trimestres` | número de trimestres com registros válidos / 4, calculado somente após coleta integral |
| `presenca_sentinela` | número de datas sentinela em que o ente apareceu / número de datas sentinela |
| `n_instrumentos_compra` | quantidade de instrumentos associados à mesma contratação |
| `n_fornecedores_compra` | fornecedores distintos associados à mesma contratação |
| `n_municipios_orgao` | municípios distintos observados nas unidades executoras de um mesmo CNPJ comprador |

`presenca_sentinela` é um diagnóstico de frequência de publicação. Não será tratada como medida de completude anual do município.

## Concentração

Na análise institucional, se `V_bsct` é o valor agregado entre comprador institucional b, fornecedor s, categoria c e ano t, e `q_bsct = V_bsct / V_bct`:

- `HHI_bct = Σ_s q_bsct²`
- `CR1_bct = max_s(q_bsct)`
- `CR4_bct = Σ Top4(q_bsct)`
- `N_eff_bct = 1 / HHI_bct`
- `Entropia_bct = -Σ_s q_bsct ln(q_bsct)`
- `Entropia_normalizada = Entropia / ln(N_fornecedores)`, para N > 1

A versão territorial será estimada apenas na amostra municipal cuja atribuição comprador-município seja não ambígua.

## Persistência

- `Jaccard_bct = |S_bct ∩ S_bc,t-1| / |S_bct ∪ S_bc,t-1|`
- `Turnover_bct = 1 - Jaccard_bct`

## Rede de fornecedores

| Variável | Definição |
|---|---|
| `Degree_sct` | número de compradores institucionais distintos do fornecedor |
| `Strength_sct` | valor total das relações do fornecedor |
| `Reach_sct` | Degree / número de compradores na categoria-ano |
| `pct_degree_sct` | percentil de Degree na categoria-ano |
| `pct_strength_sct` | percentil de Strength na categoria-ano |
| `E_degree_bct` | Σ_s q_bsct × pct_degree_sct |
| `E_strength_bct` | Σ_s q_bsct × pct_strength_sct |

## Controles externos previstos

- população municipal, IBGE;
- PIB per capita defasado, IBGE;
- despesa total, SICONFI/FINBRA;
- receita total, SICONFI/FINBRA;
- despesas correntes, SICONFI/FINBRA;
- investimentos, SICONFI/FINBRA;
- data de abertura, localização, CNAE e outras características cadastrais, Receita/CNPJ, com cautela temporal.

## Observação metodológica

Indicadores de concentração e rede são sinais de exposição estrutural. Não constituem prova de irregularidade, favorecimento ou interrupção efetiva do fornecimento.
