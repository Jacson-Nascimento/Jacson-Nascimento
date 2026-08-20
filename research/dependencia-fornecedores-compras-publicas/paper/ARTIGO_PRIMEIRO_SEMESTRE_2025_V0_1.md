# Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidências do Primeiro Semestre de 2025

**Structural Supplier Dependency in Municipal Public Procurement: Evidence from the First Half of 2025**

**Jacson Cruz do Nascimento**

> Versão de trabalho v0.1. O recorte empírico utiliza instrumentos assinados em 2025 e observados nas publicações do PNCP entre 1º de janeiro e 30 de junho de 2025. Por existirem publicações tardias, a base não deve ser interpretada como estoque definitivamente fechado de todas as contratações assinadas no primeiro semestre.

## Resumo

A concentração de fornecedores em compras públicas pode ser avaliada por participações monetárias dentro da carteira de cada comprador, mas essa perspectiva local não informa, por si só, se os fornecedores relevantes para um órgão também ocupam posições centrais no sistema de contratação. Este estudo combina medidas de concentração da carteira, recorrência contratual e exposição estrutural em uma rede bipartida comprador–fornecedor para examinar compradores públicos municipais observados no Portal Nacional de Contratações Públicas (PNCP) no primeiro semestre de 2025. A base pública minimizada reúne 105.582 instrumentos de fornecedores pessoa jurídica, dos quais 98.438 foram assinados em 2025. Foram calculadas métricas para 2.349 compradores institucionais e definida uma amostra analítica principal de 1.347 compradores com pelo menos três fornecedores e cinco instrumentos. O HHI monetário mediano é 0,2365, enquanto o HHI normalizado mediano é 0,1563 e o número efetivo mediano de fornecedores é 4,23. Em 98,14% dos compradores, a concentração por valor supera a concentração por frequência. A correlação entre HHI normalizado e exposição a fornecedores de elevado Strength global é moderada (ρ=0,4081), e 13,14% dos compradores combinam concentração relativa abaixo do quartil superior com exposição estrutural acima do quartil superior. Simulações de remoção mostram que a exclusão direcionada dos 10% de fornecedores de maior Strength deixa 48,26% dos compradores com perda de pelo menos metade da carteira observada, contra 4,08% em remoções aleatórias de mesmo tamanho. O ranking de exposição apresenta elevada persistência longitudinal: entre maio e junho, 90,76% dos compradores no quartil superior permanecem nesse grupo. Na integração PNCP–SICONFI, a cobertura de despesa empenhada alcança 99,18% da amostra com vínculo municipal único. Modelos associativos indicam relação negativa e persistente entre número de fornecedores e HHI normalizado, enquanto recorrência contratual se mostra mais consistentemente associada à exposição estrutural do que à concentração local. Os resultados sugerem que dependência de fornecedores é multidimensional e que indicadores locais de concentração podem deixar de capturar vulnerabilidades associadas à posição sistêmica dos fornecedores.

**Palavras-chave:** compras públicas; fornecedores; concentração; HHI; análise de redes; PNCP; SICONFI; vulnerabilidade estrutural.

## Abstract

Supplier dependency in public procurement can be assessed through monetary concentration within each buyer's portfolio, but this local perspective does not reveal whether important suppliers also occupy central positions in the broader procurement system. This study combines portfolio concentration, contractual recurrence, and structural exposure in a bipartite buyer–supplier network to examine municipal public buyers observed in Brazil's National Public Procurement Portal (PNCP) during the first half of 2025. The minimized public dataset contains 105,582 instruments involving corporate suppliers, of which 98,438 were signed in 2025. Metrics were calculated for 2,349 institutional buyers, and the main analytical sample includes 1,347 buyers with at least three suppliers and five instruments. Median monetary HHI is 0.2365, median normalized HHI is 0.1563, and the median effective number of suppliers is 4.23. For 98.14% of buyers, value concentration exceeds frequency concentration. The correlation between normalized HHI and exposure to suppliers with high global Strength is moderate (ρ=0.4081), while 13.14% of buyers combine relatively low portfolio concentration with high structural exposure. Targeted removal simulations show that removing the top 10% of suppliers by global Strength leaves 48.26% of buyers exposed to losses of at least half of their observed portfolio, compared with 4.08% under equally sized random removals. Structural exposure rankings are highly persistent over time: from May to June, 90.76% of buyers in the top quartile remain there. The PNCP–SICONFI integration covers committed expenditure for 99.18% of buyers with an unambiguous municipal link. Associative models show a persistent negative relationship between the number of suppliers and normalized HHI, whereas contractual recurrence is more consistently associated with structural exposure than with local concentration. The results suggest that supplier dependency is multidimensional and that local concentration measures may fail to capture vulnerabilities related to suppliers' systemic positions.

