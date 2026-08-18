# Estrutura do Artigo v3

## Título provisório

**Dependência de Fornecedores nas Compras Públicas: Concentração da Carteira, Recorrência Contratual e Vulnerabilidade Estrutural**

### Título em inglês

**Supplier Dependency in Public Procurement: Portfolio Concentration, Contractual Recurrence, and Structural Vulnerability**

## Pergunta de pesquisa

Em que medida a dependência de fornecedores dos compradores públicos apresenta dimensões distintas de concentração monetária, recorrência contratual e exposição a fornecedores estruturalmente centrais, e quanto a análise de rede acrescenta às medidas locais da carteira?

## Contribuição central

O artigo separa empiricamente três dimensões:

1. **concentração monetária** — distribuição do valor contratado entre fornecedores;
2. **recorrência contratual** — distribuição da frequência de instrumentos entre fornecedores;
3. **vulnerabilidade estrutural** — exposição da carteira a fornecedores centrais na rede global observada.

A contribuição não depende de interpretar categorias administrativas do PNCP como mercados econômicos.

## Princípios metodológicos incorporados após os testes de robustez

- comprador principal identificado pelo CNPJ institucional;
- PortfolioHHI bruto acompanhado obrigatoriamente de HHI normalizado pelo piso `1/N`;
- CountHHI tratado como dimensão distinta;
- critérios de elegibilidade submetidos a análise de sensibilidade;
- ranking principal de fornecedores calculado na rede global observada;
- ranking restrito à subamostra elegível mantido apenas como robustez;
- simulações comparadas com distribuição aleatória empírica;
- SICONFI usado como controle territorial somente quando o vínculo comprador–município for não ambíguo;
- nenhuma associação será descrita como causal sem estratégia específica de identificação.

# 1. Introdução

## 1.1 Motivação

Um comprador público pode contratar muitos fornecedores e ainda depender economicamente de poucos deles. A contagem nominal de fornecedores, a distribuição do valor, a frequência dos instrumentos e a posição dos fornecedores na rede são objetos diferentes.

## 1.2 Problema

Medidas locais da carteira podem não revelar exposição a fornecedores que ocupam posições centrais na rede de contratação pública. Do mesmo modo, alta frequência de contratos não implica necessariamente alta concentração monetária.

## 1.3 Pergunta de pesquisa

Apresentar a pergunta central e explicar que o objeto é dependência da carteira, não concentração antitruste de mercado.

## 1.4 Contribuições

- mensuração da dependência monetária por PortfolioHHI bruto e normalizado;
- separação entre concentração por valor e por frequência;
- mensuração de exposição a fornecedores centrais em rede bipartida;
- simulação de retirada aleatória e direcionada de fornecedores;
- teste explícito de robustez ao critério de elegibilidade;
- integração com controles fiscais e territoriais;
- protocolo reproduzível e auditável.

## 1.5 Limites conceituais

PortfolioHHI não será interpretado como medida de poder de mercado, competição ou definição de mercado relevante. Vulnerabilidade simulada representa exposição contratual, não interrupção comprovada de serviço.

# 2. Literatura

## 2.1 Dependência de fornecedores e concentração da base de suprimentos

Supplier dependency, sourcing concentration, supply-base concentration e resiliência de suprimentos.

## 2.2 Compras públicas

Repetição de fornecedores, governança, compras compartilhadas, escala e riscos de fornecimento.

## 2.3 Redes comprador-fornecedor

Redes bipartidas, centralidade, concentração de vínculos, resiliência e choques direcionados.

## 2.4 Auditoria e priorização baseada em risco

Indicadores como sinais quantitativos para seleção e priorização de análises, sem equivalência automática a irregularidade.

# 3. Dados

## 3.1 PNCP

- instrumentos contratuais e empenhos;
- CNPJ do comprador institucional;
- fornecedor;
- valores;
- datas;
- tipo de instrumento;
- contratação de origem;
- compras compartilhadas.

## 3.2 SICONFI/DCA

- despesa empenhada;
- despesa liquidada;
- despesa paga;
- população disponível no retorno;
- demais controles fiscais selecionados.

## 3.3 IBGE

- população quando necessário para validação/robustez;
- PIB municipal e PIB per capita defasados;
- UF e região.

## 3.4 Receita Federal/CNPJ

Enriquecimento empresarial da amostra PJ, com atenção à natureza temporal dos atributos cadastrais.

## 3.5 Política de dados

Base pública identificada restrita a PJ. PF e identificadores pessoais não serão republicados no GitHub. Testes com todos os tipos de fornecedor poderão ser executados em base privada/agregada.

# 4. Construção da Amostra

## 4.1 Coleta por data de publicação

A API é percorrida pela data de publicação e os arquivos são particionados para permitir checkpoint, validação e reconstrução.

## 4.2 Ano econômico por data de assinatura

