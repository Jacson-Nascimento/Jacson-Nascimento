# Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição Externa em Rede e Testes de Estresse

## Structural Supplier Dependency in Municipal Public Procurement: Portfolio Concentration, External Network Exposure, and Stress Tests

## Resumo

Este estudo investiga dependência de fornecedores em compras públicas municipais a partir de duas dimensões distintas: concentração monetária dentro da carteira de cada comprador e exposição externa a fornecedores relevantes na rede global de contratação. Utilizamos dados do Portal Nacional de Contratações Públicas referentes a instrumentos publicados entre janeiro e junho de 2025, restringindo as métricas econômicas a instrumentos assinados em 2025 e a fornecedores pessoa jurídica. A unidade de comprador é o CNPJ institucional do órgão do Poder Executivo municipal. A concentração local é medida por HHI, HHI normalizado, CR1, CR4 e número efetivo de fornecedores. Para separar posição externa do fornecedor da contribuição do próprio comprador, construímos exposições leave-one-buyer-out baseadas em Strength e Degree. A robustez mostra que a exposição calculada com Strength bruto contém forte componente de auto-inclusão, enquanto Strength LOO e Degree LOO apresentam elevada concordância entre si e associação muito baixa com HHI. A discordância entre concentração e exposição permanece identificável com ambas as medidas externalizadas e apresenta elevada persistência entre abril e junho. Nos testes de estresse, a remoção dos fornecedores de maior Strength produz perdas de carteira superiores a um contrafactual aleatório de igual tamanho ponderado por Strength. Modelos associativos complementares indicam que recorrência contratual tem associação frágil com concentração local, mas associação positiva e consistente com exposição externa. Os resultados mostram que dependência de fornecedores em compras públicas municipais não pode ser inferida apenas pela concentração observada dentro de cada carteira.

**Palavras-chave:** compras públicas; fornecedores; concentração; redes; dependência estrutural; PNCP; centralidade; stress testing.

## Abstract

This study examines supplier dependency in municipal public procurement through two distinct dimensions: monetary concentration within each buyer's portfolio and external exposure to suppliers that occupy relevant positions in the broader procurement network. We use data from Brazil's National Public Procurement Portal for instruments published from January through June 2025, restricting economic metrics to instruments signed in 2025 and to corporate suppliers. The buyer unit is the institutional tax identifier of municipal executive-branch entities. Local concentration is measured using HHI, normalized HHI, CR1, CR4, and effective number of suppliers. To separate external supplier position from the focal buyer's own contribution, we construct leave-one-buyer-out exposure measures based on supplier Strength and Degree. Robustness tests show that raw Strength-based buyer exposure contains substantial self-inclusion, whereas Strength LOO and Degree LOO are highly concordant with each other and weakly associated with HHI. Concentration-exposure discordance remains identifiable under both externalized measures and is highly persistent from April through June. In stress tests, removing the highest-Strength suppliers produces larger portfolio losses than a Strength-weighted random benchmark of equal size. Complementary associative models indicate that contractual recurrence is weakly associated with local concentration but positively and consistently associated with external exposure. The findings show that supplier dependency in municipal public procurement cannot be inferred from within-portfolio concentration alone.

**Keywords:** public procurement; suppliers; concentration; networks; structural dependency; stress testing; centrality.

# 1. Introdução

A concentração da carteira de fornecedores é uma dimensão relevante de dependência, mas não a esgota. Um comprador pode distribuir seu valor contratado entre diversas empresas e ainda manter parcela importante de sua carteira em fornecedores amplamente conectados a outros compradores. Da mesma forma, uma carteira localmente concentrada pode depender de fornecedores pouco relevantes fora das relações daquele comprador.

Essa distinção produz duas perguntas diferentes. A primeira é local: como o valor de cada comprador está distribuído entre seus fornecedores? A segunda é relacional: qual é a posição dos fornecedores da carteira nas relações com os demais compradores do sistema observado?

Medidas como o índice Herfindahl-Hirschman respondem principalmente à primeira pergunta. Métricas de rede podem contribuir para a segunda, mas exigem cuidado quando a posição global do fornecedor contém o próprio valor contratado pelo comprador cuja exposição está sendo avaliada. Se esse componente não for removido, uma medida apresentada como exposição externa pode refletir parcialmente a própria concentração ou escala local.

Este artigo trata a dependência de fornecedores como um problema de duas dimensões:

1. **concentração local da carteira**, definida a partir das participações monetárias dos fornecedores dentro do comprador;
2. **exposição externa em rede**, definida a partir da posição dos fornecedores após retirar a contribuição do comprador focal.

Uma terceira camada é adicionada por testes de estresse. Neles, a pergunta deixa de ser como um comprador está posicionado e passa a ser quanto de sua carteira seria mecanicamente afetado se conjuntos de fornecedores sistemicamente relevantes fossem removidos.

A pergunta de pesquisa é:

> Em que medida medidas locais de concentração da carteira capturam, ou deixam de capturar, a exposição externa de compradores públicos municipais a fornecedores estruturalmente relevantes, e como essa diferença se manifesta sob choques coletivos simulados?

O estudo não interpreta HHI, centralidade, recorrência ou resultados de simulação como evidência de fraude, favorecimento, conluio, risco de crédito ou interrupção efetiva de serviços públicos.

# 2. Contribuição e literatura

O uso de HHI, redes, Degree, Strength, relações recorrentes e centralidade não constitui novidade isolada. A literatura recente de compras públicas já emprega estruturas de rede para caracterizar relações entre firmas e entidades contratantes, competição e influência.

Sturm, Candia, Damásio et al. (2025) analisam mais de um milhão de contratos da administração pública portuguesa e utilizam métricas de centralidade para estudar a posição de firmas em redes de compras públicas. Fountoukidis, Dafli, Antoniou e Varsakelis (2026) propõem o Institutional Closure Index, no nível da autoridade contratante, combinando concentração, persistência e embeddedness em relações comprador-fornecedor. No Brasil, Fonseca (2025) aplica teoria de redes a contratações públicas federais entre 2022 e meados de 2024.

A contribuição deste estudo é mais restrita e defensável. Integramos, no nível do comprador público municipal:

- concentração monetária local;
- concentração por frequência como caracterização complementar;
- posição sistêmica dos fornecedores;
- exposição externa leave-one-buyer-out;
- discordância entre concentração e exposição;
- testes de estresse direcionados e contrafactuais aleatórios;
- persistência longitudinal do screening;
- integração complementar com características fiscais municipais.

A correção leave-one-buyer-out é especialmente importante porque separa duas funções que poderiam ser confundidas: Strength bruto como medida de importância sistêmica monetária do fornecedor e Strength externalizado como medida de exposição do comprador à posição desse fornecedor fora da própria relação focal.

# 3. Dados e formação da amostra

## 3.1 PNCP

A fonte principal é o Portal Nacional de Contratações Públicas, PNCP. A coleta é feita pela data de publicação do instrumento.

A janela deste paper compreende publicações de 01/01/2025 a 30/06/2025. Para as métricas econômicas são utilizados apenas instrumentos assinados em 2025, com `valorInicial > 0`, pertencentes à esfera municipal e ao Poder Executivo.

A janela é uma **coorte de publicações** e não equivale ao ano de 2025 completo. Instrumentos assinados no período podem ser publicados depois da janela e, portanto, não fazem parte desta coorte.

## 3.2 Unidade institucional e chaves

O comprador principal é o CNPJ institucional do órgão ou entidade do instrumento. Município é dimensão territorial e fonte de controles, não substituto da unidade institucional de comprador.

A chave de instrumento é `numeroControlePNCP`, materializada como `id_contrato`.

`numeroControlePNCPCompra` é utilizado somente como ligação com a compra e nunca como chave de deduplicação de instrumentos.

## 3.3 Privacidade

A base pública identificada contém somente fornecedores pessoa jurídica. Registros de pessoa física e pessoa estrangeira são preservados apenas em diagnósticos agregados, sem republicação de CPF ou nome de pessoa física.

## 3.4 Escala da base

No acumulado janeiro-junho:

- 105.582 instrumentos PJ únicos na coorte de publicação;
- 98.438 instrumentos assinados em 2025;
- 2.349 compradores com métricas calculadas;
- 1.347 compradores elegíveis no critério principal de pelo menos 3 fornecedores e 5 instrumentos;
- 20.367 fornecedores na rede global.

# 4. Concentração local da carteira

Para comprador `b` e fornecedor `j`, seja `V_bj` o valor acumulado da relação comprador-fornecedor e:

`w_bj = V_bj / sum_j(V_bj)`

O HHI monetário da carteira é:

`HHI_b = sum_j(w_bj^2)`

