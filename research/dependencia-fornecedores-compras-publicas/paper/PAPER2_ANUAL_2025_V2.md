# Paper 2 - ano de 2025 completo

## Título provisório

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

### Título em inglês

**Temporal Persistence of Structural Supplier Dependency in Municipal Public Procurement: Annual Evidence, Networks, and Stress Tests**

## 1. Papel científico do Paper 2

O Paper 2 será um estudo de validação temporal do framework definido e testado no Paper 1. Não será uma atualização numérica nem uma reprodução do primeiro manuscrito.

Sua pergunta central será:

> Em que medida a exposição externa dos compradores públicos municipais a fornecedores estruturalmente relevantes permanece estável ao longo de um ano completo, resiste à expansão da rede, à mudança na composição dos compradores elegíveis e à incorporação de publicações tardias?

O framework anual separará explicitamente dois conceitos que a robustez do primeiro semestre mostrou não serem intercambiáveis:

1. **importância sistêmica monetária do fornecedor**, medida pelo Strength global bruto e usada para ordenar fornecedores nos testes de estresse;
2. **exposição externa do comprador**, medida prioritariamente por Strength leave-one-buyer-out e, de forma complementar, por Degree leave-one-buyer-out.

Essa separação será mantida em todas as janelas mensais e no fechamento anual.

## 2. Janela e regra temporal

- período econômico: instrumentos assinados de 01/01/2025 a 31/12/2025;
- coleta operacional: por data de publicação no PNCP;
- janelas mensais de publicação: janeiro a dezembro de 2025;
- depois de dezembro: captura tardia em 2026 de instrumentos assinados em 2025;
- a base anual somente será congelada após a captura tardia e as validações finais.

O artigo distinguirá permanentemente:

- mês de publicação;
- data de assinatura;
- coorte acumulada janeiro-M;
- base anual congelada após captura tardia.

Nenhum acumulado janeiro-M será descrito como ano completo.

## 3. Escopo

O escopo empírico corresponde a compradores institucionais do Poder Executivo municipal observados no PNCP segundo os filtros documentados.

Unidade principal de comprador: CNPJ institucional.

Chave de instrumento: `numeroControlePNCP`, materializada como `id_contrato`.

`numeroControlePNCPCompra` permanece exclusivamente como chave de ligação com a compra e nunca será usado para deduplicar instrumentos.

A base pública identificada permanece restrita a fornecedores pessoa jurídica. Pessoa física e pessoa estrangeira aparecem somente em diagnósticos agregados.

## 4. Perguntas de validação anual

O Paper 2 responderá a seis perguntas empíricas:

1. Os rankings de exposição externa Strength LOO e Degree LOO são persistentes entre meses consecutivos?
2. A discordância entre concentração local e exposição externa permanece com a expansão da rede?
3. Os maiores fornecedores por Strength bruto continuam produzindo perdas de carteira superiores a contrafactuais aleatórios comparáveis?
4. Quanto da mudança das estatísticas agregadas decorre de mudança dentro dos compradores persistentes e quanto decorre da entrada de novos elegíveis?
5. Os padrões associativos fiscais permanecem estáveis quando a exposição é externalizada e os municípios recebem peso equivalente?
6. A captura tardia de 2026 altera materialmente rankings, quadrantes, stress tests ou conclusões anuais?

## 5. Hipóteses descritivas pré-especificadas

O artigo não formulará hipóteses causais. As expectativas descritivas são registradas antes do fechamento anual:

- H1: Strength LOO e Degree LOO apresentarão alta concordância entre si e persistência temporal relevante;
- H2: HHI e exposição externa permanecerão dimensões pouco redundantes;
- H3: o grupo de discordância concentração-exposição não desaparecerá com a expansão da rede;
- H4: ataques direcionados por Strength bruto permanecerão mais severos que remoções aleatórias uniformes e que sorteios de igual tamanho ponderados por Strength;
- H5: medianas transversais serão parcialmente afetadas pela composição dos novos compradores elegíveis;
- H6: os resultados principais permanecerão qualitativamente estáveis após a captura tardia, embora números e rankings individuais possam mudar.

## 6. Métricas congeladas de concentração local

Para comprador `b` e fornecedor `j`, com valor de relação `V_bj`:

`w_bj = V_bj / sum_j(V_bj)`