O painel anual é classificado pela data de assinatura do instrumento.

## 4.3 Publicações tardias

Para o ano de assinatura de 2025, a coleta final deverá incluir uma janela em 2026 para capturar publicações tardias.

## 4.4 Chaves e duplicidades

`numeroControlePNCP` é a chave do instrumento. `numeroControlePNCPCompra` vincula o instrumento à contratação de origem e não é chave de deduplicação.

## 4.5 Compras compartilhadas

A diferença entre CNPJ do instrumento e CNPJ da contratação de origem será preservada e tratada como atributo da estrutura contratual.

## 4.6 Critérios de elegibilidade

O corte principal definitivo será escolhido somente após a base anual. A análise deverá apresentar, no mínimo, sensibilidade para:

- 3 fornecedores / 5 instrumentos;
- 5 / 10;
- 5 / 20;
- 10 / 20.

# 5. Metodologia

## 5.1 Participação financeira do fornecedor

Para comprador `b`, fornecedor `s` e ano `t`:

`V_bst = Σ_k V_k`

`q_bst = V_bst / Σ_s V_bst`

## 5.2 PortfolioHHI bruto

`PortfolioHHI_bt = Σ_s q_bst²`

## 5.3 PortfolioHHI normalizado

Para `N_bt > 1`:

`PortfolioHHI_norm_bt = (PortfolioHHI_bt - 1/N_bt) / (1 - 1/N_bt)`

A versão normalizada controla o piso mecânico associado ao número de fornecedores observados.

## 5.4 CR1, CR4 e número efetivo

`CR1_bt = max_s(q_bst)`

`CR4_bt = Σ_{s ∈ Top4} q_bst`

`Neff_bt = 1 / PortfolioHHI_bt`

## 5.5 Concentração por frequência

`p_bst = n_bst / Σ_s n_bst`

`CountHHI_bt = Σ_s p_bst²`

Também será calculado `CountHHI_norm` usando o mesmo piso `1/N`.

## 5.6 Divergência valor–frequência

Comparar:

- níveis;
- diferença `PortfolioHHI - CountHHI`;
- rankings;
- número efetivo por valor versus frequência;
- estabilidade sob diferentes cortes de elegibilidade.

## 5.7 Rede global comprador-fornecedor

`G_t = (B,S,E)`

As centralidades principais dos fornecedores serão calculadas na rede global observada antes da seleção da subamostra analítica.

`Degree_st = |{b : V_bst > 0}|`

`Strength_st = Σ_b V_bst`

`Reach_st = Degree_st / NBuyers_t`

## 5.8 Exposição estrutural do comprador

Com centralidades convertidas em percentis na rede global:

`Edegree_bt = Σ_s q_bst Pdegree_st`

`Estrength_bt = Σ_s q_bst Pstrength_st`

## 5.9 Matriz de exposição

Classificar compradores relativamente aos percentis de concentração local e exposição estrutural:

- baixa concentração / baixa exposição;
- baixa concentração / alta exposição;
- alta concentração / baixa exposição;
- alta concentração / alta exposição.

O quadrante baixa concentração relativa + alta exposição será denominado **exposição estrutural oculta** apenas como classificação analítica, não como índice proprietário.

## 5.10 Simulações de choque

Para conjunto de fornecedores removidos `R`:

`Loss_bt(R) = Σ_{s∈R} q_bst`

Para limiar `τ`:

`Severe_t(R,τ) = (1/N_B) Σ_b I[Loss_bt(R) >= τ]`

Cenários principais:

- remoção aleatória;
- maiores Degree globais;
- maiores Strength globais;
- 1%, 5% e 10% dos fornecedores;
- limiares de perda de 25%, 50% e 75%.

Inicialmente serão executadas 1.000 remoções aleatórias por cenário, com semente registrada. Serão reportados média e intervalo empírico de 95% do cenário aleatório.

## 5.11 Ranking restrito como robustez

As simulações serão repetidas usando Degree/Strength calculados apenas dentro da rede dos compradores elegíveis. Essa especificação não será a principal.

## 5.12 Dependência bilateral

`r_bst = V_bst / Σ_b V_bst`

`BuyerHHI_st = Σ_b r_bst²`

## 5.13 Persistência

Após validação de 2024–2025:

`Jaccard_bt = |S_bt ∩ S_b,t-1| / |S_bt ∪ S_b,t-1|`

`Turnover_bt = 1 - Jaccard_bt`

## 5.14 Controles fiscais

Quando a associação comprador–município for única:

- `ln(DespesaEmpenhada)`;
- `ln(População)`;
- UF/região;
- demais controles fiscais selecionados.

`ProcurementIntensity = ValorContratadoPNCP / DespesaEmpenhadaSICONFI`

será usada com cautela como medida de escala. Em coortes parciais de publicação, seu nível não será interpretado substantivamente.

## 5.15 Modelos associativos