Com `N_b` fornecedores:

`HHI_norm_b = (HHI_b - 1/N_b) / (1 - 1/N_b)`

Também são calculados:

- CR1;
- CR4;
- número efetivo de fornecedores `Neff = 1/HHI`;
- CountHHI e CountHHI normalizado, baseados na frequência de instrumentos.

Essas métricas caracterizam a carteira do comprador. Não constituem medidas de concentração antitruste de mercado relevante.

## 4.1 Resultados

Na amostra elegível 3/5:

- HHI monetário mediano: 0,2365;
- HHI normalizado mediano: 0,1563;
- CountHHI mediano: 0,0816;
- CountHHI normalizado mediano: 0,00682;
- Neff mediano: 4,23;
- CR1 mediano: 0,3837;
- CR4 mediano: 0,8037.

Em 98,14% dos compradores, o HHI monetário supera o HHI por frequência. O resultado mostra que concentração de valor e concentração de contagem não são equivalentes, sem implicar irregularidade.

# 5. Rede comprador-fornecedor

A rede principal é bipartida, com compradores institucionais de um lado e fornecedores PJ do outro.

## 5.1 Strength global bruto

`Strength_j = sum_b(V_bj)`

Strength mede a massa monetária observada nas relações do fornecedor. Ele permanece o ranking principal dos testes de estresse, pois esses cenários buscam identificar a perda associada à remoção dos fornecedores que concentram maior valor no sistema.

## 5.2 Degree global

`Degree_j = número de compradores distintos atendidos por j`

Degree representa alcance institucional e é utilizado como métrica complementar.

# 6. Por que a exposição do comprador precisa ser externalizada

Uma exposição construída diretamente com percentis de Strength bruto reutiliza a contribuição `V_bj` do próprio comprador para determinar a posição do fornecedor. A robustez leave-one-buyer-out mostrou que esse efeito é material.

Entre os 1.347 compradores elegíveis:

- a correlação entre exposição Strength bruta e Strength LOO é `rho = 0,2647`;
- a retenção do quartil superior após a correção é 38,87%;
- a contribuição própria mediana ponderada do comprador ao Strength dos fornecedores de sua carteira é 75,89%.

Em contraste, Degree é muito menos sensível à retirada do comprador focal:

- correlação entre Degree bruto e Degree LOO: `rho = 0,9821`;
- retenção do quartil superior: 89,61%.

Esses resultados exigem uma distinção conceitual. **Strength bruto permanece uma medida de importância sistêmica do fornecedor, mas não deve ser apresentado como medida puramente externa da exposição do comprador.**

# 7. Exposição externa leave-one-buyer-out

Para cada comprador `b`:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

A posição percentual dos fornecedores é recalculada na rede ajustada ao comprador focal.

As exposições são:

`E_b^(S,LOO) = sum_j w_bj * PctRank_b(Strength_j^(-b))`

`E_b^(D,LOO) = sum_j w_bj * PctRank_b(Degree_j^(-b))`

Strength LOO é a medida preferencial de exposição externa. Degree LOO é complementar.

## 7.1 Concordância entre medidas externas

Strength LOO e Degree LOO apresentam correlação de `rho = 0,9500`.

Esse resultado indica que, após retirar a relação focal, escala monetária externa e alcance institucional dos fornecedores produzem rankings de exposição bastante semelhantes no nível do comprador.

# 8. Concentração local e exposição externa

Após a externalização, a associação entre concentração local e exposição de rede torna-se muito pequena.

- HHI normalizado x Strength LOO: `rho = -0,0183`, `p = 0,502`;
- HHI normalizado x Degree LOO: `rho = -0,0763`, `p = 0,0051`.

A segunda correlação é estatisticamente diferente de zero, mas pequena em magnitude. Substantivamente, HHI e exposição externa oferecem informações distintas.

Esse resultado modifica a interpretação de versões anteriores do estudo. A correlação positiva moderada entre HHI e exposição Strength bruta não deve ser utilizada como evidência central, porque a robustez mostrou que parte relevante dessa relação decorria da auto-inclusão monetária.

# 9. Discordância concentração-exposição

A classificação histórica utilizava HHI abaixo do Q75 e exposição no Q75 ou acima. A estrutura é mantida por comparabilidade, mas a nomenclatura e a medida de exposição são corrigidas.

Não utilizar “baixa concentração” como sinônimo automático de `HHI < Q75`.

Preferir:

- **discordância concentração-exposição**;
- **exposição externa não capturada pelo HHI**.

## 9.1 Strength LOO

- 221 compradores;
- 16,41% dos elegíveis.

## 9.2 Degree LOO

- 237 compradores;
- 17,59% dos elegíveis.

A sobreposição entre as classificações Strength LOO e Degree LOO é 89,14%.

Sob independência entre duas classificações contínuas com cortes Q75, o benchmark mecânico para `HHI < Q75` e `exposição >= Q75` é 18,75%. Portanto, os percentuais observados não devem ser descritos como prevalência anormal. O resultado relevante é a existência de compradores cuja exposição externa não é resumida pelo HHI e a robustez da identificação entre duas medidas externalizadas.

O suplemento deve reportar também duas medidas contínuas de discordância:

- diferença entre percentil de exposição e percentil de HHI;
- resíduo da exposição após HHI normalizado.

# 10. Testes de estresse

Os testes de estresse respondem a uma pergunta diferente da exposição LOO. O objetivo é medir quanto da carteira dos compradores está ligado aos fornecedores de maior importância monetária sistêmica.

Ranking principal: Strength global bruto.

## 10.1 Cenário direcionado

Com perda mínima de 50% da carteira:

- remoção dos top 1%: 8,91% dos compradores severamente afetados;
- top 5%: 34,15%;
- top 10%: 48,26%.

## 10.2 Contrafactual aleatório ponderado por Strength

Para reduzir a objeção de que a comparação uniforme escolhe predominantemente fornecedores pequenos, executamos 1.000 sorteios sem reposição de igual `k`, com probabilidade de seleção proporcional ao Strength.

Para perda de pelo menos 50%:

- top 1% direcionado: 8,91%, contra média aleatória ponderada de 5,46%, intervalo empírico 2,5%-97,5% de 4,31%-6,61%;
- top 5%: 34,15%, contra 22,88%, intervalo de 20,34%-24,94%;
- top 10%: 48,26%, contra 38,52%, intervalo de 36,75%-40,31%.

O cenário direcionado permanece acima do contrafactual ponderado nas três escalas.

## 10.3 Concentração da massa sistêmica

Os top 1%, 5% e 10% por Strength concentram aproximadamente:

- 57,56%;
- 79,47%;
- 87,41%

da massa total de Strength observada.

O diagnóstico que remove número variável de fornecedores até atingir massa de Strength semelhante à dos top-k será apresentado apenas como descrição da concentração sistêmica. Ele não é um contrafactual comparável de superioridade do ataque, porque altera substancialmente o número de fornecedores removidos.

## 10.4 Limites

Os cenários não medem default, risco de crédito, capacidade produtiva, substituibilidade técnica, adaptação, renegociação ou interrupção efetiva de serviço público. Eles são testes mecânicos de exposição de carteira.

# 11. Persistência longitudinal com medidas externalizadas

A persistência foi recalculada com Strength LOO e Degree LOO para evitar depender da exposição Strength bruta.

## 11.1 Abril para maio

Nos 1.013 compradores comuns:

- Strength LOO: `rho = 0,8962`;
- Degree LOO: `rho = 0,9091`;
- retenção do quartil superior Strength LOO: 88,19%;
- retenção do quartil superior Degree LOO: 89,37%;
- retenção da discordância Strength LOO: 85,96%;
- retenção da discordância Degree LOO: 87,57%;
- estabilidade do quadrante completo Strength LOO: 86,48%;
- estabilidade do quadrante completo Degree LOO: 87,07%.

Houve 197 entrantes e nenhuma saída de elegibilidade.

## 11.2 Maio para junho

Nos 1.210 compradores comuns:

- Strength LOO: `rho = 0,9266`;
- Degree LOO: `rho = 0,9416`;
- retenção do quartil superior Strength LOO: 91,75%;
- retenção do quartil superior Degree LOO: 94,39%;
- retenção da discordância Strength LOO: 90,40%;
- retenção da discordância Degree LOO: 90,61%;
- estabilidade do quadrante completo Strength LOO: 89,50%;
- estabilidade do quadrante completo Degree LOO: 90,41%.

Houve 137 entrantes e nenhuma saída.

A persistência aumenta de abril-maio para maio-junho nas duas medidas. Os indicadores devem ser interpretados como sinais de triagem persistentes, não como rótulos permanentes de risco.

# 12. Efeito de composição