`HHI_b = sum_j(w_bj^2)`

`HHI_norm_b = (HHI_b - 1/N_b) / (1 - 1/N_b)`

Também serão reportados:

- CountHHI e CountHHI normalizado;
- CR1;
- CR4;
- número efetivo de fornecedores `1/HHI`.

A concentração é concentração da carteira do comprador, não concentração de mercado relevante.

## 7. Importância sistêmica dos fornecedores

A rede principal permanece bipartida entre compradores institucionais e fornecedores PJ.

### 7.1 Strength global bruto

`Strength_j = sum_b(V_bj)`

O Strength bruto representa a escala monetária sistêmica observada do fornecedor. Ele permanecerá o ranking principal dos testes de estresse, pois a pergunta do choque é quais fornecedores concentram maior volume de relações no sistema observado.

### 7.2 Degree global

`Degree_j = número de compradores distintos atendidos por j`

Degree permanece medida complementar de alcance estrutural.

## 8. Exposição externa do comprador

A robustez leave-one-buyer-out do primeiro semestre mostrou que a exposição calculada com Strength bruto incorpora parcela relevante do próprio gasto do comprador. Por isso, o Paper 2 pré-especifica medidas externalizadas.

Para cada comprador `b`:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Após recalcular a posição percentual dos fornecedores na rede externalizada ao comprador, a exposição será:

`E_b^(S,LOO) = sum_j w_bj * PctRank_b(Strength_j^(-b))`

`E_b^(D,LOO) = sum_j w_bj * PctRank_b(Degree_j^(-b))`

Strength LOO será a medida preferencial de exposição externa. Degree LOO será medida complementar e teste de robustez.

A exposição Strength bruta poderá aparecer apenas como ponte de comparabilidade com versões históricas da análise, sempre identificada como mecanicamente contaminada pela contribuição do próprio comprador.

## 9. Discordância concentração-exposição

O artigo não utilizará a expressão “baixa concentração” como sinônimo automático de `HHI < Q75`.

Classificação principal:

- HHI monetário abaixo do Q75 da amostra elegível;
- exposição externa no Q75 ou acima.

Serão reportadas duas versões:

- HHI x Strength LOO;
- HHI x Degree LOO.

A nomenclatura será **discordância concentração-exposição** ou **exposição externa não capturada pelo HHI**.

O benchmark mecânico sob independência entre duas classificações contínuas com cortes Q75 é 18,75%. Portanto, o percentual observado não será apresentado como prevalência anormal. O resultado relevante será a não redundância das dimensões, a identidade dos compradores e a estabilidade temporal da classificação.

Robustezes contínuas:

- gap entre percentil de exposição externa e percentil de HHI;
- resíduo da exposição externa após HHI normalizado.

## 10. Stress tests

### 10.1 Especificação principal congelada

Ranking de choque: Strength global bruto.

Remoções:

- top 1%;
- top 5%;
- top 10%.

Limiar principal de perda severa: 50% da carteira, com 25% e 75% como sensibilidades.

Contrafactual principal histórico: 1.000 remoções aleatórias uniformes de igual número de fornecedores.

### 10.2 Contrafactual adicional pré-especificado

Adicionar sorteio sem reposição de igual `k`, com probabilidade de seleção proporcional ao Strength.

Esse nulo reduz a objeção de que o resultado decorre apenas de comparar fornecedores grandes com um conjunto aleatório dominado por fornecedores pequenos.

### 10.3 Diagnóstico de massa sistêmica

Também será reportado, de forma descritiva, quantos fornecedores de uma ordem aleatória são necessários para acumular massa de Strength semelhante à dos top 1%, 5% e 10%.

Esse diagnóstico mede concentração de massa sistêmica. Ele não será usado como contrafactual de superioridade do ataque direcionado, porque o número de fornecedores removidos é endogenamente muito diferente.

## 11. Painel longitudinal principal

Para cada transição `M-1 -> M`, reportar:

- elegíveis em cada coorte acumulada;
- compradores comuns;
- entrantes;
- saídas;
- Spearman de Strength LOO;
- Spearman de Degree LOO;
- retenção do quartil superior;
- retenção da discordância concentração-exposição;
- estabilidade do quadrante completo;
- mudança de HHI nos compradores comuns;
- perfil dos entrantes;
- mudança na própria contribuição ao Strength bruto.

