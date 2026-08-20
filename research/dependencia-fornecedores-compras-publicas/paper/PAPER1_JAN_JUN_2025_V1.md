# Paper 1 — janeiro a junho de 2025

## Título provisório

**Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição em Rede e Vulnerabilidade a Choques**

### Título em inglês

**Structural Supplier Dependency in Municipal Public Procurement: Portfolio Concentration, Network Exposure, and Vulnerability to Supplier Shocks**

## Escopo do estudo

Este artigo apresenta e testa um quadro de mensuração de dependência de fornecedores aplicado a órgãos do Poder Executivo municipal observados no Portal Nacional de Contratações Públicas (PNCP). A janela de coleta compreende publicações de 1º de janeiro a 30 de junho de 2025. Para as métricas econômicas, são considerados apenas instrumentos assinados em 2025 e com `valorInicial > 0`.

A unidade principal de comprador é o CNPJ institucional do órgão. A chave de instrumento é `numeroControlePNCP`, materializada na base como `id_contrato`. `numeroControlePNCPCompra` é utilizado somente como ligação com a compra e nunca como chave de deduplicação de instrumentos.

A base pública identificada contém somente fornecedores pessoa jurídica. Informações de pessoas físicas e pessoas estrangeiras permanecem restritas a diagnósticos agregados.

A janela janeiro-junho é uma coorte de publicações e não equivale ao ano fiscal completo. O artigo não deve apresentar seus resultados como estimativas anuais de 2025.

## Pergunta de pesquisa

Em que medida a concentração monetária observada dentro da carteira de um comprador público municipal captura a sua exposição a fornecedores estruturalmente centrais na rede global de contratação e como essa exposição se manifesta sob choques coletivos direcionados?

## Tese

A dependência de fornecedores possui pelo menos duas dimensões empiricamente distintas:

1. **concentração local da carteira**, medida por participações monetárias dentro de cada comprador;
2. **exposição estrutural**, medida pela posição global dos fornecedores na rede comprador-fornecedor e ponderada pela importância desses fornecedores na carteira local.

A vulnerabilidade do comprador deve ser analisada pela combinação dessas dimensões e por testes de estresse, e não pelo HHI isoladamente.

## Contribuição

A contribuição não é o uso isolado de HHI, redes bipartidas, Degree, Strength, recorrência ou ataques direcionados. Esses instrumentos já aparecem na literatura de compras públicas e de redes comprador-fornecedor.

A contribuição é a integração, no nível do comprador público municipal, de:

- concentração monetária local;
- divergência entre valor e frequência contratual;
- centralidade global de fornecedores;
- exposição da carteira à centralidade global;
- identificação de discordância entre concentração local e exposição estrutural;
- testes de estresse direcionados e contrafactuais aleatórios;
- validação longitudinal do sinal de exposição;
- integração complementar com variáveis fiscais municipais.

## Posicionamento na literatura

O artigo deve dialogar explicitamente com quatro blocos:

1. concentração e dependência em cadeias de suprimento;
2. redes comprador-fornecedor e centralidade;
3. public procurement analytics e redes de contratação;
4. persistência e embeddedness de relações comprador-fornecedor.

Literatura recente a incorporar na revisão:

- Fountoukidis, I.; Dafli, E.; Antoniou, I.; Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160. O Institutional Closure Index combina concentração, persistência e embeddedness no nível da autoridade contratante. O presente artigo se diferencia por concentrar-se na exposição de uma carteira local à posição global dos fornecedores e na vulnerabilidade a choques coletivos.
- Trabalho em EPJ Data Science sobre influência, hierarquia e centralidade de firmas em redes portuguesas de compras públicas. Deve ser usado para situar Degree, Strength, comunidades e concentração como instrumentos já existentes.
- Trabalhos recentes sobre redes brasileiras de contratação pública devem ser citados para evitar reivindicação de novidade da análise de redes no contexto nacional.
- Literatura geral de supplier concentration e network position deve sustentar a interpretação de dependência e poder relacional sem transpor causalidade do setor privado ao setor público.

## 1. Dados e formação da amostra

### 1.1 PNCP

- coleta por data de publicação;
- janela principal: 01/01/2025 a 30/06/2025;
- esfera municipal, Poder Executivo;
- comprador: CNPJ institucional;
- fornecedores identificados publicamente: PJ;
- instrumento: `numeroControlePNCP`;
- valor econômico: `valorInicial`;
- assinatura em 2025 para métricas econômicas.

### 1.2 Escala acumulada janeiro-junho

- 105.582 instrumentos PJ únicos na coorte de publicação;
- 98.438 instrumentos assinados em 2025;
- 2.349 compradores com métricas;
- 1.347 compradores elegíveis no critério principal de pelo menos 3 fornecedores e 5 instrumentos;
- 20.367 fornecedores na rede global.

