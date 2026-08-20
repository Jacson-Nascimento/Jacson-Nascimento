# Dependência de Fornecedores e Compras Públicas

Projeto de pesquisa quantitativa sobre concentração da carteira de fornecedores, exposição externa em rede, recorrência contratual e vulnerabilidade estrutural nas compras públicas municipais.

## Pergunta central

Em que medida compradores públicos municipais concentram valor e frequência de contratação em poucos fornecedores, e quanto a posição externa desses fornecedores revela exposições que não aparecem nas medidas locais de concentração da carteira?

## Estratégia de publicação

O projeto possui dois papers complementares, com perguntas e contribuições distintas.

### Paper 1: janeiro a junho de 2025

**Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição Externa em Rede e Testes de Estresse**

Objetivo: propor e validar o framework de mensuração combinando concentração local da carteira, exposição externa leave-one-buyer-out, discordância entre HHI e exposição, stress tests e persistência longitudinal.

Manuscrito principal: `paper/PAPER1_JAN_JUN_2025_V3.md`.

### Paper 2: ano de 2025 completo

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

Objetivo: testar a estabilidade temporal do framework ao longo de janeiro-dezembro, decompor efeito de composição, avaliar estabilidade dos stress tests e das associações fiscais e medir a sensibilidade à captura tardia de instrumentos assinados em 2025 e publicados em 2026.

Especificação anual atual: `paper/PAPER2_ANUAL_2025_V2.md`.

O Paper 2 deve citar o Paper 1 e evitar repetição integral de texto, tabelas e contribuição. Sua contribuição própria é longitudinal e de validação anual.

## Fontes principais

- PNCP: instrumentos, fornecedores, órgãos, unidades, valores, datas e contratações de origem.
- SICONFI/DCA: controles fiscais e contábeis municipais.
- IBGE: população e características econômicas municipais.
- Receita Federal/CNPJ: características cadastrais de fornecedores PJ, como enriquecimento posterior.

## Estrutura

- `data/raw/`: amostras e arquivos de referência permitidos para publicação.
- `data/processed/`: bases analíticas minimizadas.
- `scripts/`: coleta, limpeza, diagnóstico, cálculos e robustezes.
- `docs/`: metodologia, dicionário de variáveis e registros técnicos.
- `results/`: tabelas, métricas, logs e saídas analíticas.
- `paper/`: materiais dos dois artigos.

## Unidade principal de análise

`comprador institucional (CNPJ) × fornecedor × ano`

O município é dimensão territorial e fonte de controles. Categorias administrativas do PNCP são utilizadas para composição e análises secundárias, não presumidas como mercados econômicos.

O escopo empírico principal corresponde a órgãos do Poder Executivo municipal observados no PNCP segundo os filtros documentados. Por isso, títulos e conclusões usam explicitamente o termo **compras públicas municipais**.

## Distinção conceitual central

A robustez leave-one-buyer-out mostrou que duas funções do Strength devem ser separadas.

### Importância sistêmica do fornecedor

`Strength_j = sum_b(V_bj)`

O Strength global bruto mede massa monetária sistêmica observada e permanece o ranking principal dos testes de estresse.

### Exposição externa do comprador

Para comprador `b`:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Strength LOO é a medida preferencial de exposição externa. Degree LOO é complementar.

A exposição Strength bruta permanece apenas para comparabilidade histórica, porque a robustez mostrou forte componente de auto-inclusão do próprio comprador.

## Resultados estruturais do Paper 1

Na amostra de 1.347 compradores elegíveis:

- correlação entre exposição Strength bruta e Strength LOO: `rho = 0,2647`;
- correlação entre Degree bruto e Degree LOO: `rho = 0,9821`;
- correlação entre Strength LOO e Degree LOO: `rho = 0,9500`;
- HHI normalizado x Strength LOO: `rho = -0,0183`;
- HHI normalizado x Degree LOO: `rho = -0,0763`.

A classificação passa a ser denominada **discordância concentração-exposição** ou **exposição externa não capturada pelo HHI**.

- Strength LOO: 221 compradores, 16,41%;
- Degree LOO: 237 compradores, 17,59%;
- sobreposição entre as classificações LOO: 89,14%.

O benchmark mecânico sob independência dos cortes Q75 é 18,75%. Os percentuais não devem ser apresentados como prevalência anormal.

