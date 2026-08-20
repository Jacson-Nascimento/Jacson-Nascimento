# Paper 1 - janeiro a junho de 2025

## Título provisório recomendado

**Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição Externa em Rede e Testes de Estresse**

### Título em inglês

**Structural Supplier Dependency in Municipal Public Procurement: Portfolio Concentration, External Network Exposure, and Stress Tests**

## Resumo provisório

Este estudo investiga a dependência de fornecedores em compras públicas municipais a partir de duas dimensões distintas: concentração monetária dentro da carteira de cada comprador e exposição externa a fornecedores relevantes na rede global de contratação. Utilizamos dados do Portal Nacional de Contratações Públicas referentes a publicações de janeiro a junho de 2025, restringindo as métricas econômicas a instrumentos assinados em 2025 e a fornecedores pessoa jurídica. A unidade de comprador é o CNPJ institucional do órgão do Poder Executivo municipal. Medimos concentração por HHI, HHI normalizado, CR1, CR4 e número efetivo de fornecedores. Para separar a posição externa do fornecedor da contribuição do próprio comprador, construímos exposições leave-one-buyer-out baseadas em Strength e Degree. Os resultados mostram que a exposição Strength bruta contém forte componente de auto-inclusão, mas que as medidas externalizadas Strength LOO e Degree LOO apresentam elevada concordância entre si e baixa associação com a concentração local. O HHI normalizado praticamente não se correlaciona com Strength LOO, enquanto a classificação de discordância entre concentração e exposição permanece presente sob ambas as medidas externalizadas. Nos testes de estresse, a remoção direcionada dos fornecedores de maior Strength continua produzindo perdas superiores a um contrafactual aleatório de igual tamanho ponderado por Strength. Modelos associativos complementares mostram que recorrência contratual está fortemente associada à exposição externa, mas não de forma robusta à concentração local. Os resultados sugerem que dependência de fornecedores em compras públicas municipais não pode ser inferida apenas pela concentração observada dentro de cada carteira.

**Palavras-chave:** compras públicas; fornecedores; concentração; redes; dependência estrutural; PNCP; stress test; centralidade.

## 1. Introdução

A diversificação aparente de uma carteira de fornecedores não implica necessariamente baixa dependência estrutural. Um comprador público pode distribuir seu valor contratado entre várias empresas e, ainda assim, estar exposto a fornecedores que mantêm relações extensas com outros compradores ou concentram grande volume monetário no sistema observado. Inversamente, uma carteira localmente concentrada pode depender de fornecedores pouco relevantes fora daquela relação específica.

Essa distinção é importante porque medidas tradicionais de concentração, como o índice Herfindahl-Hirschman, respondem a uma pergunta local: como o valor da carteira de um comprador está distribuído entre seus fornecedores? Elas não respondem diretamente a outra pergunta: quão conectados ou sistemicamente relevantes são esses fornecedores fora da carteira focal?

Este artigo propõe tratar dependência de fornecedores em compras públicas municipais como um problema de pelo menos duas dimensões:

1. **concentração local da carteira**, baseada nas participações monetárias dos fornecedores dentro de cada comprador;
2. **exposição externa em rede**, baseada na posição dos fornecedores nas relações com os demais compradores, retirando a contribuição do próprio comprador focal.

A terceira camada do framework é o teste de estresse. Em vez de interpretar centralidade como probabilidade de falha, simulamos a perda mecânica de carteira associada à remoção de conjuntos de fornecedores estruturalmente relevantes e comparamos esses cenários com contrafactuais aleatórios.

A pergunta de pesquisa é:

> Em que medida medidas locais de concentração da carteira capturam, ou deixam de capturar, a exposição externa de compradores públicos municipais a fornecedores estruturalmente relevantes, e como essa diferença se manifesta sob choques coletivos simulados?

O artigo não interpreta concentração, centralidade ou recorrência como evidência de fraude, favorecimento, conluio, risco de crédito ou interrupção efetiva de serviço.

## 2. Contribuição e posicionamento

