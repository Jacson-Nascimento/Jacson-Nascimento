# Estrutura do Artigo v2

## Título provisório

**Dependência de Fornecedores nas Compras Públicas: Concentração da Carteira e Vulnerabilidade Estrutural em Redes de Contratação**

### Título em inglês

**Supplier Dependency in Public Procurement: Portfolio Concentration and Structural Vulnerability in Contracting Networks**

## Pergunta de pesquisa

Em que medida compradores públicos concentram valor e frequência de contratação em poucos fornecedores, e quanto a estrutura da rede comprador-fornecedor revela exposições que não são capturadas pelas medidas locais de concentração da carteira?

## Contribuição central

O artigo separa três dimensões que frequentemente são tratadas como equivalentes:

1. concentração monetária da carteira de fornecedores;
2. concentração da frequência das relações contratuais;
3. exposição a fornecedores estruturalmente centrais na rede pública.

A contribuição não depende de interpretar categorias administrativas amplas como mercados econômicos.

## Hipóteses

### H1 - Concentração monetária

Uma parcela não trivial dos compradores apresenta carteira financeira concentrada em poucos fornecedores.

### H2 - Divergência valor-frequência

`PortfolioHHI` e `CountHHI` não classificam os compradores de forma equivalente.

### H3 - Exposição de rede

Compradores com concentração local relativamente baixa podem estar expostos a fornecedores de elevada centralidade na rede.

### H4 - Choques direcionados

A remoção simulada de fornecedores estruturalmente centrais produz perda contratual superior à remoção aleatória equivalente.

### H5 - Compras compartilhadas

A participação de instrumentos originados em compras compartilhadas está associada à estrutura da carteira de fornecedores, com sinal a ser determinado empiricamente.

### H6 - Persistência

A composição comprador-fornecedor e as medidas de concentração apresentam persistência entre exercícios quando a cobertura temporal é comparável.

# 1. Introdução

## 1.1 Motivação

Organizações públicas podem contratar muitos fornecedores e, ainda assim, concentrar parcela elevada do valor total em poucas empresas. Número nominal de fornecedores, concentração monetária e recorrência contratual não são medidas equivalentes.

## 1.2 Problema

Indicadores convencionais de concentração local também não identificam necessariamente a exposição a fornecedores que atendem grande número de compradores públicos.

## 1.3 Pergunta

Apresentar a pergunta central.

## 1.4 Contribuições

- construção de medidas de concentração da carteira por valor e frequência;
- comparação sistemática entre as duas dimensões;
- integração com métricas de redes bipartidas comprador-fornecedor;
- simulação de choques direcionados e aleatórios;
- documentação de compras compartilhadas;
- base reproduzível com dados públicos e controles fiscais.

## 1.5 Limite conceitual

Esclarecer desde a introdução que `PortfolioHHI` mede dependência da carteira de fornecedores e não concentração antitruste de mercado.

# 2. Literatura

## 2.1 Dependência de fornecedores e concentração da base de suprimentos

Literatura sobre supplier dependency, supply-base concentration, sourcing concentration e procurement resilience.

## 2.2 Compras públicas

Competição, repetição de fornecedores, compras compartilhadas, governança e risco de fornecimento.

## 2.3 Redes comprador-fornecedor

Redes bipartidas, centralidade, fragilidade estrutural e propagação de choques.

## 2.4 Auditoria e priorização baseada em risco

Uso de indicadores quantitativos como sinais para priorização de análise, sem equivalência automática a irregularidade.

# 3. Dados

## 3.1 PNCP

- instrumentos contratuais e empenhos;
- compradores institucionais;
- fornecedores;
- valores;
- datas;
- tipos de instrumento;
- contratação de origem;
- compras compartilhadas.

## 3.2 SICONFI/DCA

- despesa empenhada;
- despesa liquidada;
- despesa paga;
- composição fiscal.

## 3.3 IBGE

- população;
- PIB e PIB per capita defasados;
- UF e região.

## 3.4 Receita Federal/CNPJ

Enriquecimento posterior da amostra de fornecedores pessoa jurídica.

## 3.5 Política de dados

Separar base integral privada e base pública minimizada. O repositório não republicará CPF ou nome associado a fornecedor PF.

# 4. Construção da Amostra

## 4.1 Coleta por data de publicação

A API é percorrida pela data de publicação.

## 4.2 Classificação econômica por assinatura

O painel é atribuído pelo ano de assinatura.

## 4.3 Publicações tardias

