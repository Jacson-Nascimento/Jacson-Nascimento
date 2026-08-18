# Dicionário de Variáveis

## Chaves e identificação

| Variável | Fonte | Definição | Uso |
|---|---|---|---|
| `numeroControlePNCP` | PNCP | Identificador do instrumento contratual | chave primária do instrumento |
| `numeroControlePncpCompra` | PNCP | Identificador da contratação de origem | relacionamento contratação-instrumentos |
| `numeroRetificacao` | PNCP | versão/retificação observada | controle de versões |
| `municipio_ibge` | PNCP/IBGE | código IBGE da unidade compradora | integração municipal |
| `fornecedor_id` | PNCP | CNPJ/CPF/identificador do fornecedor | nó fornecedor, armazenado como texto |
| `categoria` | PNCP | categoria do processo/contratação | definição inicial de mercado |
| `ano_assinatura` | PNCP | ano derivado da data de assinatura | período econômico |

## Valores contratuais

| Variável | Fonte | Definição | Regra inicial |
|---|---|---|---|
| `valorInicial` | PNCP | valor no instrumento na celebração | medida principal inicial |
| `valorGlobal` | PNCP | valor global informado | teste de robustez |
| `valorAcumulado` | PNCP | valor acumulado informado | análise separada, não substituir automaticamente valor inicial |

## Qualidade e cobertura

| Variável | Fórmula/definição |
|---|---|
| `lag_publicacao_dias` | dataPublicacaoPncp - dataAssinatura |
| `coverage_meses` | número de meses com registros válidos / 12 |
| `coverage_trimestres` | número de trimestres com registros válidos / 4 |
| `n_instrumentos_compra` | quantidade de instrumentos associados à mesma contratação |

## Concentração

Se `V_bsct` é o valor agregado entre comprador b, fornecedor s, categoria c e ano t, e `q_bsct = V_bsct / V_bct`:

- `HHI_bct = Σ_s q_bsct²`
- `CR1_bct = max_s(q_bsct)`
- `CR4_bct = Σ Top4(q_bsct)`
- `N_eff_bct = 1 / HHI_bct`
- `Entropia_bct = -Σ_s q_bsct ln(q_bsct)`
- `Entropia_normalizada = Entropia / ln(N_fornecedores)`, para N > 1

## Persistência

- `Jaccard_bct = |S_bct ∩ S_bc,t-1| / |S_bct ∪ S_bc,t-1|`
- `Turnover_bct = 1 - Jaccard_bct`

## Rede de fornecedores

| Variável | Definição |
|---|---|
| `Degree_sct` | número de compradores distintos do fornecedor |
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