A contribuição não é o uso isolado de HHI, CR1, CR4, redes bipartidas, Degree, Strength, persistência ou ataques direcionados. Esses elementos já aparecem na literatura de concentração, cadeias de suprimento e análise de redes em compras públicas.

A contribuição está na integração, no nível do comprador público municipal, de:

- concentração monetária local da carteira;
- divergência entre valor e frequência contratual;
- posição sistêmica dos fornecedores;
- exposição externa leave-one-buyer-out;
- discordância entre concentração local e exposição externa;
- stress tests direcionados e contrafactuais aleatórios;
- persistência longitudinal do screening;
- integração complementar com variáveis fiscais municipais.

### 2.1 Literatura recente relevante

A revisão final deve dialogar explicitamente com:

**Fountoukidis, Dafli, Antoniou e Varsakelis (2026).** *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160. O estudo introduz um índice no nível da autoridade contratante que combina concentração, persistência e embeddedness das relações. A distinção do presente artigo está na separação entre concentração local e exposição externa à posição dos fornecedores, além dos testes de estresse coletivos.

**Sturm, Candia, Damásio et al. (2025).** *High earnings through firm influence: the role of hierarchical structures in public procurement*. EPJ Data Science, 14, 27. O trabalho mostra a utilidade de métricas de rede e centralidade para caracterizar posição e influência de firmas em compras públicas portuguesas. Ele deve ser usado para situar centralidade e análise de redes como literatura precedente, não como novidade isolada deste artigo.

**Fonseca (2025).** *Patterns in Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil*. Dissertação de mestrado, NOVA IMS. O estudo aplica análise de redes a contratações públicas federais brasileiras entre 2022 e meados de 2024, reforçando que a originalidade do presente trabalho não está em ser a primeira aplicação de network analysis a compras públicas brasileiras.

A versão final deve completar este bloco com literatura de supplier concentration, supply-network resilience e buyer-supplier embeddedness.

## 3. Dados e escopo

### 3.1 Fonte principal

A fonte de contratos é o Portal Nacional de Contratações Públicas, PNCP.

Janela operacional deste paper:

- publicações de 01/01/2025 a 30/06/2025;
- métricas econômicas restritas a instrumentos assinados em 2025;
- `valorInicial > 0`;
- esfera municipal;
- Poder Executivo;
- fornecedor identificado publicamente: pessoa jurídica.

A janela janeiro-junho é uma coorte parcial de publicações e não equivale ao ano de 2025 completo.

### 3.2 Unidade de comprador e chaves

Comprador principal: CNPJ institucional do órgão ou entidade do instrumento.

Chave de instrumento: `numeroControlePNCP`, materializada como `id_contrato`.

`numeroControlePNCPCompra` é utilizado somente como ligação com a compra e nunca como chave de deduplicação de instrumentos.

Município é dimensão territorial e fonte de controles, não substituto da unidade institucional de comprador.

### 3.3 Política de privacidade

A base pública identificada contém apenas fornecedores PJ. Registros PF e PE são utilizados exclusivamente em diagnósticos agregados e não têm CPF ou nome republicados.

### 3.4 Escala da amostra janeiro-junho

A coorte acumulada contém:

- 105.582 instrumentos PJ únicos publicados na janela;
- 98.438 instrumentos assinados em 2025;
- 2.349 compradores com métricas calculadas;
- 1.347 compradores elegíveis no critério principal de pelo menos 3 fornecedores e 5 instrumentos;
- 20.367 fornecedores na rede global.

## 4. Concentração local da carteira

Para comprador `b` e fornecedor `j`, seja `V_bj` o valor acumulado da relação e:

`w_bj = V_bj / sum_j(V_bj)`

O HHI monetário da carteira é:

`HHI_b = sum_j(w_bj^2)`

Com `N_b` fornecedores, o HHI normalizado é:

`HHI_norm_b = (HHI_b - 1/N_b) / (1 - 1/N_b)`

Também são calculados:

- CR1;
- CR4;
- número efetivo de fornecedores `Neff = 1/HHI`;
- CountHHI e CountHHI normalizado, baseados na frequência de instrumentos.

### 4.1 Resultados de concentração

Na amostra elegível 3/5:

- HHI monetário mediano: 0,2365;
- HHI normalizado mediano: 0,1563;
- CountHHI mediano: 0,0816;
- CountHHI normalizado mediano: 0,00682;
- número efetivo mediano de fornecedores: 4,23;
- CR1 mediano: 0,3837;
- CR4 mediano: 0,8037.

Em 98,14% dos compradores, o HHI monetário é superior ao HHI por frequência. O resultado indica que concentração de valor e concentração de contagem não são equivalentes. Ele não implica irregularidade.

## 5. Rede e distinção entre importância sistêmica e exposição externa

A rede é bipartida entre compradores institucionais e fornecedores PJ.

### 5.1 Strength global bruto

`Strength_j = sum_b(V_bj)`

Strength mede a massa monetária das relações observadas do fornecedor no sistema. Essa medida é adequada para ordenar fornecedores nos testes de estresse, pois a pergunta é quais fornecedores concentram mais valor no conjunto observado.

### 5.2 Degree global

`Degree_j = número de compradores distintos atendidos pelo fornecedor j`

Degree mede alcance institucional e é complementar ao Strength.

### 5.3 Problema de auto-inclusão na exposição do comprador

A exposição originalmente calculada com o Strength global bruto reutilizava o próprio valor `V_bj` para determinar a posição do fornecedor. A robustez leave-one-buyer-out mostrou que esse componente não é pequeno.

A correlação entre exposição Strength bruta e exposição Strength externalizada foi apenas `rho = 0,2647`. A retenção do quartil superior foi 38,87%, e a contribuição própria mediana ponderada do comprador ao Strength dos fornecedores de sua carteira foi 75,89%.

Por isso, o Strength bruto permanece a medida principal de **importância sistêmica do fornecedor**, mas deixa de ser a medida principal de **exposição externa do comprador**.

## 6. Exposição externa leave-one-buyer-out

Para cada comprador `b`, externalizamos a posição do fornecedor:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Os percentis são recalculados na rede ajustada ao comprador focal.

A exposição externa é:

`E_b^(S,LOO) = sum_j w_bj * PctRank_b(Strength_j^(-b))`

`E_b^(D,LOO) = sum_j w_bj * PctRank_b(Degree_j^(-b))`

Strength LOO é a medida preferencial. Degree LOO é complementar.

### 6.1 Validação cruzada das medidas externas

Strength LOO e Degree LOO apresentam elevada concordância entre si:

`rho = 0,9500`.

O Degree é especialmente estável à externalização: a correlação entre a exposição Degree original e Degree LOO é `rho = 0,9821`, com retenção de 89,61% do quartil superior.

Esses resultados mostram que alcance institucional do fornecedor é pouco sensível à retirada do comprador focal, enquanto a escala monetária Strength é fortemente afetada pela própria relação focal.

## 7. Concentração local e exposição externa não são redundantes

Após a correção LOO, a separação entre as dimensões torna-se mais clara.

A correlação entre HHI normalizado e Strength LOO é:

`rho = -0,0183`, `p = 0,502`.

Para Degree LOO:

`rho = -0,0763`, `p = 0,0051`.

Embora a segunda correlação seja estatisticamente diferente de zero, sua magnitude é pequena. Em termos substantivos, as duas medidas externas apresentam baixa redundância com a concentração local.

Esse resultado substitui a interpretação anterior baseada na correlação positiva moderada entre HHI e exposição Strength bruta, que estava parcialmente contaminada pela auto-inclusão monetária.

## 8. Discordância concentração-exposição

A classificação histórica utilizava HHI abaixo do Q75 e exposição no Q75 ou acima. O paper mantém essa estrutura por comparabilidade, mas muda a nomenclatura e a métrica de exposição.

Não utilizar “baixa concentração” como sinônimo automático de `HHI < Q75`.

Preferir:

- **discordância concentração-exposição**;
- **exposição externa não capturada pelo HHI**.

### 8.1 Resultados com medidas externalizadas

Com Strength LOO:

- 221 compradores;
- 16,41% dos 1.347 elegíveis.

Com Degree LOO:

- 237 compradores;
- 17,59% dos elegíveis.

A sobreposição entre os grupos Strength LOO e Degree LOO é 89,14%, o que mostra que a classificação externalizada é muito semelhante entre as duas medidas de rede.

O benchmark mecânico sob independência perfeita entre uma variável classificada abaixo do Q75 e outra acima do Q75 é 18,75%. Portanto, os percentuais de 16,41% e 17,59% não devem ser apresentados como incidência anormal. O resultado relevante é que existe um grupo identificável cuja posição externa não é resumida pelo HHI e que essa identificação é robusta à escolha entre Strength LOO e Degree LOO.

### 8.2 Robustez contínua

O suplemento deve reportar:

- diferença entre percentil de exposição e percentil de HHI;
- resíduo da exposição após HHI normalizado.

Essas medidas evitam depender exclusivamente de cortes por quartil.

## 9. Testes de estresse

Os testes de estresse respondem a uma pergunta diferente da exposição LOO. Eles avaliam a perda mecânica de carteira quando conjuntos de fornecedores sistemicamente importantes são removidos da rede observada.

Ranking principal: Strength global bruto.

### 9.1 Cenário principal histórico

Com perda mínima de 50% da carteira:

- top 1% dos fornecedores por Strength: 8,91% dos compradores severamente afetados;
- top 5%: 34,15%;
- top 10%: 48,26%.

O contrafactual uniforme histórico permanece no suplemento e na tabela principal de replicação.

### 9.2 Contrafactual aleatório ponderado por Strength

Para reduzir a objeção de que o ataque direcionado apenas escolhe fornecedores maiores, adicionamos 1.000 sorteios de igual `k` sem reposição, com probabilidade de seleção proporcional ao Strength.

Para perda de pelo menos 50% da carteira:

- top 1% direcionado: 8,91%, contra média ponderada de 5,46%, intervalo empírico de 2,5% a 97,5% entre 4,31% e 6,61%;
- top 5% direcionado: 34,15%, contra 22,88%, intervalo entre 20,34% e 24,94%;
- top 10% direcionado: 48,26%, contra 38,52%, intervalo entre 36,75% e 40,31%.

O padrão direcionado permanece acima do contrafactual mais exigente em todas as três escalas.

### 9.3 Concentração da massa sistêmica

Os top 1%, 5% e 10% por Strength concentram, respectivamente, aproximadamente:

- 57,56%;
- 79,47%;
- 87,41%

da massa total de Strength observada.

Esse resultado é descritivo de concentração sistêmica da rede e ajuda a explicar por que a perda associada aos maiores fornecedores é elevada.

O diagnóstico que remove número variável de fornecedores até reproduzir a mesma massa de Strength não será tratado como contrafactual de superioridade do ataque direcionado, pois ele exige remover uma fração muito maior de fornecedores e responde a outra pergunta.

### 9.4 Limites do stress test

Os cenários não medem:

- probabilidade de default;
- risco de crédito;
- capacidade produtiva;
- substituibilidade técnica;
- adaptação do comprador;
- renegociação;
- interrupção efetiva de serviço público.

Eles são testes mecânicos de exposição de carteira.

## 10. Persistência longitudinal

Os diagnósticos históricos abril-maio e maio-junho mostraram alta persistência dos rankings calculados com a especificação original. Contudo, como a exposição Strength bruta mostrou forte auto-inclusão, esses números deixam de constituir a evidência longitudinal principal do paper.

A versão final deverá recalcular a persistência do primeiro semestre com Strength LOO e Degree LOO, mantendo as séries históricas brutas apenas como diagnóstico de transição metodológica.

Essa alteração é uma correção metodológica motivada por robustez e deve ser registrada explicitamente, não ocultada.

