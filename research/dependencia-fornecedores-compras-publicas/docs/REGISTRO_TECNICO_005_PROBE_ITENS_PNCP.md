# Registro Técnico 005 - Itens do PNCP e Redefinição da Medida de Concentração

## 1. Objetivo

Avaliar se os campos de classificação dos itens do PNCP permitem definir mercados econômicos suficientemente homogêneos para cálculo de concentração de fornecedores e testar a disponibilidade dos resultados de item para ligação com fornecedores vencedores.

## 2. Contratações testadas

Foram testadas três contratações históricas já observadas no projeto e três contratações de 2025.

### Amostra histórica

- `00396895000125-1-000495/2022`
- `00402552000126-1-000316/2022`
- `12075748000132-1-000133/2024`

Foram observados 587 itens.

### Amostra 2025

- `06102908000192-1-000004/2025`
- `14675553000159-1-000011/2025`
- `88659313000105-1-000238/2025`

Foram observados 170 itens na primeira página das consultas.

## 3. Campos de classificação

Nos seis casos, `materialOuServico` esteve preenchido em 100% dos itens.

`itemCategoriaNome` também esteve sintaticamente preenchido em 100%, mas nos 170 itens de 2025 testados o conteúdo foi `Não se aplica` em 100% dos casos. O mesmo padrão foi observado nas contratações históricas inspecionadas.

Nos testes realizados:

- `ncmNbsCodigo`: cobertura 0%;
- `catalogoCodigoItem`: cobertura 0%;
- categoria de catálogo: não disponível nos registros observados.

Portanto, preenchimento técnico do campo não equivale a conteúdo econômico informativo.

## 4. Resultados dos itens

O endpoint de resultados do item mostrou capacidade de retornar:

- fornecedor vencedor;
- quantidade homologada;
- valor unitário homologado;
- outras características do resultado.

No teste de 2025, foram recuperados 35 resultados de itens sem erro quando as consultas foram condicionadas a itens com `temResultado = true`.

No primeiro teste histórico ocorreram sete consultas sem resposta JSON utilizável porque o probe ainda tentava consultar alguns itens sem resultado. A repetição condicionada a `temResultado` eliminou o problema na amostra 2025.

## 5. Consequência para a definição de mercado

A categoria geral `Compras` não representa um mercado econômico. Ela agrega objetos heterogêneos, como alimentos, medicamentos, veículos, material de expediente e diversos outros bens.

Os campos de classificação de item observados no probe não forneceram granularidade econômica suficiente para substituir essa categoria por uma taxonomia oficial confiável.

Dessa forma, o projeto não utilizará o HHI agregado da categoria `Compras` como medida de concentração de mercado, nem aplicará limiares antitruste a esse indicador.

## 6. Redefinição do indicador principal

O objeto central do artigo é dependência de fornecedores. Para esse objetivo, não é necessário definir um mercado antitruste. A medida principal passa a ser a concentração da carteira de fornecedores do comprador institucional.

Para comprador institucional `b`, fornecedor `s` e ano `t`:

`V_bst = soma do valor elegível dos instrumentos do comprador b com fornecedor s no ano t`

`V_bt = soma_s V_bst`

`q_bst = V_bst / V_bt`

### HHI da carteira de fornecedores

`PortfolioHHI_bt = soma_s q_bst^2`

Esse indicador mede a concentração financeira da carteira de fornecedores do comprador.

Ele não mede, por si só:

- competição de mercado;
- poder de mercado do fornecedor;
- existência de alternativas tecnicamente equivalentes;
- irregularidade da contratação.

## 7. Métricas complementares

### Participação do maior fornecedor

`PortfolioCR1_bt = max_s(q_bst)`

### Participação dos quatro maiores

`PortfolioCR4_bt = soma das quatro maiores participações`

### Número efetivo de fornecedores

`PortfolioNeff_bt = 1 / PortfolioHHI_bt`

### Concentração por frequência de instrumentos

Defina:

`n_bst = número de instrumentos elegíveis do comprador b com fornecedor s no ano t`

`p_bst = n_bst / soma_s n_bst`

Então:

`CountHHI_bt = soma_s p_bst^2`

Essa medida captura concentração na frequência das relações, em contraste com concentração monetária.

## 8. Divergência valor versus frequência

A comparação entre `PortfolioHHI` e `CountHHI` passa a ser uma dimensão própria da análise.

Possíveis padrões:

1. alto PortfolioHHI e alto CountHHI: dependência monetária e recorrente;
2. alto PortfolioHHI e baixo CountHHI: poucos contratos de grande valor concentrados;
3. baixo PortfolioHHI e alto CountHHI: relação muito recorrente, mas financeiramente menos dominante;
4. baixo PortfolioHHI e baixo CountHHI: carteira mais distribuída nas duas dimensões.

Essa distinção é diretamente relevante para auditoria porque concentração de valor e repetição contratual representam exposições diferentes.

## 9. Composição por categoria

As categorias administrativas do PNCP continuarão sendo utilizadas para decomposição e controle de composição, mas não serão automaticamente chamadas de mercados econômicos.

Defina a participação da categoria `c` no gasto do comprador:

`w_bct = V_bct / V_bt`

Uma medida de concentração do mix de categorias é:

`CategoryMixHHI_bt = soma_c w_bct^2`

Isso permite controlar se o comprador concentra seus gastos em poucos tipos gerais de contratação.

Também será possível calcular:

`PortfolioHHI_bct`

como concentração da carteira de fornecedores dentro de uma categoria administrativa, sempre com nomenclatura explícita de concentração de carteira por categoria, e não concentração de mercado.

## 10. Redes

A rede principal passa a ser anual e institucional:

`G_t = (B, S, E)`

onde:

- `B` são compradores institucionais;
- `S` são fornecedores;
- `E` são relações contratuais ponderadas por valor.

Redes por categoria serão análises secundárias.

## 11. Hipóteses revisadas

### H1 - Concentração da carteira

Uma parcela não trivial dos compradores públicos apresenta elevada concentração financeira em poucos fornecedores.

### H2 - Divergência valor-frequência

A concentração ponderada por valor e a concentração ponderada por número de instrumentos não classificam os compradores de forma equivalente.

### H3 - Exposição de rede

Compradores com concentração local relativamente baixa podem apresentar exposição elevada a fornecedores estruturalmente centrais na rede pública.

### H4 - Choque direcionado

A remoção simulada de fornecedores estruturalmente centrais gera perda de exposição contratual superior à remoção aleatória de fornecedores em quantidade equivalente.

### H5 - Compras compartilhadas

A participação de instrumentos originados em compras compartilhadas está associada à estrutura da carteira de fornecedores, com sinal a ser estimado empiricamente.

### H6 - Persistência

A concentração e a composição das relações comprador-fornecedor apresentam persistência relevante entre exercícios, condicionada à comparabilidade da cobertura temporal.

## 12. Modelo associativo revisado

Uma especificação inicial poderá ser:

`PortfolioHHI_bt = beta1 SharedProcurementShare_bt + beta2 ln(Value_bt) + beta3 ln(Contracts_bt + 1) + beta4 CategoryMixHHI_bt + beta5 DirectShare_bt + theta X_it + FE_t + FE_UF + erro_bt`

A interpretação será associativa. Não será atribuída causalidade às modalidades, compras compartilhadas ou demais covariáveis sem estratégia adicional de identificação.

## 13. Extensão setorial

A análise de concentração dentro de mercados econômicos poderá ser retomada em segmentos mais homogêneos, por exemplo TIC, obras, serviços de engenharia ou determinados grupos de saúde, desde que uma taxonomia auditável e suficientemente granular seja demonstrada.

Essa extensão não será necessária para a contribuição principal sobre dependência da carteira de fornecedores.

## 14. Decisão

O artigo continuará, mas com linguagem mais precisa:

**concentração da carteira de fornecedores e vulnerabilidade estrutural**, e não concentração de mercado das compras públicas em geral.

Essa mudança reduz o risco de erro conceitual, preserva as métricas quantitativas já desenvolvidas e alinha diretamente o indicador ao problema de dependência de fornecedores.