### 1.3 SICONFI

A integração fiscal é complementar. Em junho:

- 1.346 compradores possuíam vínculo municipal único;
- 1.335 tinham despesa empenhada disponível;
- cobertura de 99,18%;
- 725 municípios com despesa empenhada.

A integração fiscal não redefine a unidade do estudo nem transforma associação em causalidade.

## 2. Métricas

### 2.1 Concentração monetária da carteira

Para comprador `b` e fornecedor `j`, seja:

`w_bj = V_bj / sum_j V_bj`

Então:

`HHI_b = sum_j w_bj^2`

O HHI normalizado é:

`HHI_norm_b = (HHI_b - 1/N_b) / (1 - 1/N_b)`

Também são reportados CR1, CR4 e número efetivo de fornecedores `1/HHI`.

### 2.2 Concentração por frequência

O CountHHI utiliza a participação do fornecedor no número de instrumentos da carteira. Ele é uma métrica de caracterização e robustez e não uma contribuição original isolada.

### 2.3 Rede global

A rede é bipartida, com compradores institucionais e fornecedores PJ.

- **Degree global**: número de compradores distintos atendidos pelo fornecedor;
- **Strength global**: soma do valor das relações comprador-fornecedor.

Strength permanece a especificação principal para choque sistêmico. Degree é complementar.

### 2.4 Exposição estrutural

A exposição por Strength é:

`E_b^S = sum_j w_bj * PctRank(Strength_j)`

A exposição por Degree é definida de forma análoga.

### 2.5 Discordância entre HHI e exposição

A classificação principal historicamente utilizada é:

- HHI monetário abaixo do Q75;
- exposição Strength no Q75 ou acima.

No texto final, essa categoria deve ser denominada preferencialmente **exposição estrutural não capturada pelo HHI** ou **discordância concentração-exposição**, evitando sugerir que `HHI < Q75` significa necessariamente baixa concentração absoluta.

O percentual observado não deve ser interpretado como prevalência anormal. Sob independência perfeita entre classificações contínuas, o benchmark mecânico para `abaixo de Q75` × `acima de Q75` é 18,75%.

Robustezes adicionais:

- diferença entre percentil de exposição e percentil de HHI;
- resíduo da exposição Strength após HHI normalizado;
- classificação leave-one-buyer-out.

## 3. Resultados principais janeiro-junho

### 3.1 Concentração

Na amostra elegível 3/5:

- HHI monetário mediano: 0,2365;
- HHI normalizado mediano: 0,1563;
- CountHHI mediano: 0,0816;
- CountHHI normalizado mediano: 0,00682;
- número efetivo mediano de fornecedores: 4,23;
- CR1 mediano: 0,3837;
- CR4 mediano: 0,8037.

Em 98,14% dos compradores o HHI monetário supera o HHI por frequência. Interpretar como diferença entre concentração de valor e de contagem, não como indício de irregularidade.

### 3.2 Exposição estrutural

A correlação entre HHI normalizado e exposição Strength global é moderada (`rho = 0,4081`). Foram identificados 177 compradores, 13,14% dos elegíveis, no quadrante de discordância concentração-exposição.

A interpretação correta é que HHI e exposição estrutural não são medidas redundantes.

### 3.3 Choques coletivos

Com perda mínima de 50% da carteira e ranking principal por Strength global:

- top 1%: 8,91% severamente afetados, contra 0,32% na média aleatória;
- top 5%: 34,15%, contra 1,79%;
- top 10%: 48,26%, contra 4,08%.

Esses cenários são mecânicos e não medem default, interrupção real, substituibilidade, capacidade produtiva ou renegociação.

## 4. Robustezes obrigatórias antes da versão final

### 4.1 Leave-one-buyer-out

Para cada comprador `b`, recalcular a posição do fornecedor retirando a própria contribuição do comprador:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Em seguida, recalcular a exposição da carteira usando rankings específicos do comprador. Reportar:

- correlação original versus LOO;
- variação mediana e caudas;
- retenção do quartil superior;
- alteração na classificação de discordância.

Esse teste responde à possibilidade de auto-inclusão mecânica do próprio comprador no Strength global.

### 4.2 Stress test alternativo

Manter o teste principal já congelado e adicionar dois contrafactuais:

1. remoção aleatória com probabilidade proporcional ao Strength;
2. remoção aleatória de número variável de fornecedores até atingir aproximadamente a mesma massa de Strength sistêmico removida pelo ataque direcionado.

A comparação deve separar o efeito de selecionar fornecedores estruturalmente centrais do efeito mecânico de retirar grande massa monetária do sistema.