**Keywords:** public procurement; suppliers; concentration; HHI; network analysis; PNCP; structural vulnerability.

# 1. Introdução

Compras públicas organizam relações econômicas entre órgãos compradores e fornecedores privados e, por essa razão, podem gerar dependências que não são integralmente visíveis em indicadores tradicionais de concentração. Um comprador pode apresentar número elevado de fornecedores e concentração local aparentemente moderada, mas continuar exposto a empresas que ocupam posição central em várias carteiras do sistema. Da mesma forma, a frequência de contratação pode sugerir diversificação formal sem que os valores contratados estejam distribuídos de maneira equivalente.

A distinção entre concentração local e exposição estrutural é relevante para governança, planejamento de compras, gestão de riscos e auditoria. A concentração monetária descreve como o gasto de um comprador se distribui entre seus fornecedores. A análise de redes adiciona outra dimensão: identifica fornecedores que conectam múltiplos compradores ou concentram valor em escala global. Em princípio, duas organizações com o mesmo HHI podem apresentar vulnerabilidades diferentes se uma delas depender de fornecedores periféricos e a outra de fornecedores centrais no sistema.

Este artigo investiga essa distinção no contexto das compras públicas municipais brasileiras observadas no Portal Nacional de Contratações Públicas (PNCP). A pergunta central é: **em que medida medidas locais de concentração da carteira capturam — ou deixam de capturar — a exposição dos compradores públicos a fornecedores globalmente centrais, e quão persistente e relevante é essa exposição quando conjuntos centrais de fornecedores são removidos da rede de contratação?**

O estudo contribui de forma empírica e institucional. Não se reivindica originalidade no uso isolado do HHI, de redes bipartidas, de Degree, de Strength ou da comparação entre valor e frequência. A contribuição está em integrar essas dimensões no nível do comprador institucional, explorar características próprias do PNCP — incluindo a distinção entre órgão do instrumento, unidade executora e contratação de origem —, simular perdas de carteira sob choques coletivos e combinar os indicadores com controles fiscais do SICONFI.

O recorte temporal é deliberadamente intermediário. São analisados instrumentos assinados em 2025 e observados nas publicações do PNCP entre janeiro e junho. Como instrumentos assinados nesse período podem ser publicados posteriormente, os resultados não representam o fechamento definitivo de 2025 nem de todas as contratações assinadas no primeiro semestre. A análise deve ser entendida como evidência semestral de uma coorte observada e como primeira etapa de um programa empírico que será posteriormente ampliado para o ano completo.

# 2. Literatura e posicionamento da contribuição

A mensuração de concentração de fornecedores por meio de índices derivados de participações econômicas possui antecedentes na literatura de supply-base concentration. Sharma et al. (2026), por exemplo, utilizam HHI adaptado às participações dos fornecedores nos custos de insumos do comprador. No campo de compras públicas, Fountoukidis (2026) documenta divergência entre participação por número de contratos e captura de valor no contexto europeu, enquanto Fountoukidis et al. (2026) combinam concentração e persistência de relações em um índice de fechamento institucional. Assim, nem a concentração monetária, nem a divergência valor–contagem, nem a repetição contratual são tratadas neste estudo como métricas inéditas.