A expansão da coorte altera as estatísticas transversais e deve ser separada da mudança dentro dos compradores persistentes.

Entre maio e junho:

- elegíveis: 1.210 para 1.347;
- novos elegíveis: 137;
- saídas: zero;
- HHI agregado mediano: 0,2420 para 0,2365;
- HHI mediano dos compradores comuns em junho: 0,2233;
- HHI mediano dos entrantes: 0,3606.

Os entrantes de junho também apresentaram exposição externa mediana inferior à dos compradores comuns:

- Strength LOO: 0,2048 nos entrantes contra 0,3106 nos comuns;
- Degree LOO: 0,1996 contra 0,3044.

Assim, a composição da coorte afeta simultaneamente concentração e exposição. Toda análise temporal deve separar subamostra comum, entrantes, saídas e estatística transversal total.

# 13. Integração SICONFI

A integração fiscal é complementar. Na janela janeiro-junho:

- 1.346 compradores possuem vínculo municipal único;
- 1.335 possuem despesa empenhada disponível;
- cobertura: 99,18%;
- 725 municípios possuem total de despesa empenhada.

Modelos fiscais são associativos e não recebem interpretação causal.

# 14. Robustez econométrica de concentração

A especificação histórica é:

`HHI_norm_b = beta0 + beta1 ln(Pop_b) + beta2 ln(DespesaPC_b) + beta3 ln(NFornec_b) + beta4 ln(InstrPorFornec_b) + Regiao + erro_b`

Como população e despesa per capita variam no nível municipal, acrescentamos:

1. WLS no nível comprador com peso `1/N_m`, em que `N_m` é o número de compradores elegíveis do município;
2. OLS agregado ao município;
3. CR1 e CR4 como outcomes alternativos.

## 14.1 HHI normalizado ponderado

WLS:

- população: 0,0206, positiva e significativa;
- despesa per capita: 0,00045, não significativa;
- número de fornecedores: -0,0715, significativo;
- recorrência: 0,0301, `p = 0,0716`.

Agregado ao município:

- população: 0,0207, positiva e significativa;
- despesa per capita: não significativa;
- número de fornecedores: -0,0753, significativo;
- recorrência: 0,0264, `p = 0,227`.

A significância da recorrência para HHI observada na especificação histórica não é robusta à equalização do peso municipal.

CR1 e CR4 preservam o sinal positivo de população, a ausência de associação robusta com despesa per capita e o sinal negativo do número de fornecedores. Recorrência varia entre especificações.

O número de fornecedores deve ser tratado como controle estrutural, pois possui relação matemática com medidas de concentração. Seu coeficiente não será interpretado causalmente.

# 15. Modelos associativos de exposição externa

Os outcomes preferenciais são Strength LOO e Degree LOO.

## 15.1 Strength LOO

WLS com peso municipal:

- população: -0,0311, significativa;
- despesa per capita: -0,0664, `p = 0,0269`;
- número de fornecedores: 0,0072, não significativo;
- recorrência: 0,1556, altamente significativa.

Agregado ao município:

- população: -0,0298, significativa;
- despesa per capita: -0,0638, `p = 0,0347`;
- número de fornecedores: 0,0104, não significativo;
- recorrência: 0,2076, altamente significativa.

## 15.2 Degree LOO

WLS:

- população: -0,0276, significativa;
- despesa per capita: -0,0563, `p = 0,0608`;
- número de fornecedores: -0,0055, não significativo;
- recorrência: 0,2009, altamente significativa.

Agregado ao município:

- população: -0,0260, significativa;
- despesa per capita: -0,0531, `p = 0,0775`;
- número de fornecedores: aproximadamente zero, não significativo;
- recorrência: 0,2694, altamente significativa.

## 15.3 Interpretação

A conclusão histórica de associação positiva entre número de fornecedores e exposição Strength não sobrevive à externalização e é abandonada como resultado substantivo.

Recorrência, por outro lado, permanece positiva nas quatro especificações externalizadas. A formulação adequada é:

> **recorrência contratual apresenta associação frágil com concentração local, mas associação positiva e consistente com exposição externa a fornecedores conectados a outros compradores.**

A associação permanece não causal.

# 16. Síntese dos resultados

A evidência janeiro-junho sustenta seis pontos:

1. concentração monetária e concentração por frequência são dimensões distintas;
2. Strength bruto mede importância sistêmica monetária, mas não é uma medida limpa de exposição externa do comprador;
3. Strength LOO e Degree LOO convergem fortemente entre si;
4. HHI e exposição externa apresentam baixa redundância;
5. a discordância concentração-exposição é robusta à escolha entre Strength LOO e Degree LOO e é longitudinalmente persistente;
6. ataques aos maiores fornecedores por Strength permanecem mais severos do que sorteios aleatórios de igual tamanho ponderados por Strength.

Nos modelos complementares, recorrência é o contraste mais estável entre as dimensões: frágil para concentração local e forte para exposição externa.

# 17. Implicações para screening

Um painel baseado apenas em HHI pode omitir dimensão relevante da dependência. A interpretação recomendada combina concentração local e exposição externa:

| Concentração local | Exposição externa | Interpretação de screening |
|---|---|---|
| menor | menor | carteira relativamente diversificada e fornecedores menos centrais externamente |
| maior | menor | dependência predominantemente local |
| menor | maior | exposição externa não capturada pelo HHI |
| maior | maior | concentração local combinada com exposição externa elevada |

Os quadrantes são instrumentos de triagem. Avaliação de risco material exige informação adicional sobre objeto contratado, criticidade, substituibilidade, capacidade operacional e contexto institucional.

# 18. Limitações

- a janela janeiro-junho é uma coorte parcial de publicações;
- instrumentos assinados no período podem ser publicados posteriormente;
- `valorInicial` não representa execução financeira;
- Strength representa escala monetária observada, não capacidade produtiva;
- Degree representa alcance institucional, não substituibilidade;
- centralidade não mede probabilidade de falha;
- stress tests não modelam adaptação, substituição ou renegociação;
- a rede está condicionada à cobertura observada do PNCP;
- o escopo é municipal e do Poder Executivo;
- modelos fiscais são associativos;
- nenhuma métrica implica fraude, favorecimento ou conluio.

# 19. Conclusão

A dependência de fornecedores nas compras públicas municipais não se reduz à concentração interna das carteiras. O principal resultado metodológico do estudo é que importância sistêmica do fornecedor e exposição externa do comprador precisam ser separadas. A exposição baseada diretamente em Strength global era fortemente influenciada pela contribuição monetária do próprio comprador. Ao retirar essa contribuição, Strength LOO e Degree LOO passam a fornecer medidas convergentes de exposição externa e apresentam relação muito pequena com o HHI.

A correção não enfraquece a tese central. Ao contrário, torna mais nítida a existência de duas dimensões distintas: concentração local e exposição externa. A classificação de discordância permanece presente, é semelhante sob Strength LOO e Degree LOO e apresenta alta persistência entre abril e junho.

Os testes de estresse preservam outra função do Strength bruto. Os fornecedores de maior Strength concentram parcela elevada da massa monetária da rede e sua remoção produz perdas superiores às observadas em sorteios aleatórios de igual tamanho ponderados pelo próprio Strength. Esse resultado deve ser interpretado como vulnerabilidade mecânica da estrutura observada, não como previsão de falha.

O framework resultante combina concentração local, exposição externa e stress testing. O segundo paper aplicará exatamente essa arquitetura ao ano completo de 2025 para testar estabilidade temporal, efeito de composição, expansão da rede e sensibilidade às publicações tardias.

# Referências recentes de posicionamento

Fountoukidis, I., Dafli, E., Antoniou, I., & Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160.

Sturm, N. F., Candia, C., Damásio, B., et al. (2025). High earnings through firm influence: the role of hierarchical structures in public procurement. *EPJ Data Science*, 14, 27. https://doi.org/10.1140/epjds/s13688-025-00543-z

Fonseca, F. T. (2025). *Patterns in Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil*. Master’s dissertation, NOVA Information Management School.

# Reprodutibilidade

Scripts:

- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`
- `scripts/calcular_exposicao_loo_generica.py`
- `scripts/diagnosticos_longitudinais_loo_jan_jun_2025.py`

Resultados principais de robustez:

- `results/robustez_estrutural_2025_06/`
- `results/robustez_modelos_municipio_2025_06/`
- `results/exposicao_loo_2025_04/`
- `results/exposicao_loo_2025_05/`
- `results/exposicao_loo_2025_06/`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/`

Logs auditáveis:

- `results/robustez_estrutural_2025_06/log_execucao.txt`
- `results/robustez_modelos_municipio_2025_06/log_execucao.txt`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/log_execucao.txt`