A análise temporal principal utilizará medidas externalizadas. Séries históricas baseadas em exposição Strength bruta serão mantidas somente como diagnóstico de transição metodológica.

## 12. Evolução da rede

Para cada mês acumulado, reportar:

- compradores;
- fornecedores;
- relações comprador-fornecedor;
- instrumentos;
- distribuição de Degree bruto;
- distribuição de Strength bruto;
- concentração da massa de Strength nos maiores fornecedores;
- distribuição de Strength LOO e Degree LOO no nível comprador;
- associação HHI-exposição externa;
- percentual de discordância concentração-exposição.

## 13. Efeito de composição

Toda comparação mensal separará:

1. estatística transversal total;
2. mudança dentro dos compradores comuns;
3. perfil dos novos elegíveis;
4. perfil de eventuais saídas.

Não atribuir variação da mediana agregada a mudança comportamental sem essa decomposição.

## 14. Integração SICONFI e modelos associativos

A integração SICONFI permanece incremental e exige cobertura de despesa empenhada de pelo menos 95% antes da execução dos modelos.

Os modelos terão papel complementar.

### 14.1 Especificação histórica de concentração

`HHI_norm_b = beta0 + beta1 ln(Pop_b) + beta2 ln(DespesaPC_b) + beta3 ln(NFornec_b) + beta4 ln(InstrPorFornec_b) + Regiao + erro_b`

### 14.2 Robustez municipal

Além do modelo histórico:

- WLS no nível comprador com peso `1/N_m`, onde `N_m` é o número de compradores elegíveis do município;
- OLS agregado ao município;
- CR1 e CR4 como outcomes alternativos.

O número de fornecedores será interpretado como controle estrutural, não como determinante causal da concentração.

### 14.3 Modelos de exposição externa

Outcomes preferenciais:

- Strength LOO;
- Degree LOO.

A exposição Strength bruta permanecerá somente para comparabilidade histórica.

A interpretação priorizará persistência de sinal, ordem de grandeza e consistência entre especificações, e não significância isolada em um mês.

## 15. Captura tardia como teste de sensibilidade anual

Após dezembro, coletar instrumentos publicados em 2026 e assinados em 2025 conforme protocolo específico.

Comparar base dezembro-publicação versus base anual congelada após captura tardia em:

- instrumentos;
- compradores elegíveis;
- fornecedores;
- HHI, CR1, CR4 e Neff;
- Strength bruto sistêmico;
- Strength LOO e Degree LOO;
- ranking de compradores;
- discordância concentração-exposição;
- stress tests;
- coeficientes dos modelos complementares.

A captura tardia é parte do desenho temporal e não uma correção ad hoc.

## 16. Relação com o Paper 1

O Paper 1 propõe e testa o framework no primeiro semestre e registra a correção metodológica de externalização da exposição.

O Paper 2 deve citar o Paper 1 e tratar as métricas como previamente definidas. Sua contribuição própria será a validação anual, a persistência temporal, o efeito de composição, a expansão da rede e a sensibilidade à captura tardia.

Textos, tabelas e discussão não serão reproduzidos integralmente entre os dois papers.

## 17. Estrutura recomendada do manuscrito anual

1. Introdução: por que persistência temporal importa.
2. Framework previamente definido e correção LOO.
3. Dados, calendário de publicação e captura tardia.
4. Evolução mensal da rede.
5. Persistência da exposição externa.
6. Discordância concentração-exposição.
7. Efeito de composição das coortes.
8. Estabilidade dos stress tests.
9. Robustezes estruturais e nulos adicionais.
10. Estabilidade das associações fiscais.
11. Sensibilidade à captura tardia.
12. Discussão, limitações e conclusão.

## 18. Critério de fechamento

O Paper 2 somente será considerado empiricamente fechado quando:

- janeiro-dezembro estiver consolidado;
- duplicidades de `id_contrato` forem zero;
- janelas de publicação forem validadas;
- hashes estiverem registrados;
- captura tardia de 2026 estiver concluída;
- métricas anuais forem recalculadas;
- diagnósticos longitudinais LOO estiverem completos;
- SICONFI anual estiver integrado;
- modelos e robustezes estiverem executados;
- resultados e logs estiverem versionados;
- documentação técnica estiver registrada no GitHub e no Google Drive.