## Persistência longitudinal LOO

Abril para maio:

- `rho` Strength LOO: 0,8962;
- `rho` Degree LOO: 0,9091;
- retenção da discordância: 85,96% e 87,57%.

Maio para junho:

- `rho` Strength LOO: 0,9266;
- `rho` Degree LOO: 0,9416;
- retenção da discordância: 90,40% e 90,61%.

A persistência é interpretada como estabilidade de screening, não permanência causal de risco.

## Stress tests

O ranking principal de choque permanece o Strength bruto.

Além das remoções aleatórias uniformes históricas, foi adicionado contrafactual de igual número de fornecedores com probabilidade de seleção proporcional ao Strength.

Para perda de pelo menos 50% da carteira:

- top 1% direcionado: 8,91%, contra 5,46% no aleatório ponderado;
- top 5%: 34,15%, contra 22,88%;
- top 10%: 48,26%, contra 38,52%.

Os top 1%, 5% e 10% concentram 57,56%, 79,47% e 87,41% da massa total de Strength observada.

O procedimento que remove número variável de fornecedores até atingir massa semelhante de Strength é apenas um **diagnóstico de concentração sistêmica**. Não deve ser usado como contrafactual de superioridade do ataque direcionado.

## Robustez econométrica

Os modelos SICONFI são complementares e associativos.

Robustezes adicionais:

- WLS com peso `1/N_m`, equalizando o peso municipal;
- modelo agregado ao município;
- CR1 e CR4 como outcomes alternativos ao HHI normalizado;
- Strength LOO e Degree LOO como outcomes preferenciais de exposição externa.

O número de fornecedores é tratado como controle estrutural, pois possui relação matemática com medidas de concentração.

Com as medidas LOO, a antiga associação positiva entre número de fornecedores e exposição Strength desaparece. Recorrência contratual, em contraste, permanece positiva e consistente nos modelos de exposição externa, mas não apresenta a mesma robustez para concentração local.

Nenhuma associação recebe interpretação causal.

## Scripts de robustez e persistência

- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`
- `scripts/calcular_exposicao_loo_generica.py`
- `scripts/diagnosticos_longitudinais_loo_jan_jun_2025.py`

## Resultados e logs auditáveis

- `results/robustez_estrutural_2025_06/`
- `results/robustez_modelos_municipio_2025_06/`
- `results/exposicao_loo_2025_04/`
- `results/exposicao_loo_2025_05/`
- `results/exposicao_loo_2025_06/`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/`

Os workflows persistem `log_execucao.txt` junto aos resultados para permitir auditoria dos novos números.

## Compras compartilhadas

O projeto distingue o CNPJ do órgão ou entidade do instrumento do CNPJ da contratação de origem. A participação de instrumentos originados por outra entidade é medida sem presunção de irregularidade.

## Mercado relevante

Os probes de itens do PNCP não forneceram taxonomia suficientemente granular para tratar a categoria geral `Compras` como mercado econômico. O resultado principal é concentração da **carteira de fornecedores**, não concentração antitruste de mercado.

## Privacidade

O repositório é público. Bases identificadas publicadas contêm somente fornecedores pessoa jurídica. Registros de pessoa física não terão CPF ou nome republicados. Cópias integrais de pesquisa permanecem em armazenamento privado.

## Regras de interpretação

- HHI, recorrência, persistência e centralidade não implicam fraude ou favorecimento.
- centralidade não mede probabilidade de falha ou substituibilidade técnica.
- stress tests são cenários mecânicos de perda de carteira.
- modelos econométricos são associativos.
- ausência mensal de município não implica falha de reporte.
- janeiro-M não representa o ano completo.

## Regra temporal anual

- coleta por data de publicação no PNCP;
- período econômico anual: instrumentos assinados de 01/01/2025 a 31/12/2025;
- acumulados janeiro-M não equivalem ao ano completo;
- após dezembro, será executada captura tardia em 2026 de instrumentos assinados em 2025;
- a base anual somente será congelada depois da captura tardia e das validações de duplicidade, janela temporal e hash.

## Estado atual

O Paper 1 está estruturado na versão V3 com as robustezes LOO e a persistência abril-junho recalculadas. Julho já foi validado e integra a trilha longitudinal do Paper 2. A coleta dos meses restantes de 2025 continua sem mudança da metodologia de coleta principal.
