# Dependência de Fornecedores e Compras Públicas

Projeto de pesquisa sobre concentração econômica, persistência das relações comprador-fornecedor e vulnerabilidade estrutural nas compras públicas brasileiras.

## Pergunta central

Em que medida as compras públicas municipais apresentam concentração e dependência estrutural de fornecedores, e quanto a análise de redes acrescenta aos indicadores convencionais de concentração?

## Fontes principais

- PNCP: contratos, fornecedores, órgãos, categorias, valores e datas.
- SICONFI/FINBRA: controles fiscais e contábeis municipais.
- IBGE: população e características econômicas municipais.
- Receita Federal/CNPJ: características cadastrais dos fornecedores, como enriquecimento.

## Estrutura

- `data/raw/`: amostras e bases brutas coletadas.
- `data/processed/`: bases tratadas para análise.
- `scripts/`: coleta, limpeza, diagnóstico e cálculos.
- `docs/`: metodologia, dicionário de variáveis e registros técnicos.
- `results/`: tabelas, métricas e saídas analíticas.
- `paper/`: materiais do artigo.

## Unidade principal de análise

`município × categoria de contratação × ano`

A rede é bipartida entre compradores e fornecedores, com peso igual ao valor agregado contratado em cada relação.

## Métricas previstas

- HHI
- CR1 e CR4
- Número efetivo de fornecedores
- Entropia
- Persistência/Jaccard
- Degree, Strength e Reach dos fornecedores
- Exposição a fornecedores centrais
- Simulações de remoção direcionada e aleatória

## Regra de interpretação

As métricas de concentração e rede são sinais para priorização de análise. Não constituem, isoladamente, evidência de fraude, favorecimento ou interrupção efetiva de serviços.

## Estado atual

Fase de diagnóstico das bases e validação do pipeline de coleta do PNCP.