### 4.3 Exposição discordante

Manter o quadrante principal por comparabilidade e adicionar:

- gap de percentis `PctExposure - PctHHI`;
- resíduo da exposição após HHI normalizado.

### 4.4 Modelos fiscais

O modelo principal permanece associativo. A regressão deve ocupar papel secundário no artigo.

Acrescentar como robustez:

- peso `1/N_m`, onde `N_m` é o número de compradores elegíveis no município;
- regressão agregada ao município;
- CR1 e CR4 como outcomes alternativos ao HHI normalizado.

O número de fornecedores deve ser tratado como controle estrutural, pois possui relação matemática com medidas de concentração. Seu coeficiente não deve ser apresentado como descoberta causal.

## 5. Persistência longitudinal

### Abril para maio

- 1.013 compradores comuns;
- rho de exposição Strength: 0,9378;
- retenção do quartil superior: 86,22%;
- retenção do quadrante de discordância: 82,96%;
- quadrante completo estável: 85,88%.

### Maio para junho

- 1.210 compradores comuns;
- Strength: rho = 0,9570;
- Degree: rho = 0,9319;
- retenção do quartil superior de Strength: 90,76%;
- retenção do quartil superior de Degree: 92,08%;
- retenção da discordância concentração-exposição: 86,27%;
- quadrante completo estável: 88,68%.

A interpretação deve ser de persistência de **sinais de triagem**, não de rótulo permanente de risco.

## 6. Efeito de composição

Entre maio e junho:

- elegíveis: 1.210 para 1.347;
- 137 novos elegíveis;
- nenhuma saída;
- HHI agregado mediano: 0,2420 para 0,2365;
- HHI mediano dos comuns em junho: 0,2233;
- HHI mediano dos entrantes: 0,3606.

Portanto, estatísticas temporais devem separar mudança dos compradores persistentes e efeito de composição dos novos elegíveis.

## 7. Modelos associativos

Especificação principal:

`HHI_norm_b = beta0 + beta1 ln(Pop_b) + beta2 ln(DespesaPC_b) + beta3 ln(NFornec_b) + beta4 ln(InstrPorFornec_b) + Regiao + erro_b`

OLS com erros agrupados por município e fractional logit como robustez funcional.

Resultados janeiro-junho devem ser apresentados apenas depois dos resultados de rede e stress test.

Pontos de interpretação:

- população: associação positiva e persistente com HHI normalizado;
- despesa per capita: ausência de robustez;
- número de fornecedores: associação negativa forte, porém parcialmente mecânica;
- recorrência: instável para HHI local;
- recorrência: positiva e persistente para exposição Strength nas janelas disponíveis.

Nenhuma dessas associações deve receber linguagem causal.

## 8. Discussão

A discussão deve enfatizar que diversificação aparente da carteira não garante baixa exposição estrutural. Um comprador pode distribuir seus gastos entre diversos fornecedores e, ainda assim, depender de firmas que ocupam posições centrais em várias carteiras públicas.

O framework é um instrumento de screening e stress testing. Não é mecanismo de detecção automática de fraude, favorecimento, conluio ou risco de crédito.

## 9. Limitações

- janeiro-junho é coorte parcial de publicações;
- publicações tardias podem alterar a cobertura de instrumentos assinados no período;
- `valorInicial` não representa execução financeira;
- centralidade não mede substituibilidade técnica;
- Strength depende da escala monetária observada;
- choques simulados não modelam adaptação, substituição ou renegociação;
- a rede cobre o universo observado no PNCP segundo os filtros adotados;
- ausência mensal de município não implica falha de reporte;
- modelos fiscais são associativos;
- nenhuma métrica implica fraude ou favorecimento.

## 10. Organização recomendada do manuscrito

1. Introdução e problema de dependência.
2. Literatura e contribuição.
3. Dados, cobertura e política de privacidade.
4. Concentração local da carteira.
5. Rede global e exposição estrutural.
6. Discordância HHI-exposição.
7. Stress tests.
8. Persistência longitudinal e efeito de composição.
9. Robustezes estruturais.
10. Integração fiscal e modelos associativos.
11. Discussão, implicações e limitações.
12. Conclusão.

## 11. Regra de não sobreposição com o Paper 2

O Paper 1 é o artigo de **proposição e validação inicial do framework**. Seu objeto empírico termina em junho de 2025. O Paper 2 não deve repetir integralmente as mesmas tabelas, narrativa ou introdução. Ele deve citar o Paper 1 e tratar o framework como método previamente definido, concentrando-se na validação anual, estabilidade temporal, sazonalidade, sensibilidade a publicações tardias e generalização das conclusões ao ano de 2025 fechado.