Modelos iniciais poderão usar como dependentes:

- PortfolioHHI;
- PortfolioHHI normalizado;
- CountHHI;
- exposição estrutural.

Covariáveis candidatas:

- tamanho da carteira;
- número de instrumentos;
- número de fornecedores;
- compras compartilhadas;
- mix administrativo;
- controles fiscais/territoriais.

As estimativas serão descritas como associações.

# 6. Resultados

## 6.1 Formação da amostra e qualidade

Fluxo de registros brutos, instrumentos válidos, PJ/PF/PE, compradores e critérios de elegibilidade.

## 6.2 Nível e distribuição da concentração monetária

PortfolioHHI bruto, normalizado, CR1, CR4 e Neff.

## 6.3 Sensibilidade ao tamanho mínimo da carteira

Mostrar como os níveis de HHI variam nos cortes 3/5, 5/10, 5/20 e 10/20.

## 6.4 Valor versus frequência

PortfolioHHI versus CountHHI, HHI normalizado, rankings e proporção de compradores em que concentração monetária supera frequência.

## 6.5 Estrutura da rede global

Degree, Strength, Reach, caudas e concentração das relações.

## 6.6 Exposição estrutural oculta

Matriz concentração local × exposição estrutural.

## 6.7 Choques direcionados versus aleatórios

Resultados principais com ranking global e intervalos empíricos do cenário aleatório.

## 6.8 Controles fiscais e territoriais

Cobertura SICONFI, estatísticas de escala e modelos associativos.

## 6.9 Persistência intertemporal

Somente após a cobertura comparável de 2024–2025.

# 7. Robustez

## 7.1 Critérios de elegibilidade

3/5, 5/10, 5/20 e 10/20.

## 7.2 HHI bruto versus normalizado

Avaliar dependência dos resultados em relação ao número de fornecedores.

## 7.3 Ranking global versus ranking restrito

Comparar centralidades calculadas na rede completa e na subamostra elegível.

## 7.4 Valor contratual

Valor inicial versus alternativas documentadas.

## 7.5 Tipos de fornecedor

PJ pública versus agregados privados incluindo PF/PE.

## 7.6 Lags negativos e inconsistências temporais

Resultados com e sem observações temporalmente inconsistentes.

## 7.7 Compras compartilhadas

Inclusão/exclusão e controle por participação financeira.

## 7.8 Limiares de choque

1%, 5%, 10%; perdas de 25%, 50%, 75%; ampliação do número de sorteios se necessário.

## 7.9 Incerteza condicional

Bootstrap de compradores para medianas e proporções como diagnóstico de estabilidade interna. Os intervalos não corrigem viés de cobertura do PNCP.

# 8. Discussão

## 8.1 O que é concentração de carteira

Discutir dependência financeira sem linguagem antitruste.

## 8.2 Por que frequência e valor divergem

Contratos grandes, recorrência de instrumentos e estrutura de contratação.

## 8.3 O que a rede acrescenta

Exposição a fornecedores centrais que não aparece necessariamente no HHI local.

## 8.4 Aplicação em auditoria

Indicadores como instrumentos de priorização e seleção para análise aprofundada.

# 9. Limitações

- cobertura e maturidade histórica do PNCP;
- publicações tardias;
- heterogeneidade de instrumentos;
- valor contratado não equivale a execução financeira;
- HHI depende do universo de fornecedores observados;
- centralidade não mede substituibilidade técnica;
- simulação não incorpora resposta adaptativa do comprador;
- vínculo institucional-territorial pode ser ambíguo em consórcios e estruturas compartilhadas;
- intervalos bootstrap condicionais não geram representatividade nacional.

# 10. Conclusão

A conclusão deverá se concentrar na distinção entre dependência monetária, recorrência e vulnerabilidade estrutural, evitando transformar medidas de risco em diagnósticos de irregularidade.

# Tabelas previstas

1. Formação da amostra e controles de qualidade.
2. Estatísticas descritivas.
3. PortfolioHHI bruto e normalizado, CR1, CR4 e Neff.
4. Sensibilidade aos critérios de elegibilidade.
5. PortfolioHHI versus CountHHI.
6. Métricas da rede global.
7. Matriz de exposição estrutural.
8. Simulações direcionadas versus aleatórias.
9. Cobertura e integração SICONFI.
10. Modelos associativos.
11. Robustez consolidada.

# Figuras previstas

1. Fluxo de construção da base.
2. Distribuição do PortfolioHHI bruto e normalizado.
3. HHI versus número de fornecedores.
4. PortfolioHHI versus CountHHI.
5. Número nominal versus número efetivo.
6. Degree versus Strength.
7. PortfolioHHI normalizado versus exposição estrutural.
8. Curvas de remoção aleatória versus direcionada.
9. Estabilidade acumulada ao longo dos meses de publicação.
10. Mapas territoriais somente após validação do vínculo institucional-municipal.