A análise de redes em compras públicas também possui aplicações anteriores. Fonseca (2025) examina contratações públicas federais brasileiras como redes comprador–fornecedor e utiliza medidas clássicas de centralidade. A literatura internacional igualmente emprega redes para estudar seleção repetida, relações persistentes, estrutura competitiva e centralização das compras.

O presente estudo diferencia-se pelo desenho integrado. Primeiro, a unidade principal é o CNPJ institucional do comprador do instrumento, evitando agregar automaticamente órgãos distintos localizados no mesmo município. Segundo, a concentração local é comparada com a exposição do comprador à centralidade global dos fornecedores. Terceiro, são simuladas perdas de carteira após remoções direcionadas e aleatórias. Quarto, a estabilidade dos rankings é testada ao longo da expansão mensal da coorte. Quinto, indicadores de compras são combinados a variáveis fiscais municipais provenientes do SICONFI.

Esse posicionamento é deliberadamente conservador. O estudo não se apresenta como a primeira análise de redes do PNCP, nem propõe um novo HHI. A contribuição potencial reside na integração das medidas, na adaptação ao desenho institucional brasileiro, na comparação entre vulnerabilidade local e sistêmica e na construção de um pipeline reproduzível.

# 3. Dados e construção da amostra

## 3.1 PNCP

A principal fonte é a API pública de contratos do PNCP. A coleta é realizada por data de publicação, com paginação, tentativas automáticas em caso de falha e persistência de checkpoints. Para cada instrumento são preservados, entre outros campos, o identificador `numeroControlePNCP`, a contratação de origem, o CNPJ do órgão/entidade, o código IBGE e o nome do município da unidade, o identificador do fornecedor, o tipo de pessoa, `valorInicial`, `valorGlobal`, data de assinatura e data de publicação.

A chave do instrumento é `numeroControlePNCP`. A contratação de origem não é utilizada como chave de deduplicação porque uma mesma compra pode gerar vários instrumentos e envolver fornecedores diferentes. A unidade comprador é o CNPJ institucional do órgão/entidade do instrumento. Essa escolha evita confundir localização territorial da unidade executora com identidade econômica do comprador.

A base pública identificada é restrita a fornecedores pessoa jurídica. Registros envolvendo pessoa física ou pessoa estrangeira são mantidos apenas em diagnósticos agregados e em cópia privada para testes de robustez, reduzindo republicação desnecessária de identificadores pessoais.

## 3.2 Recorte temporal

O artigo utiliza publicações observadas entre 1º de janeiro e 30 de junho de 2025 e, para a análise econômica principal, mantém instrumentos com data de assinatura em 2025 e valor inicial positivo. A data de publicação organiza a captura; a data de assinatura define o pertencimento econômico ao exercício.

Essa distinção é necessária porque a distribuição do atraso de publicação apresenta cauda longa. Consequentemente, a coorte semestral não deve ser interpretada como base definitivamente completa de todos os instrumentos assinados até junho. A expansão posterior da coleta será utilizada para avaliar o efeito de publicações tardias.

## 3.3 SICONFI e integração municipal

As variáveis fiscais provêm da API de Dados Abertos do SICONFI, especialmente da Declaração das Contas Anuais (DCA) de 2025. A integração utiliza o código IBGE municipal e preserva apenas vínculos territoriais não ambíguos para os modelos principais. População e despesa empenhada são usadas para construir controles de escala, incluindo despesa empenhada per capita.

No acumulado até junho, 1.346 compradores elegíveis apresentam vínculo municipal único, dos quais 1.335 possuem despesa empenhada disponível, correspondendo a 99,18% de cobertura na amostra fiscal utilizada.

## 3.4 Escala da base

A base acumulada janeiro–junho contém 105.582 instrumentos PJ únicos. Destes, 98.438 foram assinados em 2025. Foram calculadas métricas para 2.349 compradores institucionais. A especificação principal utiliza 1.347 compradores com pelo menos três fornecedores e cinco instrumentos, critério escolhido para reduzir instabilidade mecânica em carteiras extremamente pequenas. Cortes mais exigentes são avaliados como robustez.

