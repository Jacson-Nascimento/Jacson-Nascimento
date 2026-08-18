# Metodologia Reespecificada após os Testes de Dados

## 1. Unidade compradora

A unidade principal deixa de ser o município agregado e passa a ser a instituição contratante identificada pelo CNPJ do órgão/entidade no instrumento.

Defina:

- `b`: comprador institucional, CNPJ do órgão/entidade;
- `s`: fornecedor;
- `m`: mercado de contratação;
- `t`: ano de assinatura.

A dimensão municipal `i` permanece como variável territorial associada ao comprador, quando a associação for não ambígua.

## 2. Valor da relação

Para instrumentos elegíveis `k` pertencentes à relação comprador-fornecedor-mercado-ano:

`V_bsmt = Σ_k V_k`

A especificação principal partirá de `valorInicial`, após regras explícitas para tipo de instrumento e duplicidade econômica.

O valor total do mercado do comprador é:

`V_bmt = Σ_s V_bsmt`

A participação do fornecedor é:

`q_bsmt = V_bsmt / V_bmt`

## 3. Concentração

### HHI

`HHI_bmt = Σ_s q_bsmt²`

### Participação do maior fornecedor

`CR1_bmt = max_s(q_bsmt)`

### Quatro maiores fornecedores

`CR4_bmt = Σ_{s em Top4} q_bsmt`

### Número efetivo de fornecedores

`N_eff_bmt = 1 / HHI_bmt`

### Entropia normalizada

`Hnorm_bmt = -Σ_s q_bsmt ln(q_bsmt) / ln(N_bmt)`

para `N_bmt > 1`.

## 4. Definição do mercado

A variável geral `categoriaProcesso` não será automaticamente tratada como mercado econômico. O piloto mostrou que `Compras` é excessivamente amplo.

Será utilizada uma hierarquia de decisão.

### Nível A - classificação oficial granular

Priorizar, quando houver cobertura e conteúdo informativo suficientes:

- NCM/NBS;
- categoria de catálogo;
- código de catálogo;
- categoria do item.

O simples preenchimento do campo não será considerado suficiente. Categorias como `Não se aplica` serão tratadas como ausência de classificação econômica.

### Nível B - categorias de processo relativamente homogêneas

Categorias como TIC, Obras, Serviços de Engenharia e, após validação, Serviços de Saúde poderão formar estratos próprios ou análises setoriais.

### Nível C - classificação textual

Classificação baseada na descrição do item ou objeto somente será usada se a taxonomia oficial for insuficiente e após protocolo específico de validação. Não será introduzida apenas para viabilizar o resultado esperado.

## 5. Compras compartilhadas

O CNPJ do instrumento pode diferir do CNPJ proprietário da contratação de origem.

Defina:

`ExternalOrigin_k = 1[CNPJ_contrato != CNPJ_compra]`

Para comprador-mercado-ano:

`SharedProcurementShare_bmt = Σ_k V_k ExternalOrigin_k / Σ_k V_k`

A medida representa exposição a contratações originadas por outra entidade, por exemplo consórcios ou estruturas compartilhadas. Não representa irregularidade.

## 6. Rede comprador-fornecedor

Para cada mercado e ano:

`G_mt = (B, S, E)`

onde os compradores `B` e fornecedores `S` formam rede bipartida e a aresta possui peso `V_bsmt`.

### Degree do fornecedor

`Degree_smt = |{b : V_bsmt > 0}|`

### Strength

`Strength_smt = Σ_b V_bsmt`

### Reach

`Reach_smt = Degree_smt / NBuyers_mt`

### Participação sistêmica

`SystemShare_smt = Σ_b V_bsmt / Σ_b Σ_s V_bsmt`

## 7. Exposição estrutural do comprador

As métricas de centralidade do fornecedor serão transformadas inicialmente em percentis dentro de mercado-ano.

`Pdegree_smt = percentile(Degree_smt)`

`Pstrength_smt = percentile(Strength_smt)`

Então:

`Edegree_bmt = Σ_s q_bsmt Pdegree_smt`

