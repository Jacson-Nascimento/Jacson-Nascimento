# Dependência de Fornecedores e Compras Públicas

Projeto de pesquisa quantitativa sobre concentração da carteira de fornecedores, recorrência contratual e vulnerabilidade estrutural nas redes brasileiras de contratação pública.

## Pergunta central

Em que medida compradores públicos concentram valor e frequência de contratação em poucos fornecedores, e quanto a estrutura da rede comprador-fornecedor revela exposições que não aparecem nas medidas locais de concentração da carteira?

## Fontes principais

- PNCP: instrumentos, fornecedores, órgãos, unidades, valores, datas e contratações de origem.
- SICONFI/DCA: controles fiscais e contábeis municipais.
- IBGE: população e características econômicas municipais.
- Receita Federal/CNPJ: características cadastrais de fornecedores pessoa jurídica, como enriquecimento posterior.

## Estrutura

- `data/raw/`: amostras e arquivos de referência permitidos para publicação.
- `data/processed/`: bases analíticas minimizadas.
- `scripts/`: coleta, limpeza, diagnóstico e cálculos.
- `docs/`: metodologia, dicionário de variáveis e registros técnicos.
- `results/`: tabelas, métricas e saídas analíticas.
- `paper/`: materiais do artigo.

## Unidade principal de análise

`comprador institucional (CNPJ) × fornecedor × ano`

O município é dimensão territorial e fonte de controles. Categorias administrativas do PNCP são usadas para composição e análises secundárias, não presumidas como mercados econômicos.

## Resultados principais

- `PortfolioHHI`: concentração do valor anual da carteira de fornecedores.
- `PortfolioCR1` e `PortfolioCR4`.
- número efetivo de fornecedores.
- `CountHHI`: concentração da frequência de instrumentos por fornecedor.
- divergência entre concentração monetária e recorrência contratual.
- persistência/Jaccard.
- Degree, Strength e Reach dos fornecedores.
- exposição dos compradores a fornecedores centrais.
- simulações de remoção direcionada e aleatória.

## Compras compartilhadas

O projeto distingue o CNPJ do órgão/entidade do instrumento do CNPJ da contratação de origem. A participação de instrumentos originados por outra entidade será medida por `SharedProcurementShare`, sem presunção de irregularidade.

## Mercado relevante

Os probes de itens do PNCP não forneceram, na amostra testada, taxonomia suficientemente granular para tratar a categoria geral `Compras` como mercado econômico. Por isso, o resultado principal é concentração da **carteira de fornecedores**, não concentração antitruste de mercado. Análises setoriais só serão realizadas quando houver classificação econômica defensável.

## Privacidade

O repositório é público. Bases identificadas publicadas contêm somente fornecedores pessoa jurídica. Registros de pessoa física não terão CPF ou nome republicados. Cópias integrais de pesquisa permanecem em armazenamento privado.

## Regra de interpretação

Concentração, recorrência, persistência e centralidade descrevem dependência e exposição estrutural. Não constituem, isoladamente, evidência de fraude, favorecimento, poder de mercado ou interrupção efetiva de serviços.

## Estado atual

PNCP e SICONFI foram empiricamente validados. A coleta contínua por mês foi iniciada para 2025, antes da construção do painel anual e dos resultados substantivos do artigo.
