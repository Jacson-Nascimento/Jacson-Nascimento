# Metodologia Reespecificada após os Testes de Dados

## 1. Objeto empírico

O artigo mede **dependência de fornecedores**, não concentração antitruste de mercados de produtos.

A unidade principal é a instituição contratante identificada pelo CNPJ do órgão/entidade no instrumento.

Defina:

- `b`: comprador institucional;
- `s`: fornecedor;
- `c`: categoria administrativa do PNCP, quando utilizada;
- `t`: ano de assinatura.

O município `i` permanece como dimensão territorial e fonte de controles quando a associação comprador-município for não ambígua.

## 2. Resultado principal: concentração da carteira de fornecedores

Para os instrumentos elegíveis `k` entre comprador `b` e fornecedor `s` no ano `t`:

`V_bst = Σ_k V_k`

A especificação principal parte de `valorInicial`, após classificação dos tipos de instrumento e tratamento das retificações.

O valor total da carteira anual do comprador é:

`V_bt = Σ_s V_bst`

A participação financeira do fornecedor é:

`q_bst = V_bst / V_bt`

### PortfolioHHI

`PortfolioHHI_bt = Σ_s q_bst²`

O indicador mede concentração financeira da carteira de fornecedores do comprador.

Ele **não** será interpretado como medida de competição, poder de mercado ou definição antitruste de mercado relevante.

### PortfolioCR1

`PortfolioCR1_bt = max_s(q_bst)`

### PortfolioCR4

`PortfolioCR4_bt = Σ_{s em Top4} q_bst`

### Número efetivo de fornecedores

`PortfolioNeff_bt = 1 / PortfolioHHI_bt`

### Entropia normalizada

`PortfolioEntropy_bt = -Σ_s q_bst ln(q_bst) / ln(N_bt)`

para `N_bt > 1`.

## 3. Segunda dimensão: concentração da frequência contratual

O piloto mostrou que dependência monetária e recorrência contratual devem ser separadas.

Defina:

`n_bst = número de instrumentos elegíveis do comprador b com fornecedor s no ano t`

`p_bst = n_bst / Σ_s n_bst`

Então:

`CountHHI_bt = Σ_s p_bst²`

A comparação entre `PortfolioHHI` e `CountHHI` produzirá quatro padrões:

1. alta concentração monetária e alta recorrência;
2. alta concentração monetária e baixa recorrência;
3. baixa concentração monetária e alta recorrência;
4. baixa concentração nas duas dimensões.

Essa distinção será tratada como uma contribuição empírica própria do artigo.

## 4. Categorias administrativas e mercado relevante

Os probes de itens mostraram que a classificação disponível no PNCP não sustentou, na amostra testada, uma taxonomia econômica suficientemente granular.

Nos itens de 2025 examinados:

- `itemCategoriaNome` estava preenchido, mas era `Não se aplica` em 100% dos 170 itens;
- `ncmNbsCodigo` teve cobertura 0%;
- `catalogoCodigoItem` teve cobertura 0%;
- a categoria de catálogo não apareceu preenchida.

Consequentemente, `Compras` não será tratada como mercado econômico e não serão utilizados limiares antitruste para interpretar o HHI.

As categorias do PNCP terão três funções:

1. descrição da composição da carteira;
2. controle estatístico;
3. análises secundárias por categoria administrativa.

Uma análise futura de concentração de mercado ficará restrita a segmentos homogêneos para os quais uma taxonomia auditável possa ser demonstrada.

## 5. Concentração do mix de categorias

Para a categoria administrativa `c`:

`V_bct = valor total do comprador b na categoria c e ano t`

`w_bct = V_bct / V_bt`

Então:

`CategoryMixHHI_bt = Σ_c w_bct²`

Esse indicador mede quão concentrada é a composição administrativa da carteira de compras e servirá como controle de mix.

Também poderá ser calculado:

`PortfolioHHI_bct`

como concentração da carteira de fornecedores dentro de uma categoria administrativa. A nomenclatura será explícita para evitar confusão com concentração de mercado.

## 6. Compras compartilhadas

O CNPJ do instrumento pode diferir do CNPJ da contratação de origem.

Defina:

`ExternalOrigin_k = 1[CNPJ_instrumento != CNPJ_compra]`

Para comprador-ano:

`SharedProcurementShare_bt = Σ_k V_k ExternalOrigin_k / Σ_k V_k`

A medida representa participação financeira de instrumentos originados por outra entidade, como consórcios ou estruturas compartilhadas. Não representa irregularidade por si só.

## 7. Rede comprador-fornecedor

A rede principal é anual e institucional:

`G_t = (B, S, E)`

onde `B` são compradores, `S` fornecedores e as arestas são relações ponderadas por `V_bst`.

Redes por categoria administrativa serão análises secundárias.

### Degree

`Degree_st = |{b : V_bst > 0}|`

### Strength

`Strength_st = Σ_b V_bst`

### Reach

`Reach_st = Degree_st / NBuyers_t`

### Participação na rede observada

`SystemShare_st = Σ_b V_bst / Σ_b Σ_s V_bst`

## 8. Exposição a fornecedores centrais

Degree e Strength serão convertidos inicialmente em percentis anuais:

`Pdegree_st = percentile(Degree_st)`

`Pstrength_st = percentile(Strength_st)`

A exposição do comprador será:

`Edegree_bt = Σ_s q_bst Pdegree_st`

`Estrength_bt = Σ_s q_bst Pstrength_st`

Não será criado índice composto com pesos arbitrários antes de avaliar dimensionalidade, correlação e estabilidade temporal.

## 9. Dependência bilateral

Do ponto de vista do fornecedor:

`r_bst = V_bst / Σ_b V_bst`

`BuyerHHI_st = Σ_b r_bst²`

Isso permite distinguir:

- comprador dependente de determinado fornecedor;
- fornecedor dependente de poucos compradores públicos;
- situações de dependência bilateral.

## 10. Persistência

Se `S_bt` é o conjunto de fornecedores do comprador `b` no ano `t`:

`Jaccard_bt = |S_bt ∩ S_b,t-1| / |S_bt ∪ S_b,t-1|`

`Turnover_bt = 1 - Jaccard_bt`

A análise exige cobertura temporal comparável entre os exercícios.

Também serão avaliadas persistência dos principais fornecedores e estabilidade de `PortfolioHHI`, `CR1` e `CountHHI`.

## 11. Choques estruturais

Para conjunto removido de fornecedores `R`:

`Loss_bt(R) = Σ_{s em R} q_bst`

Para limiar `tau`:

`Severe_t(R,tau) = (1/N_B) Σ_b I[Loss_bt(R) >= tau]`

Serão comparadas:

1. remoção aleatória;
2. remoção por Degree;
3. remoção por Strength;
4. outras centralidades somente se acrescentarem informação substantiva.

A interpretação é de exposição da carteira contratual, não de interrupção comprovada de serviços.

## 12. Controles externos

Para compradores associados de forma não ambígua a municípios serão incorporados:

- população;
- despesa empenhada, liquidada e paga do SICONFI;
- composição da despesa;
- PIB per capita defasado;
- UF e região.

Uma variável de escala candidata é:

`ProcurementIntensity_it = ValorContratadoPNCP_it / DespesaEmpenhadaSICONFI_it`

Ela não é identidade contábil, pois contratos e execução orçamentária possuem conceitos e temporalidades diferentes.

## 13. Modelo associativo inicial

Uma especificação de referência será:

`PortfolioHHI_bt = beta1 SharedProcurementShare_bt + beta2 ln(Value_bt) + beta3 ln(Contracts_bt + 1) + beta4 CategoryMixHHI_bt + beta5 DirectShare_bt + theta X_it + FE_t + FE_UF + error_bt`

Uma especificação paralela utilizará `CountHHI_bt` como variável dependente.

As relações serão interpretadas como associações. Contratação direta, compras compartilhadas e demais covariáveis não serão descritas como causas sem estratégia adicional de identificação.

## 14. Hipóteses principais

### H1 - concentração financeira

Uma parcela não trivial dos compradores públicos apresenta concentração financeira relevante da carteira em poucos fornecedores.

### H2 - divergência valor-frequência

`PortfolioHHI` e `CountHHI` não classificam os compradores de forma equivalente.

### H3 - exposição de rede

Compradores com concentração local relativamente baixa podem apresentar exposição elevada a fornecedores estruturalmente centrais na rede.

### H4 - choque direcionado

A remoção simulada de fornecedores centrais gera perda de exposição contratual superior à remoção aleatória da mesma quantidade de fornecedores.

### H5 - compras compartilhadas

`SharedProcurementShare` está associada à estrutura da carteira de fornecedores, com sinal a ser estimado empiricamente.

### H6 - persistência

A composição comprador-fornecedor e as medidas de concentração apresentam persistência entre exercícios quando a cobertura é comparável.

## 15. Critérios mínimos de qualidade

Antes de interpretar os indicadores serão avaliados:

- cobertura temporal do comprador;
- quantidade de instrumentos;
- quantidade de fornecedores;
- valor total da carteira;
- tipos de instrumento;
- retificações;
- atrasos de publicação;
- valores extremos;
- participação de compras compartilhadas;
- estabilidade entre diferentes regras de inclusão.

Filtros não serão escolhidos com base em tornar a concentração maior ou menor.

## 16. Robustez

As análises previstas incluem:

- valor inicial versus valor global;
- fornecedores PJ versus agregados privados com todos os fornecedores;
- contratos termo inicial versus conjunto ampliado de instrumentos elegíveis;
- inclusão e exclusão de compras compartilhadas;
- comprador institucional versus agregação municipal;
- concentração anual versus concentração por categoria administrativa;
- PortfolioHHI versus CountHHI;
- tratamento de valores extremos;
- diferentes limiares nos choques de rede.

## 17. Regra de interpretação

Concentração da carteira, recorrência, persistência e centralidade podem refletir especialização, escala, contratos de grande porte, exclusividade, estrutura regional de oferta ou compras compartilhadas legítimas.

Os indicadores descrevem dependência e exposição estrutural e podem apoiar priorização de auditoria. Não constituem prova isolada de fraude, direcionamento, favorecimento, poder de mercado ou falha de controle.