A coleta de 2025 deve incluir publicações de 2026 referentes a instrumentos assinados em 2025.

## 4.4 Tipos de instrumento

Documentar regras para contrato inicial, empenho, outros instrumentos e retificações.

## 4.5 Compras compartilhadas

Distinguir CNPJ do instrumento e CNPJ da contratação de origem.

# 5. Metodologia

## 5.1 Concentração monetária da carteira

`PortfolioHHI`, `PortfolioCR1`, `PortfolioCR4`, `PortfolioNeff`, entropia.

## 5.2 Concentração por frequência

`CountHHI`, `CountCR1`, `CountCR4`, `CountNeff`.

## 5.3 Matriz valor-frequência

Classificação em quatro quadrantes e análise de divergência de rankings.

## 5.4 Mix de categorias

`CategoryMixHHI` como controle de composição da carteira.

## 5.5 Rede comprador-fornecedor

Degree, Strength, Reach e participação sistêmica observada.

## 5.6 Exposição estrutural

`Edegree` e `Estrength`.

## 5.7 Dependência bilateral

`BuyerHHI` do fornecedor.

## 5.8 Persistência

Jaccard, turnover e estabilidade das principais métricas.

## 5.9 Choques

Remoções aleatórias e direcionadas.

## 5.10 Modelos associativos

Modelos para PortfolioHHI e CountHHI, com compras compartilhadas, tamanho da carteira, quantidade de instrumentos, mix de categorias e controles territoriais.

# 6. Resultados

## 6.1 Formação da amostra

Fluxo desde registros brutos até compradores-ano elegíveis.

## 6.2 Distribuição da concentração monetária

PortfolioHHI, CR1 e número efetivo.

## 6.3 Valor versus frequência

Correlação, dispersão e quadrantes PortfolioHHI × CountHHI.

## 6.4 Estrutura da rede

Distribuições de Degree, Strength e Reach.

## 6.5 Dependência oculta

Casos de baixa concentração local combinada com alta exposição a fornecedores centrais.

## 6.6 Compras compartilhadas

Comparação descritiva e modelos associativos.

## 6.7 Choques estruturais

Curvas de remoção e distribuição da perda contratual.

## 6.8 Persistência

Comparação intertemporal quando a base 2024-2025 estiver validada.

# 7. Robustez

- valor inicial versus global;
- PJ versus agregados privados com todos os tipos de fornecedor;
- tipos de instrumento;
- compras compartilhadas;
- comprador institucional versus município;
- carteira total versus categorias administrativas;
- regras de valores extremos;
- diferentes métricas e percentis de centralidade;
- diferentes percentuais de remoção e limiares de perda.

# 8. Discussão

## 8.1 Interpretação econômica

Distinguir contratos grandes, recorrência e centralidade.

## 8.2 Aplicação em auditoria

Os indicadores podem ajudar a priorizar revisões, mas exigem análise do contexto contratual.

## 8.3 O que os indicadores não demonstram

Não provam fraude, direcionamento, ausência de competição ou interrupção de serviços.

# 9. Limitações

- cobertura histórica e atrasos do PNCP;
- heterogeneidade de instrumentos;
- valor contratado não equivale a execução financeira;
- classificação de item insuficiente para alguns tipos de análise setorial;
- centralidade não mede substituibilidade técnica;
- choques simulados não observam resposta adaptativa do comprador.

# 10. Conclusão

Sintetizar a diferença entre dependência monetária, recorrência e exposição de rede e discutir a utilidade desses indicadores para gestão e auditoria de compras públicas.

# Tabelas planejadas

1. Formação da amostra e controles de qualidade.
2. Estatísticas descritivas comprador-ano.
3. PortfolioHHI, CR1, CR4 e número efetivo.
4. CountHHI e medidas de frequência.
5. Correlação e concordância de rankings valor-frequência.
6. Métricas de rede dos fornecedores.
7. Exposição estrutural dos compradores.
8. Compras compartilhadas e concentração.
9. Simulações de choque.
10. Modelos associativos e robustez.

# Figuras planejadas

1. Fluxo de construção da base.
2. Distribuição do PortfolioHHI.
3. PortfolioHHI versus CountHHI.
4. Número nominal versus número efetivo de fornecedores.
5. Degree versus Strength.
6. PortfolioHHI versus exposição estrutural.
7. Curvas de remoção aleatória e direcionada.
8. Mapas territoriais apenas como análise secundária, após associação institucional-municipal validada.