`Estrength_bmt = Σ_s q_bsmt Pstrength_smt`

Não serão definidos pesos arbitrários para um índice composto antes de testar correlação, dimensionalidade e estabilidade das métricas.

## 8. Dependência bilateral

A concentração da carteira pública do próprio fornecedor será calculada por:

`r_bsmt = V_bsmt / Σ_b V_bsmt`

`BuyerHHI_smt = Σ_b r_bsmt²`

Isso permite distinguir:

- comprador dependente do fornecedor;
- fornecedor dependente de poucos compradores;
- dependência bilateral.

## 9. Persistência

Se `S_bmt` representa o conjunto de fornecedores do comprador `b`, mercado `m`, no ano `t`:

`Jaccard_bmt = |S_bmt ∩ S_bm,t-1| / |S_bmt ∪ S_bm,t-1|`

`Turnover_bmt = 1 - Jaccard_bmt`

A análise de persistência exige cobertura temporal comparável entre os anos.

## 10. Choques estruturais

Para um conjunto removido de fornecedores `R`:

`Loss_bmt(R) = Σ_{s em R} q_bsmt`

Para limiar `tau`:

`Severe_mt(R,tau) = (1/N_B) Σ_b I[Loss_bmt(R) >= tau]`

Serão comparados:

1. remoção aleatória;
2. remoção por Degree;
3. remoção por Strength;
4. outras centralidades apenas se acrescentarem informação substantiva.

A interpretação será de exposição contratual. Não se afirmará que a retirada simulada implica interrupção efetiva do serviço público.

## 11. Controles municipais

Quando o comprador puder ser associado a um município, serão incorporados:

- população;
- despesa empenhada, liquidada ou paga do SICONFI;
- estrutura da despesa;
- PIB per capita defasado;
- UF e região.

Uma variável de escala candidata é:

`ProcurementIntensity_it = ValorContratadoPNCP_it / DespesaEmpenhadaSICONFI_it`

Ela não é identidade contábil e será tratada com cautela, porque contratos e execução orçamentária possuem conceitos e temporalidades diferentes.

## 12. Modelos associativos

Um modelo inicial de concentração poderá assumir:

`HHI_bmt = beta1 SharedProcurementShare_bmt + beta2 ln(Value_bmt) + beta3 ln(Contracts_bmt + 1) + beta4 DirectShare_bmt + theta X_it + FE_m + FE_t + FE_UF + error_bmt`

`DirectShare`, `SharedProcurementShare` e outras características da contratação não serão descritas como causas da concentração sem estratégia adicional de identificação.

A simultaneidade é plausível: a estrutura do mercado pode influenciar a modalidade e a modalidade pode estar associada à estrutura observada.

## 13. Critérios mínimos para cálculo substantivo de concentração

Os limites definitivos serão escolhidos após a coleta anual, mas o artigo evitará interpretar mercados com informação evidentemente insuficiente.

Serão avaliados, no mínimo:

- cobertura temporal do comprador;
- número de instrumentos;
- número de fornecedores;
- valor total;
- completude da classificação de mercado;
- presença de retificações ou valores anômalos;
- participação de instrumentos compartilhados.

Filtros não serão escolhidos com base em aumentar ou reduzir o HHI observado.

## 14. Robustez

As análises de robustez previstas incluem:

- valor inicial versus valor global;
- fornecedores PJ versus todos os fornecedores em agregados privados;
- contratos termo inicial versus conjunto elegível de instrumentos;
- exclusão e inclusão de compras compartilhadas;
- comprador institucional versus agregação municipal;
- diferentes granularidades de mercado;
- winsorização ou exclusão justificada de valores extremos;
- diferentes limiares nos choques de rede.

## 15. Regra de interpretação

Concentração, persistência e centralidade podem refletir especialização, escala, exclusividade, estrutura regional de oferta, compras compartilhadas ou outras características legítimas.

Os indicadores são instrumentos de descrição estrutural e potencial priorização de auditoria. Não constituem prova isolada de fraude, direcionamento, favorecimento ou falha de controle.