# 4. Metodologia

## 4.1 Concentração monetária da carteira

Para cada comprador `b` e fornecedor `s`, o valor agregado da relação é:

`V_bs = Σ_k V_k`,

onde `V_k` é o `valorInicial` positivo do instrumento `k`. A participação monetária do fornecedor na carteira do comprador é:

`q_bs = V_bs / Σ_s V_bs`.

O HHI monetário é:

`HHI_b = Σ_s q_bs²`.

Também são calculados CR1, CR4 e o número efetivo de fornecedores:

`N_eff,b = 1 / HHI_b`.

Como o limite inferior do HHI depende do número de fornecedores, utiliza-se adicionalmente uma versão normalizada:

`HHI_norm,b = (HHI_b - 1/N_b) / (1 - 1/N_b)`, para `N_b > 1`.

## 4.2 Concentração por frequência

Substituindo participações monetárias por participações no número de instrumentos, obtém-se `CountHHI`. A comparação entre `PortfolioHHI` e `CountHHI` é usada como caracterização da diferença entre diversificação formal de contratações e distribuição econômica do valor.

## 4.3 Rede comprador–fornecedor

Constrói-se uma rede bipartida entre compradores e fornecedores, ponderada pelo valor agregado das relações. Para cada fornecedor, são calculados:

- `Degree`: número de compradores distintos atendidos;
- `Strength`: soma dos valores de suas relações na rede;
- `Reach`: proporção dos compradores conectados ao fornecedor.

O ranking principal de vulnerabilidade utiliza `Strength` calculado na rede global observada. `Degree` é mantido como medida complementar.

## 4.4 Exposição estrutural do comprador

A exposição de cada comprador à centralidade dos seus fornecedores é calculada ponderando o percentil global de centralidade pela participação monetária local:

`ExposureStrength_b = Σ_s q_bs PStrength_s`.

Esse indicador é distinto do HHI. O HHI mede concentração dentro da carteira; a exposição mede quanto do valor da carteira está associado a fornecedores centrais no sistema.

Define-se como **exposição estrutural oculta** a combinação de HHI normalizado abaixo do quartil superior e exposição Strength acima do quartil superior da amostra elegível. O termo é descritivo e não implica irregularidade, risco de crédito ou indisponibilidade efetiva.

## 4.5 Simulações de choque

Para um conjunto removido de fornecedores `R`, a perda de carteira do comprador é:

`Loss_b(R) = Σ_{s∈R} q_bs`.

São avaliadas remoções de 1%, 5% e 10% dos fornecedores globais. O cenário principal remove fornecedores em ordem decrescente de Strength. O contrafactual utiliza 1.000 remoções aleatórias de mesmo tamanho, com semente pseudoaleatória fixa para replicabilidade. Um comprador é classificado como severamente exposto quando `Loss_b ≥ 0,50`.

As simulações são mecânicas: não modelam substituição de fornecedor, renegociação, estoques, capacidade produtiva, risco de crédito ou continuidade real do serviço.

## 4.6 Persistência longitudinal

Como a base é construída mês a mês, são comparados rankings e quadrantes entre janelas acumuladas consecutivas. Utilizam-se correlação de Spearman, retenção no quartil superior e transição entre quadrantes `concentração × exposição`. A análise separa compradores persistentes de novos elegíveis para evitar confundir mudança individual com efeito de composição da amostra.

## 4.7 Modelos associativos

A especificação principal para concentração é:

`HHI_norm_b = β0 + β1 ln(Pop_b) + β2 ln(DespesaPC_b) + β3 ln(NFornec_b) + β4 ln(InstrPorFornec_b) + Região + ε_b`.

São estimados OLS com erros-padrão agrupados por município e efeitos de macrorregião. Fractional logit é utilizado como robustez funcional. Modelos análogos são estimados para exposição Strength. As estimativas são interpretadas como associações, não como efeitos causais.

# 5. Resultados

## 5.1 Concentração local e divergência valor–frequência