## 11. Efeito de composição das coortes

Entre maio e junho:

- elegíveis: 1.210 para 1.347;
- novos elegíveis: 137;
- saídas: zero;
- HHI agregado mediano: 0,2420 para 0,2365;
- HHI mediano dos compradores comuns em junho: 0,2233;
- HHI mediano dos novos elegíveis em junho: 0,3606.

Dentro dos compradores comuns, o HHI caiu. Os entrantes, porém, chegaram mais concentrados e atuaram em sentido oposto na estatística transversal.

Por isso, toda análise temporal deve separar:

1. mudança na subamostra comum;
2. perfil dos entrantes;
3. eventuais saídas;
4. estatística transversal total.

## 12. Integração SICONFI

Na janela janeiro-junho:

- 1.346 compradores possuem vínculo municipal único;
- 1.335 possuem despesa empenhada disponível;
- cobertura: 99,18%;
- 725 municípios possuem total de despesa empenhada.

Os modelos fiscais são complementares e associativos.

## 13. Modelos de concentração e robustez municipal

A especificação histórica é:

`HHI_norm_b = beta0 + beta1 ln(Pop_b) + beta2 ln(DespesaPC_b) + beta3 ln(NFornec_b) + beta4 ln(InstrPorFornec_b) + Regiao + erro_b`

O modelo principal histórico usa erros agrupados por município. Como população e despesa per capita são municipais, adicionamos duas robustezes:

- WLS no comprador com peso `1/N_m`, onde `N_m` é o número de compradores elegíveis do município;
- OLS agregado ao município.

Também usamos CR1 e CR4 como outcomes alternativos ao HHI normalizado.

### 13.1 Resultados de concentração

No WLS ponderado por município:

- população: coeficiente 0,0206, positivo e significativo;
- despesa per capita: praticamente zero e não significativa;
- número de fornecedores: -0,0715, negativo e significativo;
- recorrência: 0,0301, `p = 0,0716`.

No modelo agregado ao município:

- população: 0,0207, positiva e significativa;
- despesa per capita: não significativa;
- número de fornecedores: -0,0753, negativo e significativo;
- recorrência: 0,0264, `p = 0,227`.

Portanto, a significância da recorrência para HHI observada na especificação histórica não é robusta à equalização do peso municipal.

O número de fornecedores deve permanecer tratado como controle estrutural, pois existe relação matemática entre amplitude da carteira e medidas de concentração. Sua significância não será interpretada como descoberta causal.

CR1 e CR4 preservam o sinal positivo de população, a ausência de associação robusta com despesa per capita e o sinal negativo do número de fornecedores. A recorrência varia entre especificações, reforçando a leitura de fragilidade para concentração local.

## 14. Modelos de exposição externa

A robustez econométrica foi recalculada usando Strength LOO e Degree LOO.

### 14.1 Strength LOO

WLS com peso municipal:

- população: -0,0311, significativa;
- despesa per capita: -0,0664, `p = 0,0269`;
- número de fornecedores: 0,0072, não significativo;
- recorrência: 0,1556, altamente significativa.

Modelo agregado ao município:

- população: -0,0298, significativa;
- despesa per capita: -0,0638, `p = 0,0347`;
- número de fornecedores: 0,0104, não significativo;
- recorrência: 0,2076, altamente significativa.

### 14.2 Degree LOO

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

### 14.3 Interpretação

A conclusão anterior de que maior número de fornecedores estaria positivamente associado à exposição Strength não resiste à externalização. Esse efeito desaparece com Strength LOO e Degree LOO.

Em contraste, recorrência contratual permanece positiva e forte nas quatro especificações externalizadas. Esse é um resultado organizador mais defensável:

> **recorrência não apresenta associação robusta com concentração local, mas está consistentemente associada à exposição externa a fornecedores conectados aos demais compradores.**

Esse resultado é associativo. Não implica que recorrência cause exposição, nem que exposição cause recorrência.

## 15. Síntese dos resultados

Os resultados sustentam cinco conclusões principais:

1. concentração monetária e concentração por contagem são distintas;
2. Strength bruto é útil para importância sistêmica e stress testing, mas não é uma medida limpa de exposição externa do comprador;
3. depois de externalizar a contribuição do comprador, HHI e exposição de rede tornam-se praticamente não redundantes;
4. Strength LOO e Degree LOO convergem fortemente entre si e identificam quase o mesmo grupo de discordância concentração-exposição;
5. ataques aos maiores fornecedores por Strength permanecem mais severos que um contrafactual aleatório de igual tamanho ponderado pelo próprio Strength.

Nos modelos complementares, recorrência aparece como o contraste mais interessante: associação frágil com concentração local e associação forte com exposição externa.

## 16. Implicações

Para monitoramento de dependência de fornecedores, um painel baseado exclusivamente em HHI pode omitir uma dimensão estrutural relevante. A leitura recomendada é matricial:

| Concentração local | Exposição externa | Interpretação de screening |
|---|---|---|
| baixa relativa | baixa | carteira localmente diversificada e com fornecedores menos centrais externamente |
| alta | baixa | dependência predominantemente local |
| baixa relativa | alta | exposição externa não capturada pela concentração local |
| alta | alta | concentração local combinada com exposição a fornecedores externos relevantes |

Esses quadrantes são sinais de triagem. Eles não constituem classificação de irregularidade ou risco material sem avaliação adicional de objeto contratado, substituibilidade, criticidade operacional e contexto institucional.

## 17. Limitações

- janeiro-junho é coorte parcial de publicações;
- instrumentos assinados no período podem ser publicados posteriormente;
- `valorInicial` não representa execução financeira;
- Strength representa escala monetária observada e não capacidade produtiva;
- Degree representa alcance institucional e não substituibilidade;
- centralidade não mede probabilidade de falha;
- stress tests não modelam adaptação ou substituição;
- a rede está condicionada à cobertura observada do PNCP;
- o filtro empírico é municipal e do Poder Executivo;
- modelos fiscais são associativos;
- nenhuma métrica implica fraude, favorecimento ou conluio.

## 18. Conclusão provisória

A dependência de fornecedores nas compras públicas municipais não se reduz à concentração interna de cada carteira. A robustez leave-one-buyer-out mostrou que a exposição monetária calculada diretamente com Strength global incorporava fortemente a própria relação do comprador, exigindo uma separação conceitual entre importância sistêmica do fornecedor e exposição externa do comprador. Depois dessa correção, Strength LOO e Degree LOO apresentam elevada concordância entre si e associação muito baixa com o HHI, tornando mais nítida a existência de duas dimensões de dependência.

Os testes de estresse mantêm papel distinto. O Strength bruto é apropriado para identificar fornecedores que concentram grande massa monetária no sistema e, quando removidos, produzem perdas de carteira superiores às observadas em sorteios aleatórios de igual tamanho ponderados por Strength.

A combinação de concentração local, exposição externa e stress testing oferece, portanto, um framework de screening mais informativo que qualquer uma dessas medidas isoladamente. O Paper 2 testará se essa estrutura permanece estável ao longo do ano completo e após a captura tardia de instrumentos assinados em 2025.

## Referências recentes a incorporar na bibliografia final

Fountoukidis, I., Dafli, E., Antoniou, I., & Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160.

Sturm, N. F., Candia, C., Damásio, B., et al. (2025). High earnings through firm influence: the role of hierarchical structures in public procurement. *EPJ Data Science*, 14, 27. https://doi.org/10.1140/epjds/s13688-025-00543-z

Fonseca, F. T. (2025). *Patterns in Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil*. Master’s dissertation, NOVA Information Management School.

## Materiais de replicação

Scripts de robustez:

- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`

Resultados:

- `results/robustez_estrutural_2025_06/`
- `results/robustez_modelos_municipio_2025_06/`

Logs auditáveis:

- `results/robustez_estrutural_2025_06/log_execucao.txt`
- `results/robustez_modelos_municipio_2025_06/log_execucao.txt`
