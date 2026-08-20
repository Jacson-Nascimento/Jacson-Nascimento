# Dependência de Fornecedores e Compras Públicas

Projeto de pesquisa quantitativa sobre concentração da carteira de fornecedores, recorrência contratual e vulnerabilidade estrutural nas redes brasileiras de contratação pública municipal.

## Pergunta central do projeto

Em que medida compradores públicos municipais concentram valor e frequência de contratação em poucos fornecedores, e quanto a estrutura da rede comprador-fornecedor revela exposições que não aparecem nas medidas locais de concentração da carteira?

## Estratégia de publicação

O projeto passa a ter dois papers complementares, com perguntas e contribuições distintas.

### Paper 1: janeiro a junho de 2025

**Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição em Rede e Vulnerabilidade a Choques**

Objetivo: propor e validar inicialmente o framework de mensuração combinando concentração local da carteira, centralidade global de fornecedores, exposição estrutural, discordância entre HHI e exposição, stress tests e persistência longitudinal.

Arquivo de trabalho: `paper/PAPER1_JAN_JUN_2025_V1.md`.

### Paper 2: ano de 2025 completo

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

Objetivo: testar a estabilidade temporal do framework ao longo de janeiro-dezembro, decompor efeito de composição, avaliar estabilidade dos stress tests e dos modelos associativos e medir a sensibilidade à captura tardia de instrumentos assinados em 2025 e publicados em 2026.

Arquivo de trabalho: `paper/PAPER2_ANUAL_2025_V1.md`.

O Paper 2 deve citar o Paper 1 e evitar repetição integral de texto, tabelas e contribuição, preservando apenas as definições matemáticas indispensáveis.

## Fontes principais

- PNCP: instrumentos, fornecedores, órgãos, unidades, valores, datas e contratações de origem.
- SICONFI/DCA: controles fiscais e contábeis municipais.
- IBGE: população e características econômicas municipais.
- Receita Federal/CNPJ: características cadastrais de fornecedores pessoa jurídica, como enriquecimento posterior.

## Estrutura

- `data/raw/`: amostras e arquivos de referência permitidos para publicação.
- `data/processed/`: bases analíticas minimizadas.
- `scripts/`: coleta, limpeza, diagnóstico, cálculos e robustezes.
- `docs/`: metodologia, dicionário de variáveis e registros técnicos.
- `results/`: tabelas, métricas e saídas analíticas.
- `paper/`: materiais dos dois artigos.

## Unidade principal de análise

`comprador institucional (CNPJ) × fornecedor × ano`

O município é dimensão territorial e fonte de controles. Categorias administrativas do PNCP são usadas para composição e análises secundárias, não presumidas como mercados econômicos.

O escopo empírico principal atualmente corresponde a órgãos do Poder Executivo municipal observados no PNCP segundo os filtros documentados. Por isso, os títulos e conclusões dos papers utilizam explicitamente o termo **compras públicas municipais**, evitando generalização para todo o universo da contratação pública brasileira.

## Resultados principais

- `PortfolioHHI`: concentração monetária da carteira de fornecedores.
- `PortfolioCR1` e `PortfolioCR4`.
- número efetivo de fornecedores.
- `CountHHI`: concentração da frequência de instrumentos por fornecedor.
- divergência entre concentração monetária e frequência contratual.
- Degree, Strength e Reach dos fornecedores.
- exposição dos compradores a fornecedores centrais.
- discordância entre HHI e exposição estrutural.
- simulações de remoção direcionada e aleatória.
- persistência longitudinal dos rankings e classificações.

## Robustezes estruturais adicionadas

As novas robustezes não alteram a especificação principal congelada. São testes separados para reduzir objeções de mensuração:

- **leave-one-buyer-out** de Strength e Degree, retirando do ranking global a contribuição do próprio comprador;
- gap de percentis entre exposição e HHI;
- resíduo da exposição após HHI normalizado;
- remoções aleatórias ponderadas por Strength;
- stress test com massa sistêmica de Strength aproximadamente equivalente à do ataque direcionado;
- regressões com peso `1/N_m` para equalizar o peso municipal;
- especificação agregada ao município;
- CR1 e CR4 como outcomes alternativos ao HHI normalizado.

Scripts:

- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`

## Compras compartilhadas

O projeto distingue o CNPJ do órgão/entidade do instrumento do CNPJ da contratação de origem. A participação de instrumentos originados por outra entidade será medida por `SharedProcurementShare`, sem presunção de irregularidade.

## Mercado relevante

Os probes de itens do PNCP não forneceram, na amostra testada, taxonomia suficientemente granular para tratar a categoria geral `Compras` como mercado econômico. Por isso, o resultado principal é concentração da **carteira de fornecedores**, não concentração antitruste de mercado. Análises setoriais só serão realizadas quando houver classificação econômica defensável.

## Privacidade

O repositório é público. Bases identificadas publicadas contêm somente fornecedores pessoa jurídica. Registros de pessoa física não terão CPF ou nome republicados. Cópias integrais de pesquisa permanecem em armazenamento privado.

## Regra de interpretação

Concentração, recorrência, persistência e centralidade descrevem dependência e exposição estrutural. Não constituem, isoladamente, evidência de fraude, favorecimento, poder de mercado ou interrupção efetiva de serviços.

Os modelos SICONFI são associativos e ocupam papel complementar. Não devem receber interpretação causal. O número de fornecedores é tratado como controle estrutural, pois possui relação matemática com medidas de concentração.

## Regra temporal

- coleta por data de publicação no PNCP;
- período econômico anual: instrumentos assinados de 01/01/2025 a 31/12/2025;
- acumulados janeiro-M não equivalem ao ano completo;
- após dezembro, será executada captura tardia em 2026 de instrumentos assinados em 2025;
- a base anual somente será congelada depois da captura tardia e das validações de duplicidade, janela temporal e hash.

## Estado atual

O Paper 1 utiliza a evidência consolidada janeiro-junho. Julho já foi validado e integra a trilha longitudinal do Paper 2. A coleta dos meses restantes de 2025 continua sem mudança da metodologia principal.