Na regra principal 3/5, o HHI monetário mediano é 0,2365 e o HHI normalizado mediano é 0,1563. O número efetivo mediano é 4,23 fornecedores. O CR1 mediano é 38,37% e o CR4 mediano é 80,37%, indicando que os quatro maiores fornecedores respondem por parcela substancial do valor contratado na carteira mediana.

A concentração por frequência é significativamente menor: o CountHHI mediano é 0,0816 e o CountHHI normalizado mediano é 0,00682. Em 98,14% dos compradores, o HHI monetário é superior ao HHI por frequência. Portanto, o número de instrumentos e o número nominal de fornecedores oferecem uma imagem de diversificação muito maior do que a distribuição econômica do valor.

## 5.2 Concentração local e exposição estrutural são dimensões distintas

A correlação de Spearman entre HHI normalizado e exposição Strength global é 0,4081. A associação é positiva, mas longe de redundância. Entre os 1.347 compradores elegíveis, 177 — 13,14% — apresentam concentração relativa abaixo do quartil superior e exposição estrutural acima do quartil superior.

Esse quadrante é substantivamente relevante para triagem: um comprador pode não parecer excepcionalmente concentrado quando observado isoladamente e, ainda assim, direcionar parcela relevante da carteira a fornecedores que ocupam posição central em muitas outras relações da rede.

## 5.3 Vulnerabilidade a choques coletivos

A diferença entre remoções direcionadas e aleatórias é elevada. Com limiar de perda de 50% da carteira:

| Parcela de fornecedores removidos | Strength direcionado | Aleatório médio |
|---:|---:|---:|
| 1% | 8,91% | 0,32% |
| 5% | 34,15% | 1,79% |
| 10% | 48,26% | 4,08% |

A remoção direcionada dos 10% de fornecedores com maior Strength deixa quase metade dos compradores severamente expostos, enquanto o mesmo número de fornecedores removidos aleatoriamente afeta, em média, cerca de 4%.

Análises anteriores de criticidade individual mostram que o efeito não é explicado por um único fornecedor dominante. A vulnerabilidade emerge principalmente da remoção conjunta de um conjunto central de fornecedores. Por isso, o resultado deve ser interpretado como vulnerabilidade estrutural coletiva, e não como existência de um “superfornecedor” sistêmico isolado.

## 5.4 Persistência do sinal de exposição

A exposição estrutural apresenta elevada estabilidade conforme a janela de dados se expande. Entre maio e junho, nos 1.210 compradores comuns, a correlação de Spearman do ranking de ExposureStrength é 0,9570. Entre os compradores no quartil superior em maio, 90,76% permanecem no quartil superior em junho. Dos 153 compradores classificados como exposição estrutural oculta em maio, 132 permanecem no mesmo quadrante, retenção de 86,27%. O quadrante completo é estável para 88,68% da amostra comum.

Esses resultados apoiam o uso das métricas como sinais de triagem dinâmica. A alta persistência, entretanto, não autoriza transformá-las em rótulos permanentes de risco: mudanças na rede, na composição das compras e na cobertura dos dados podem alterar a classificação.

## 5.5 Efeito de composição

Entre maio e junho, o número de compradores elegíveis aumenta de 1.210 para 1.347. Os 137 novos elegíveis entram mais concentrados: o HHI mediano desses entrantes é 0,3606, enquanto o HHI dos compradores comuns em junho é 0,2233. Dentro da subamostra comum, o HHI cai medianamente 0,00828.

Portanto, a dinâmica agregada não deve ser lida apenas pela mediana transversal. Novos compradores tendem a entrar na amostra quando atingem o critério mínimo com carteiras ainda pequenas, elevando mecanicamente sua concentração. Separar incumbentes e entrantes evita atribuir ao mesmo comprador uma mudança que decorre apenas da composição da coorte.

## 5.6 Integração fiscal e modelos associativos

Na amostra fiscal, 1.335 compradores possuem dados de despesa empenhada e população, distribuídos em 725 municípios. Os fatores de inflação da variância permanecem baixos, aproximadamente entre 1,14 e 1,50.

No OLS para HHI normalizado, população apresenta coeficiente positivo (`β=0,02482`) e número de fornecedores coeficiente negativo (`β=-0,06754`), ambos estatisticamente significativos. Despesa per capita não apresenta associação robusta. Recorrência (`ln instrumentos por fornecedor`) é positiva e significativa no OLS de janeiro–junho (`β=0,02752; p=0,033`), mas não no fractional logit (`β=0,12177; p=0,123`).

A trajetória mensal mostra que esse resultado de recorrência sobre HHI não é estável: a variável é significativa em apenas uma de cinco janelas no OLS e em nenhuma de cinco no fractional logit. Assim, não há base para tratá-la como determinante persistente da concentração local.

O contraste aparece no modelo de ExposureStrength. Recorrência apresenta coeficiente positivo e altamente significativo (`β=0,04687`) e mantém sinal positivo e significância nas quatro janelas em que o modelo está disponível. O número de fornecedores também se associa positivamente à exposição estrutural, embora se associe negativamente ao HHI local.

Esse é um dos resultados centrais do estudo: **ampliar a base de fornecedores está associado a menor concentração local, mas uma carteira mais ampla e recorrente pode permanecer exposta a fornecedores globalmente centrais**.

# 6. Robustez

Os resultados foram submetidos a diferentes verificações. A sensibilidade aos critérios de elegibilidade mostra que as conclusões qualitativas persistem em cortes mais restritivos, embora o nível absoluto do HHI caia quando se exigem carteiras maiores. Esse comportamento reforça a necessidade de reportar HHI normalizado e não interpretar um único limiar como parâmetro natural.

A exclusão de empenhos praticamente não altera a concentração monetária nem as simulações por Strength. Empenhos representam parcela material do número de linhas, mas fração pequena do valor observado. Uma especificação conservadora que colapsa `compra × comprador × fornecedor` ao maior instrumento também preserva os principais resultados.

A substituição de `valorInicial` por `valorGlobal` produz resultados muito próximos porque, na ampla maioria dos instrumentos com ambos os campos positivos, os valores coincidem. Casos de lag de publicação negativo foram mantidos na base principal e excluídos em sensibilidade; seu impacto nas métricas agregadas é desprezível.

Compras compartilhadas afetam mais fortemente medidas baseadas em Degree do que choques ordenados por Strength. Por esse motivo, Strength global é adotado como ordenação principal da vulnerabilidade e Degree permanece como medida complementar.

# 7. Implicações para auditoria, governança e gestão de riscos

Os resultados sugerem que monitoramento de fornecedores pode se beneficiar de uma arquitetura em camadas. O HHI local responde à pergunta “quanto do valor deste comprador está concentrado em poucos fornecedores?”. A exposição estrutural responde “quanto desta carteira está associada a fornecedores centrais no sistema?”. A simulação de choque responde “qual parcela da carteira ficaria diretamente exposta se um conjunto central de fornecedores fosse removido da rede observada?”.

Essas perguntas são relacionadas, mas não equivalentes. Para auditoria e controles, a principal utilidade está em priorização. Compradores com alta concentração local podem demandar análise da dependência econômica dentro da carteira. Compradores com exposição estrutural elevada podem demandar exame de contingência, substituibilidade, planejamento da contratação e concentração de capacidade em fornecedores amplamente conectados.

Nenhuma dessas métricas constitui evidência de fraude, direcionamento, favorecimento, falha de controle ou interrupção futura. Elas são sinais quantitativos que podem orientar seleção de objetos e aprofundamento analítico.

# 8. Limitações

A principal limitação é temporal. O recorte utiliza publicações observadas até 30 de junho de 2025 e, portanto, não captura necessariamente todos os instrumentos assinados no primeiro semestre que foram publicados posteriormente. O estudo não deve ser interpretado como fechamento anual ou semestral definitivo do PNCP.

A segunda limitação refere-se à presença territorial. O conjunto observado de compradores não é amostra probabilística dos municípios brasileiros. A adesão, intensidade de contratação e cronologia de publicação variam entre entes. As conclusões devem ser formuladas para compradores municipais observados no PNCP, evitando inferência automática para todos os municípios.

`valorInicial` representa valor contratual e não execução financeira. Strength depende da escala monetária observada e não mede capacidade produtiva ou risco de crédito. Centralidade também não mede substituibilidade técnica. As simulações de remoção não incorporam respostas adaptativas, contratação emergencial, renegociação, estoques ou entrada de novos fornecedores.

Os modelos PNCP–SICONFI são associativos. A significância estatística de uma covariável não identifica causalidade. Variáveis omitidas, seleção para a amostra observada e heterogeneidade institucional podem afetar as estimativas.

Por fim, este artigo é deliberadamente intermediário. A expansão para o segundo semestre e a captura de publicações tardias permitirão verificar se os padrões permanecem quando a rede se aproxima de uma observação anual mais completa.

# 9. Conclusão

A evidência do primeiro semestre mostra que dependência de fornecedores nas compras públicas municipais possui pelo menos três dimensões distintas: concentração monetária local, recorrência contratual e exposição estrutural em rede. O número de fornecedores e a frequência de instrumentos podem sugerir diversificação substancial, mas a distribuição do valor permanece muito mais concentrada: em 98,14% dos compradores elegíveis, o HHI monetário supera o HHI por frequência.

A análise de rede adiciona informação que o HHI não contém. Aproximadamente 13% dos compradores combinam concentração relativa não extrema com elevada exposição a fornecedores globalmente centrais. A remoção direcionada de conjuntos centrais produz perdas de carteira muito superiores às obtidas em contrafactuais aleatórios, e esse padrão permanece sob diferentes critérios de elegibilidade e especificações de instrumentos.

A dimensão estrutural também é temporalmente persistente. Rankings de ExposureStrength permanecem altamente correlacionados entre janelas consecutivas e a maior parte dos compradores mais expostos continua no quartil superior. Nos modelos associativos, número de fornecedores se relaciona de maneira estável com menor concentração local, enquanto recorrência se associa mais consistentemente à exposição estrutural do que ao HHI.

Em conjunto, os resultados indicam que uma carteira aparentemente diversificada não é necessariamente estruturalmente independente. Para gestão de riscos e auditoria, isso sugere que indicadores de concentração local devem ser complementados por medidas de posição sistêmica dos fornecedores e por análises de dependência coletiva. A extensão anual permitirá avaliar a robustez dessas conclusões com maior cobertura temporal e incorporar publicações tardias de instrumentos assinados em 2025.

# Disponibilidade de dados e código

O projeto utiliza dados públicos do PNCP, SICONFI e IBGE. Scripts, bases públicas minimizadas, manifestos, checksums, diagnósticos e resultados são versionados no diretório `research/dependencia-fornecedores-compras-publicas` do repositório do projeto. Identificadores de fornecedores pessoa física não são republicados na base pública. As decisões metodológicas e de qualidade possuem registros técnicos próprios.

# Referências preliminares

FONSECA, Fernanda da Trindade. *Patterns In Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil*. NOVA Information Management School, 2025. Dissertação de mestrado. Handle 10362/190144.

FOUNTOUKIDIS, I. *Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement*. 2026. SSRN 6897598. DOI: 10.2139/ssrn.6897598.

FOUNTOUKIDIS, I.; DAFLI, E.; ANTONIOU, I.; VARSAKELIS, N. *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. 2026. SSRN 6765160.

SHARMA, A.; SABOO, A. R.; BORAH, S. B.; ADHIKARY, A. Supplier concentration and firm performance: the role of relative size, relative reputation, and network position. *International Journal of Research in Marketing*, 2026. DOI: 10.1016/j.ijresmar.2026.01.006.

BRASIL. Portal Nacional de Contratações Públicas — PNCP. Dados Abertos e Manual de Integração.

BRASIL. Tesouro Nacional. SICONFI — Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro. API de Dados Abertos.

IBGE. Instituto Brasileiro de Geografia e Estatística. Códigos e informações municipais.
