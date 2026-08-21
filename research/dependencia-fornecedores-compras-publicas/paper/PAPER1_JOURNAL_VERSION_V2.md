# Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração Local, Exposição Externa Leave-One-Buyer-Out e Testes de Estresse

## Structural Supplier Dependency in Municipal Public Procurement: Local Concentration, Leave-One-Buyer-Out External Exposure, and Stress Tests

**Autor:** Jacson Cruz do Nascimento  
**ORCID:** 0009-0006-6535-9569  
**Journal Version V2:** 21 de agosto de 2026  
**JEL:** H57; D85; C55

> Versão de submissão em desenvolvimento. Preserva integralmente o preprint e a Journal Version V1 como histórico editorial; os resultados novos desta versão são robustezes adicionais, sem alteração da especificação principal.

## Resumo

Este artigo desenvolve e valida empiricamente um framework integrado para mensurar dependência estrutural de fornecedores em compras públicas municipais a partir de três dimensões: concentração local da carteira, exposição externa em rede e vulnerabilidade mecânica a choques de fornecedores. A análise utiliza instrumentos publicados no Portal Nacional de Contratações Públicas entre janeiro e junho de 2025, restringindo as métricas econômicas a instrumentos assinados em 2025, fornecedores pessoa jurídica e compradores do Poder Executivo municipal. A contribuição metodológica está na integração entre concentração da carteira e exposição leave-one-buyer-out (LOO), que remove do posicionamento de cada fornecedor a contribuição do comprador focal, evitando auto-inclusão. Na amostra de 1.347 compradores elegíveis, a correlação entre exposição Strength bruta e Strength LOO é 0,2647, enquanto Degree bruto e Degree LOO apresentam correlação de 0,9821. Após a correção, Strength LOO e Degree LOO convergem fortemente entre si (rho = 0,9500), mas apresentam baixa associação com o HHI normalizado (rho = -0,0183 e -0,0763). A discordância concentração-exposição permanece identificável e persistente longitudinalmente. Nos testes de estresse, a remoção direcionada dos fornecedores de maior Strength produz perdas severas de carteira superiores às de sorteios de igual tamanho ponderados por Strength. Uma robustez adicional que agrega estabelecimentos pela raiz do CNPJ preserva os rankings de HHI, Strength LOO e Degree LOO (rho = 0,9991; 0,9877; 0,9881, respectivamente) e mantém as classificações de discordância. Modelos associativos complementares mostram que recorrência contratual tem relação frágil com concentração local, mas positiva e consistente com exposição externa. Os resultados indicam que concentração interna, posição externa e vulnerabilidade sistêmica são dimensões distintas e complementares para screening de dependência.

**Palavras-chave:** compras públicas; dependência de fornecedores; concentração; redes; leave-one-buyer-out; PNCP; testes de estresse; resiliência.

## Abstract

This article develops and empirically validates an integrated framework for measuring structural supplier dependency in municipal public procurement through three dimensions: local portfolio concentration, external network exposure, and mechanical vulnerability to supplier shocks. The analysis uses instruments published in Brazil's National Public Procurement Portal from January through June 2025, restricting economic measures to instruments signed in 2025, corporate suppliers, and municipal executive-branch buyers. The methodological contribution lies in combining portfolio concentration with leave-one-buyer-out (LOO) exposure, which removes the focal buyer's own contribution from each supplier's network position and therefore avoids mechanical self-inclusion. Among 1,347 eligible buyers, the correlation between raw Strength exposure and Strength LOO is 0.2647, whereas raw Degree and Degree LOO remain highly correlated at 0.9821. After externalization, Strength LOO and Degree LOO are strongly concordant (rho = 0.9500) but only weakly related to normalized HHI (rho = -0.0183 and -0.0763). Concentration-exposure discordance remains identifiable and longitudinally persistent. Targeted removal of the highest-Strength suppliers produces more severe portfolio losses than equally sized Strength-weighted random removals. An additional robustness test aggregating supplier establishments by the first eight digits of the Brazilian corporate tax identifier preserves HHI, Strength LOO, and Degree LOO rankings (rho = 0.9991, 0.9877, and 0.9881, respectively) and leaves discordance classifications largely unchanged. Complementary associative models show that contractual recurrence is weakly related to local concentration but positively and consistently associated with external exposure. The findings indicate that local concentration, external position, and systemic vulnerability are distinct and complementary dimensions for dependency screening.

**Keywords:** public procurement; supplier dependency; concentration; networks; leave-one-buyer-out; stress testing; resilience.

# 1. Introdução

Compradores públicos podem apresentar dependência de fornecedores por mecanismos diferentes. Uma carteira pode concentrar grande parcela do valor contratado em poucas empresas, situação capturada por medidas como HHI e CR1. Porém, mesmo uma carteira relativamente distribuída pode depender de fornecedores que ocupam posições relevantes em relações com muitos outros compradores ou concentram massa monetária expressiva fora da relação focal. A primeira situação é uma propriedade interna da carteira; a segunda é uma propriedade relacional.

Essa distinção dialoga com uma literatura consolidada sobre dependência de recursos, complexidade da base de fornecedores e redes de suprimento. A perspectiva de dependência de recursos estabelece que organizações ficam sujeitas a restrições externas quando recursos relevantes são concentrados ou controlados por outros atores (Pfeffer & Salancik, 1978). Em operações e supply management, Choi e Krause (2006) mostram que o número de fornecedores, sua diferenciação e suas inter-relações compõem dimensões distintas da complexidade da base de suprimento. Kleindorfer e Saad (2005) e Craighead et al. (2007) enfatizam que risco de disrupção depende não apenas de eventos isolados, mas também da estrutura do sistema, da criticidade de nós e das capacidades de mitigação. Borgatti e Li (2009) sistematizam a aplicação da análise de redes ao contexto de supply chains, e Kim, Chen e Linderman (2015) mostram que a estrutura da rede condiciona resiliência e propagação de disrupções.

Nas compras públicas, estudos recentes aplicam redes para analisar competição, concentração, influência de firmas, recorrência e riscos de integridade (Popa, 2019; Wachs et al., 2021; Fountoukidis et al., 2023; Pliatsidis, 2024; Sturm et al., 2025). A evidência internacional, portanto, já sustenta o uso de redes comprador-fornecedor. A questão metodológica que permanece para o presente problema é outra: como medir a exposição de um comprador à posição externa de seus fornecedores sem deixar que o próprio comprador determine parte dessa posição?

Este artigo propõe uma solução operacional por meio de uma correção leave-one-buyer-out (LOO). Ao calcular a posição de cada fornecedor para um comprador focal, subtrai-se a contribuição desse comprador. Assim, o Strength bruto continua representando importância monetária sistêmica para fins de stress testing, enquanto Strength LOO e Degree LOO passam a representar exposição externa do comprador.

O framework integra três componentes:

1. **concentração local da carteira**, baseada na distribuição do valor e da frequência de instrumentos entre fornecedores;
2. **exposição externa LOO**, baseada na posição dos fornecedores depois de removida a contribuição do comprador focal;
3. **vulnerabilidade sistêmica**, avaliada por testes de estresse que removem fornecedores de alta importância monetária.

![Figura 1. Framework empírico](figures/figura_1_framework_journal.png)

**Figura 1.** Framework empírico da dependência estrutural: concentração local, exposição externa e vulnerabilidade sistêmica são dimensões relacionadas, porém não intercambiáveis.

A pergunta de pesquisa é:

> Em que medida a concentração local da carteira captura, ou deixa de capturar, a exposição externa de compradores públicos municipais a fornecedores estruturalmente relevantes, e como essa distinção se manifesta sob choques coletivos simulados?

A contribuição não reside na novidade isolada de HHI, Degree, Strength, redes bipartidas ou stress testing. Ela consiste em **integrar concentração local, exposição externa LOO, discordância concentração-exposição e stress testing em um único desenho empírico no nível do comprador municipal**, além de testar a persistência longitudinal dessas medidas.

# 2. Literatura e desenvolvimento do argumento

## 2.1 Dependência, concentração e complexidade da base de fornecedores

A teoria da dependência de recursos fornece a base conceitual para interpretar relações concentradas com fornecedores sem presumir irregularidade. Organizações dependem de atores externos que controlam recursos necessários e procuram reduzir incerteza, equilibrar poder ou reorganizar relações interorganizacionais (Pfeffer & Salancik, 1978). Em relações comprador-fornecedor, essa lógica implica que concentração pode reduzir custos de coordenação, mas também aumentar exposição a poucos parceiros.

Choi e Krause (2006) tratam a base de fornecedores como parte da rede efetivamente gerida pelo comprador e distinguem número de fornecedores, diferenciação e inter-relações. Essa separação é central ao presente artigo: contar fornecedores não informa como o valor está distribuído nem quão conectados esses fornecedores estão fora da carteira focal. A literatura de compras também enfatiza poder e interdependência nas estratégias de portfólio (Caniëls & Gelderman, 2005), enquanto estudos empíricos de supply chain mostram que complexidade estrutural aumenta a frequência de disrupções e que os efeitos da concentração sobre resiliência dependem do contexto e do estágio da disrupção (Bode & Wagner, 2015; Jiang et al., 2023; Polyviou et al., 2023).

O HHI é utilizado aqui como medida da distribuição interna da carteira, não como medida antitruste de um mercado relevante. Essa distinção evita atribuir significado de competição de mercado a uma unidade empírica que é o comprador institucional.

## 2.2 Redes de suprimento, centralidade e disrupções

A literatura de redes de suprimento mostra que relações bilaterais não esgotam a estrutura de dependência. Borgatti e Li (2009) demonstram como conceitos de centralidade, intermediação e estrutura relacional podem ser transportados para supply chains, desde que seu mecanismo seja explicitado. Kim et al. (2015) distinguem disrupções em nós ou arcos de disrupções no nível da rede e mostram que diferentes estruturas possuem diferentes propriedades de resiliência. Craighead et al. (2007) relacionam severidade de disrupções à densidade, complexidade e criticidade de nós. A evidência clássica de Hendricks e Singhal (2003) também documenta consequências econômicas relevantes associadas a falhas de supply chain, dando fundamento ao interesse em vulnerabilidade estrutural.

A literatura de resiliência também separa a ocorrência da disrupção das capacidades de mitigação e recuperação. Um nó indisponível por curto período pode ter efeitos atenuados por estoques, redirecionamento, fornecedores alternativos, renegociação ou recuperação operacional, enquanto uma indisponibilidade persistente pode produzir efeitos mais severos. O teste de estresse deste artigo não parametriza duração nem recuperação: ele representa uma remoção estática do nó na rede observada e deve ser interpretado como um cenário-limite de indisponibilidade, não como previsão de interrupção permanente.

Esses trabalhos justificam separar a posição de um fornecedor no sistema da distribuição interna de compras de um único comprador. O problema específico deste artigo surge quando a própria relação focal contribui para a métrica global usada para medir exposição. Para Strength, esse problema é especialmente relevante porque o valor contratado pelo comprador entra diretamente na soma monetária do fornecedor.

## 2.3 Recorrência, embeddedness e compras públicas

Relações repetidas podem gerar coordenação, informação e redução de custos de transação, mas também podem produzir dependência ou fechamento relacional. Uzzi (1996) mostra que embeddedness pode gerar benefícios até determinado ponto, após o qual relações excessivamente fechadas podem perder eficiência. Em compras públicas, Popa (2019) documenta estruturas recorrentes de transações e mostra que repetição não deve ser automaticamente interpretada como comportamento impróprio.

Wachs, Fazekas e Kertész (2021) representam mercados de compras públicas como redes bipartidas de compradores e fornecedores e mostram que métricas de rede podem apoiar análise de risco quando combinadas com indicadores especificamente construídos para integridade. O presente artigo utiliza a mesma lógica de rede bipartida, mas com finalidade distinta: mensuração estrutural de dependência, sem inferência de fraude ou conluio.

Trabalhos recentes aprofundam concentração, influência, recorrência e fechamento institucional em compras públicas (Fountoukidis et al., 2023; Pliatsidis, 2024; Sturm et al., 2025; Fountoukidis et al., 2026a, 2026b). Eles são utilizados como literatura de fronteira, enquanto o argumento teórico principal é ancorado na literatura consolidada anterior a 2025.

## 2.4 Lacuna e hipóteses analíticas

Se concentração local e exposição externa forem dimensões redundantes, compradores com HHI elevado tenderão a apresentar exposição LOO igualmente elevada, e a retirada da contribuição focal pouco alterará os rankings de exposição. Se as dimensões capturarem mecanismos distintos, a correção LOO deve revelar diferenças entre posição sistêmica do fornecedor e concentração da carteira do comprador.

As hipóteses abaixo formalizam a lógica teórica que organiza os testes. Elas não utilizam limiares calibrados a partir dos resultados observados e não correspondem a um protocolo preregistrado; sua função é tornar explícitas as relações empíricas avaliadas pelo framework.

**H1 - Auto-inclusão monetária.** A externalização leave-one-buyer-out deve alterar mais intensamente a exposição baseada em Strength do que a exposição baseada em Degree, porque o valor do comprador focal entra diretamente no Strength bruto do fornecedor.

**H2 - Não redundância.** A concentração monetária da carteira e a exposição externa LOO devem apresentar associação limitada, refletindo dimensões distintas da dependência estrutural.

**H3 - Concordância externa.** Strength LOO e Degree LOO devem apresentar associação positiva, pois ambas capturam posição externa do fornecedor, embora uma represente massa monetária e a outra alcance entre compradores.

**H4 - Vulnerabilidade sistêmica.** A remoção direcionada de fornecedores com maior Strength deve produzir perdas de carteira mais severas que remoções aleatórias de igual tamanho, mesmo quando a probabilidade de sorteio é proporcional ao Strength.

**H5 - Persistência de screening.** Rankings de exposição LOO e classificações de discordância devem apresentar persistência entre janelas acumuladas adjacentes se capturarem estrutura relacional e não apenas ruído de composição.

# 3. Dados e desenho empírico

## 3.1 Fonte e regra temporal

A fonte principal é o Portal Nacional de Contratações Públicas (PNCP). A coleta operacional é realizada pela data de publicação do instrumento. A janela desta análise compreende publicações de 01/01/2025 a 30/06/2025, restringindo as métricas econômicas a instrumentos assinados em 2025, com `valorInicial > 0`, pertencentes à esfera municipal e ao Poder Executivo.

A janela é uma **coorte acumulada de publicações janeiro-junho**, não o ano de 2025 completo. Instrumentos assinados em 2025 e publicados posteriormente ficam fora deste recorte. Essa limitação temporal será tratada no segundo paper com janela anual e captura tardia.

## 3.2 Unidade institucional, chaves e privacidade

O comprador é o CNPJ institucional do órgão ou entidade. Município é dimensão territorial e fonte de controles fiscais. A chave de instrumento é `numeroControlePNCP`, materializada como `id_contrato`; `numeroControlePNCPCompra` é utilizado apenas como ligação com a compra e nunca como chave de deduplicação.

A base pública identificada contém somente fornecedores pessoa jurídica. Registros de pessoa física e pessoa estrangeira são mantidos apenas em diagnósticos agregados.

## 3.3 Amostra

**Tabela 1. Amostra e métricas principais, janeiro-junho de 2025**

| Indicador | Valor |
|---|---:|
| Instrumentos PJ únicos na coorte | 105.582 |
| Instrumentos assinados em 2025 | 98.438 |
| Compradores com métricas | 2.349 |
| Compradores elegíveis (>=3 fornecedores; >=5 instrumentos) | 1.347 |
| Fornecedores na rede global | 20.367 |
| HHI monetário mediano | 0,2365 |
| HHI normalizado mediano | 0,1563 |
| CountHHI mediano | 0,0816 |
| Número efetivo de fornecedores, mediana | 4,23 |
| CR1 mediano | 0,3837 |
| CR4 mediano | 0,8037 |
| Compradores com HHI monetário > CountHHI | 98,14% |

Fonte: elaboração própria a partir do PNCP.

A integração fiscal não reduz a amostra de 1.347 compradores diretamente para 725 observações. Dos 1.347 compradores elegíveis, 1.346 possuem vínculo municipal único e 1.335 possuem despesa empenhada disponível no SICONFI, formando a amostra dos modelos no nível do comprador. Esses 1.335 compradores pertencem a 725 municípios. A robustez municipal agrega os compradores e utiliza esses 725 municípios como nova unidade de análise. Portanto, o número 725 representa mudança de unidade analítica, e não perda de quase metade dos compradores por ausência de informação fiscal.

# 4. Medidas e estratégia analítica

## 4.1 Concentração local

Para comprador $b$ e fornecedor $j$, seja $V_{bj}$ o valor acumulado da relação comprador-fornecedor e

$$
w_{bj}=\frac{V_{bj}}{\sum_j V_{bj}}.
$$

Para simplificar a notação matemática, denotamos o HHI monetário do comprador por $H_b$:

$$
H_b=\sum_j w_{bj}^2.
$$

Com $N_b$ fornecedores, o HHI normalizado é:

$$
H_b^{norm}=\frac{H_b-1/N_b}{1-1/N_b}.
$$

São calculados ainda CR1, CR4, número efetivo de fornecedores ($N_{eff}=1/H_b$), CountHHI e CountHHI normalizado.

## 4.2 Posição sistêmica do fornecedor

A rede é bipartida e ponderada pelo valor acumulado das relações. Denotamos o Strength global do fornecedor $j$ por $S_j$:

$$
S_j=\sum_b V_{bj}.
$$

O Degree é denotado por $D_j$ e corresponde ao número de compradores distintos atendidos pelo fornecedor:

$$
D_j=\left|\{b:V_{bj}>0\}\right|.
$$

O Strength bruto mede massa monetária sistêmica e é utilizado para ordenar fornecedores nos testes de estresse.

## 4.3 Exposição externa leave-one-buyer-out

Para o comprador focal $b$, a contribuição própria é retirada antes de avaliar a posição do fornecedor:

$$
S_j^{(-b)}=S_j-V_{bj},
$$

$$
D_j^{(-b)}=D_j-I(V_{bj}>0).
$$

Se $R_b(x)$ representa o percentil do valor $x$ na rede recalculada para o comprador focal, as exposições são:

$$
E_b^{S,\mathrm{LOO}}=\sum_j w_{bj}R_b\left(S_j^{(-b)}\right),
$$

$$
E_b^{D,\mathrm{LOO}}=\sum_j w_{bj}R_b\left(D_j^{(-b)}\right).
$$

Strength LOO é a medida preferencial de exposição externa; Degree LOO é a verificação complementar.

## 4.4 Discordância concentração-exposição

Em termos operacionais, classificamos como discordante o comprador cujo HHI monetário está abaixo do 75º percentil da amostra e cuja exposição LOO está no 75º percentil ou acima. Em notação compacta:

$$
H_b<Q_{75}(H), \qquad E_b\geq Q_{75}(E).
$$

O grupo é denominado **discordância concentração-exposição** ou **exposição externa não capturada pelo HHI**. O corte é relativo à distribuição observada e não representa limiar normativo. Sob independência entre duas classificações contínuas com cortes Q75, o benchmark mecânico do quadrante é 18,75%.

## 4.5 Testes de estresse

Os testes removem os top 1%, 5% e 10% dos fornecedores segundo Strength bruto e calculam a fração da carteira de cada comprador associada aos fornecedores removidos. O resultado principal é a proporção de compradores com perda simulada de pelo menos 50% da carteira.

O benchmark principal usa 1.000 sorteios sem reposição com o mesmo número de fornecedores removidos e probabilidade de seleção proporcional ao Strength. Assim, a comparação não contrapõe fornecedores grandes a um conjunto predominantemente formado por fornecedores pequenos.

A remoção é estática: o exercício não inclui duração da indisponibilidade, estoques, substituição, expediting, renegociação ou recuperação. Por isso, ele é interpretado como diagnóstico mecânico de exposição a uma indisponibilidade do conjunto removido, próximo a um cenário-limite persistente no instante analisado. Choques temporários podem gerar perdas efetivas menores se existirem mecanismos de mitigação e recuperação (Craighead et al., 2007; Kim et al., 2015).

## 4.6 Robustez da unidade do fornecedor: CNPJ raiz

A especificação principal trata cada CNPJ completo de fornecedor PJ como nó distinto. Como matriz e filiais podem compartilhar os oito primeiros dígitos do CNPJ, realizamos uma robustez adicional agregando estabelecimentos pela **raiz do CNPJ**. Para a amostra janeiro-junho, 98.407 dos 98.438 instrumentos econômicos PJ (99,97%) apresentam identificador com 14 dígitos; identificadores fora desse padrão permanecem individualizados para evitar agregações artificiais.

A robustez recalcula relações comprador-fornecedor, HHI, CR1, número de fornecedores, Strength, Degree, exposições LOO, discordância e stress tests. A comparação principal mantém fixa a amostra original de 1.347 compradores, isolando o efeito da unidade do fornecedor. Em paralelo, a elegibilidade é recalculada após a agregação para verificar se algum comprador cruza o critério de pelo menos três fornecedores. CNPJ raiz aproxima a distinção matriz-filial, mas não equivale a grupo econômico: empresas sob controle comum podem possuir raízes distintas.

## 4.7 Modelos associativos e ponderação municipal

A integração fiscal utiliza dados municipais do SICONFI. A especificação no nível do comprador é estimada com WLS, atribuindo a cada comprador do município $m$ o peso $1/N_m$, em que $N_m$ é o número de compradores elegíveis do município presentes na amostra modelada. Essa ponderação não é uma estimação por variância inversa: sua finalidade é fazer com que o peso total de cada município seja aproximadamente igual, evitando que covariáveis fiscais municipais, repetidas para vários CNPJs compradores do mesmo ente, deem peso mecânico maior aos municípios com mais compradores institucionais. Os erros-padrão são agrupados por município.

Como robustez, os dados também são agregados ao nível municipal e estimados por OLS com erros HC3. Esses modelos caracterizam associações e não identificam efeitos causais.

# 5. Resultados

## 5.1 Concentração monetária e frequência

O HHI monetário mediano é 0,2365 e o CountHHI mediano é 0,0816. Em 98,14% dos compradores elegíveis, o HHI monetário supera o CountHHI. A correlação de Spearman entre as duas medidas é 0,5678. A distribuição monetária, portanto, contém informação que não é reproduzida pela simples frequência de instrumentos.

## 5.2 Diagnóstico da auto-inclusão

**Tabela 2. Diagnóstico leave-one-buyer-out**

| Métrica | Strength | Degree |
|---|---:|---:|
| Correlação exposição bruta vs. LOO | 0,2647 | 0,9821 |
| Retenção do quartil superior | 38,87% | 89,61% |
| Correlação HHI_norm vs. exposição LOO | -0,0183 | -0,0763 |
| Compradores em discordância | 221 (16,41%) | 237 (17,59%) |

![Figura 2. Diagnóstico leave-one-buyer-out](figures/figura_2_diagnostico_loo_journal.png)

**Figura 2.** A exposição baseada em Strength é fortemente alterada pela retirada da contribuição do comprador focal, enquanto Degree permanece praticamente invariável. Rótulos numéricos padronizados em quatro casas decimais.

A correlação entre exposição Strength bruta e Strength LOO é 0,2647 e apenas 38,87% dos compradores inicialmente no quartil superior permanecem nele após a correção. A contribuição própria mediana ponderada do comprador ao Strength dos fornecedores de sua carteira é 75,89%.

Degree apresenta comportamento distinto: a correlação entre Degree bruto e Degree LOO é 0,9821, com retenção de 89,61% do quartil superior. O contraste mostra que o problema de auto-inclusão é especialmente relevante para a dimensão monetária. Assim, Strength bruto deve ser interpretado como importância sistêmica do fornecedor, enquanto Strength LOO é a medida adequada para exposição externa do comprador.

## 5.3 Baixa redundância entre concentração e exposição externa

Strength LOO e Degree LOO apresentam forte concordância entre si ($\rho=0,9500$). Em contraste, a correlação entre HHI normalizado e Strength LOO é $\rho=-0,0183$ ($p=0,5020$), e entre HHI normalizado e Degree LOO é $\rho=-0,0763$ ($p=0,0051$). Embora a segunda associação seja estatisticamente diferente de zero, sua magnitude é pequena.

A classificação de discordância identifica 221 compradores (16,41%) com Strength LOO e 237 (17,59%) com Degree LOO. A sobreposição entre as duas classificações é 89,14%. O percentual observado não excede o benchmark mecânico de 18,75% sob independência; o resultado relevante é a existência de uma dimensão externa pouco resumida pelo HHI e a elevada concordância entre as duas medidas LOO.

## 5.4 Testes de estresse

**Tabela 3. Compradores com perda simulada de pelo menos 50% da carteira**

| Fornecedores removidos | k | Direcionado | Aleatório ponderado por Strength | Massa de Strength nos top-k |
|---|---:|---:|---:|---:|
| Top 1% | 204 | 8,91% | 5,46% | 57,56% |
| Top 5% | 1.019 | 34,15% | 22,88% | 79,47% |
| Top 10% | 2.037 | 48,26% | 38,52% | 87,41% |

![Figura 3. Testes de estresse](figures/figura_3_stress_test_journal.png)

**Figura 3.** Proporção de compradores com perda simulada de pelo menos 50% da carteira. Percentuais padronizados em duas casas decimais.

Nos três níveis de remoção, a perda severa sob choque direcionado supera a média do benchmark ponderado. Os valores direcionados também ficam acima do percentil 97,5% das respectivas distribuições aleatórias. Isso sustenta H4: a massa sistêmica não está distribuída de forma equivalente entre fornecedores. O exercício, entretanto, não estima duração ou recuperação. Uma indisponibilidade temporária pode ser atenuada por substituição, estoques ou outras capacidades que não aparecem na rede contratual observada.

## 5.5 Persistência longitudinal e composição

**Tabela 4. Persistência das medidas externalizadas**

| Transição | Compradores comuns | rho Strength LOO | rho Degree LOO | Retenção discordância Strength | Retenção discordância Degree |
|---|---:|---:|---:|---:|---:|
| Abril-maio | 1.013 | 0,8962 | 0,9091 | 85,96% | 87,57% |
| Maio-junho | 1.210 | 0,9266 | 0,9416 | 90,40% | 90,61% |

![Figura 4. Persistência longitudinal](figures/figura_4_persistencia_loo_journal.png)

**Figura 4.** Correlações de ranking e retenção da discordância, com coeficientes padronizados em quatro casas decimais.

A persistência aumenta nas duas métricas entre abril-maio e maio-junho. Ao mesmo tempo, há efeito de composição: entre maio e junho entram 137 compradores e não há saídas. Os entrantes apresentam HHI mediano de 0,3606, superior ao HHI mediano de 0,2233 entre compradores persistentes, mas exposição externa mediana menor: Strength LOO de 0,2048 contra 0,3106 e Degree LOO de 0,1996 contra 0,3044. A evolução agregada deve, portanto, ser decomposta entre mudança dentro dos compradores persistentes e entrada de novas unidades elegíveis.

## 5.6 Sensibilidade à agregação por CNPJ raiz

A robustez por CNPJ raiz reduz a rede de 20.367 CNPJs completos para 20.092 raízes. Foram identificadas 163 raízes com mais de um estabelecimento observado (0,81% das raízes), com máximo de 22 estabelecimentos na mesma raiz. Nenhum dos 1.347 compradores da amostra fixa fica abaixo do critério de três fornecedores após a agregação, e a elegibilidade recalculada permanece em 1.347 compradores.

**Tabela 5. Robustez da unidade do fornecedor por CNPJ raiz**

| Indicador | CNPJ completo | CNPJ raiz | Correlação de ranking original vs. raiz |
|---|---:|---:|---:|
| HHI mediano | 0,2365 | 0,2365 | 0,9991 |
| CR1 mediano | 0,3837 | 0,3850 | 0,9988 |
| Número mediano de fornecedores | 14 | 14 | 0,9997 |
| Strength LOO mediano | 0,2989 | 0,3099 | 0,9877 |
| Degree LOO mediano | 0,2958 | 0,3066 | 0,9881 |

A relação substantiva entre as dimensões também permanece. Na agregação por raiz, Strength LOO e Degree LOO mantêm correlação de 0,9491; HHI normalizado apresenta correlação de -0,0084 com Strength LOO e -0,0682 com Degree LOO. A discordância por Strength LOO passa de 221 para 220 compradores, com retenção de 95,48% da classificação original; por Degree LOO, passa de 237 para 234, com retenção de 96,62%.

Os testes de estresse também são estáveis. Com CNPJ raiz, a remoção direcionada dos top 1%, 5% e 10% gera perda de pelo menos 50% da carteira para 9,13%, 34,60% e 49,07% dos compradores, contra médias de 5,65%, 23,36% e 39,22% no benchmark ponderado. Portanto, a separação entre concentração local, exposição externa e vulnerabilidade sistêmica não depende da decisão de tratar filiais da mesma raiz como fornecedores independentes. A robustez não consolida grupos econômicos que operam por raízes distintas.

# 6. Modelos associativos e robustez

Na janela janeiro-junho, 1.346 compradores possuem vínculo municipal único e 1.335 possuem despesa empenhada disponível no SICONFI. Esses 1.335 compradores pertencem a 725 municípios. A especificação WLS continua no nível do comprador, com 1.335 observações; a especificação agregada utiliza 725 observações municipais.

Para evitar sobrecarregar a notação, escrevemos a especificação-base como:

$$
Y_b=\beta_0+\beta_1P_b+\beta_2X_b+\beta_3F_b+\beta_4C_b+\gamma^{\prime}G_b+\varepsilon_b,
$$

em que $Y_b$ é o outcome de concentração ou exposição; $P_b=\ln(população)$; $X_b=\ln(despesa\ per\ capita)$; $F_b=\ln(número\ de\ fornecedores)$; $C_b=\ln(instrumentos\ por\ fornecedor)$; e $G_b$ reúne os controles de macrorregião.

No WLS, cada comprador do município $m$ recebe peso $1/N_m$. Consequentemente, um município com cinco compradores elegíveis distribui peso total próximo de um entre suas cinco unidades, em vez de pesar cinco vezes mais que um município representado por um único comprador. Os erros-padrão são agrupados por município. A especificação municipal agrega as variáveis dos compradores e usa OLS com erros HC3.

**Tabela 6. Coeficientes-chave das robustezes associativas**

| Outcome / modelo | ln população | ln despesa pc | ln n fornecedores | ln instrumentos/fornecedor |
|---|---:|---:|---:|---:|
| HHI_norm WLS | 0,0206*** | 0,0005 | -0,0715*** | 0,0301† |
| HHI_norm agregado municipal | 0,0207*** | 0,0007 | -0,0753*** | 0,0264 |
| Strength LOO WLS | -0,0311*** | -0,0664* | 0,0072 | 0,1556*** |
| Strength LOO agregado municipal | -0,0298*** | -0,0638* | 0,0104 | 0,2076*** |
| Degree LOO WLS | -0,0276*** | -0,0563† | -0,0055 | 0,2009*** |
| Degree LOO agregado municipal | -0,0260*** | -0,0531† | 0,0005 | 0,2694*** |

Notas: *** $p<0,001$; * $p<0,05$; † $p<0,10$. Modelos com controles de macrorregião.

Como os regressores contínuos entram em log e os outcomes permanecem em nível, uma duplicação de um regressor corresponde a multiplicar seu coeficiente por $\ln(2)$. No HHI normalizado WLS, o coeficiente de 0,0206 para população implica que uma duplicação populacional está associada a aumento de aproximadamente 0,0143 no índice, ou 1,43 ponto percentual em uma escala de 0 a 1, mantendo os demais controles fixos. Para exposição externa, uma duplicação da população está associada a redução aproximada de 2,15 pontos percentuais em Strength LOO e 1,92 ponto percentual em Degree LOO.

A magnitude associada à recorrência é maior. Uma duplicação de instrumentos por fornecedor corresponde, no WLS, a aumento aproximado de 10,79 pontos percentuais em Strength LOO e 13,93 pontos percentuais em Degree LOO, mantidos os demais controles. Esses valores descrevem associação condicional e não efeito causal.

Nos modelos de concentração, população mantém associação positiva; despesa per capita não apresenta padrão robusto; número de fornecedores mantém associação negativa, interpretada como controle estrutural por sua relação matemática com o HHI; e recorrência perde robustez quando o peso municipal é equalizado. Nos modelos de exposição externa, o número de fornecedores deixa de apresentar associação substantiva, enquanto recorrência permanece positiva e estatisticamente precisa nas quatro especificações LOO.

# 7. Discussão

A contribuição central do estudo é mostrar que dependência de fornecedores contém dimensões que se tornam invisíveis quando o comprador é observado apenas por sua distribuição interna de gasto. Esse resultado amplia a literatura sobre supply base complexity: além do número e da concentração de fornecedores, a posição dos mesmos fornecedores fora da carteira focal adiciona informação relacional relevante (Choi & Krause, 2006; Borgatti & Li, 2009).

A correção LOO é decisiva para essa interpretação. Strength bruto é apropriado para representar massa monetária sistêmica, mas reaproveita o valor do próprio comprador quando usado para medir exposição. A forte alteração do ranking após a externalização confirma H1. Degree é muito menos sensível à correção. Em conjunto, a baixa associação de HHI com as medidas externalizadas e a elevada concordância entre Strength LOO e Degree LOO sustentam H2 e H3: concentração local e posição externa não são redundantes, enquanto duas operacionalizações diferentes da posição externa convergem substantivamente.

A robustez por CNPJ raiz reduz uma vulnerabilidade de mensuração importante. Matriz e filiais da mesma raiz poderiam inflar artificialmente o número de fornecedores e alterar Degree. Isso não ocorre em magnitude capaz de explicar os resultados: os rankings de concentração e exposição permanecem acima de 0,987 entre as especificações, a elegibilidade não muda e mais de 95% dos compradores classificados em discordância permanecem na mesma identificação. O teste, entretanto, não consolida grupos econômicos com múltiplas raízes, que exigiriam informação societária adicional.

A comparação internacional requer cautela. Pliatsidis (2024) é uma referência próxima por analisar concentração e redes em compras públicas gregas, mas sua unidade são subnetworks por grupo CPV e sua medida de concentração é derivada da distribuição de Degree. Portanto, os valores medianos de HHI (0,2365) e CR1 (0,3837) deste estudo não são numericamente comparáveis aos expoentes reportados para a Grécia. A contribuição comparativa adequada é qualitativa: ambos os desenhos mostram heterogeneidade na distribuição de contratos e a utilidade de estruturas de rede, mas operam em unidades econômicas distintas. Evitar a comparação direta preserva a interpretação do nosso HHI como concentração da carteira do comprador, e não como concentração de um mercado relevante.

Os testes de estresse sustentam H4 ao mostrar que a remoção direcionada dos maiores fornecedores por Strength produz perdas superiores a um nulo que já favorece fornecedores de alto Strength. O resultado caracteriza vulnerabilidade mecânica da rede observada. Em linha com Craighead et al. (2007) e Kim et al. (2015), resiliência efetiva depende também de mitigação e recuperação. Por isso, os percentuais não devem ser lidos como probabilidade de interrupção nem como perda operacional esperada.

A persistência longitudinal sustenta H5 e é relevante para uso de screening. Se os rankings mudassem completamente entre coortes adjacentes, sua utilidade gerencial seria limitada. A estabilidade observada, combinada ao efeito de composição dos entrantes, sugere que painéis devem separar mudança dentro dos compradores persistentes de mudanças provocadas pela entrada de novas unidades elegíveis.

# 8. Implicações para governança e screening

O framework pode ser traduzido em um painel de triagem que não substitui análise material de risco, mas orienta onde aprofundá-la. O uso gerencial recomendado é associar cada quadrante a perguntas adicionais, e não a rótulos automáticos de risco.

| Concentração local | Exposição externa | Leitura de screening | Verificação gerencial sugerida |
|---|---|---|---|
| menor | menor | carteira relativamente distribuída e fornecedores menos centrais externamente | monitoramento periódico; reavaliar diante de mudança material de objeto, fornecedor ou valor |
| maior | menor | dependência predominantemente local | examinar substitutos, custo e tempo de troca, desenho de lotes, especificações e barreiras locais à diversificação |
| menor | maior | exposição externa não capturada pelo HHI | mapear capacidade do fornecedor, compromissos simultâneos com outros compradores, alternativas e risco de demanda concorrente em choques sistêmicos |
| maior | maior | concentração local combinada com exposição externa elevada | priorizar avaliação de criticidade, continuidade, alternativas, plano de contingência e estratégia de transição contratual |

Os termos “menor” e “maior” são relativos aos cortes amostrais e não equivalem a limites regulatórios. O quadrante mais intenso não é sinônimo de irregularidade: sua função é sinalizar onde a combinação de concentração local e conectividade externa justifica investigação adicional.

Para gestores, o passo seguinte ao screening deve incorporar pelo menos: criticidade do objeto, disponibilidade de fornecedores substitutos, lead time de transição, capacidade produtiva e financeira, dependência tecnológica, condições de mercado, cláusulas de continuidade e possibilidade de substituição parcial. Essa sequência cria uma ponte entre o diagnóstico quantitativo e decisões de resiliência sem atribuir à métrica informação que ela não contém.

# 9. Limitações

A interpretação dos resultados está condicionada a seis limites principais. Primeiro, janeiro-junho representa uma coorte parcial de publicações e não o ano de 2025 completo; instrumentos assinados em 2025 podem ser publicados posteriormente. Segundo, `valorInicial` representa valor do instrumento, não execução financeira. Terceiro, Strength e Degree descrevem posição observada na rede e não medem capacidade produtiva, substituibilidade ou probabilidade de falha. Quarto, os testes de estresse são estáticos e não modelam duração da indisponibilidade, adaptação, estoque, renegociação ou recuperação. Quinto, os modelos fiscais são associativos e a classificação de discordância é relativa à distribuição observada. Sexto, a especificação principal distingue fornecedores por CNPJ completo; a robustez por raiz trata matriz e filiais com a mesma raiz como uma unidade, mas não consolida grupos econômicos sob controle comum que utilizem raízes distintas.

O escopo empírico principal é o Poder Executivo municipal observado no PNCP, e a cobertura depende da publicação disponível segundo os filtros documentados. A literatura diretamente comparável publicada em 2026 ainda inclui working papers e discussion papers; por isso, esses trabalhos são utilizados como fronteira recente e não como único fundamento teórico. Comparações internacionais de níveis de concentração exigem unidades compatíveis: estudos por mercado ou grupo CPV não fornecem benchmark numérico direto para HHI de carteira no nível do comprador institucional.

# 10. Conclusão

A análise mostra que concentração local da carteira e exposição externa aos fornecedores são dimensões empiricamente distintas da dependência estrutural em compras públicas municipais. A correção leave-one-buyer-out é necessária sobretudo para Strength, pois remove a contribuição do próprio comprador da posição monetária do fornecedor e evita interpretar auto-inclusão como exposição externa.

O avanço do artigo está na integração entre concentração local, exposição LOO, discordância concentração-exposição e stress testing. Essa arquitetura permanece estável ao longo das janelas mensais e, de forma importante, também quando estabelecimentos são agregados pela raiz do CNPJ: rankings, elegibilidade, discordância e resultados de choque pouco se alteram. O framework, portanto, oferece informação relacional adicional ao HHI sem depender de uma única definição de fornecedor por estabelecimento.

O uso adequado é de screening, seguido por avaliação de criticidade, substituibilidade, capacidade e continuidade. Os resultados não identificam causalidade, fraude ou probabilidade de falha. A validação anual será realizada em estudo separado com o ano completo de 2025 e captura tardia das publicações de 2026, permitindo avaliar persistência, composição e sensibilidade temporal em horizonte mais amplo.

# Referências

Borgatti, S. P., & Li, X. (2009). On social network analysis in a supply chain context. *Journal of Supply Chain Management, 45*(2), 5-22. https://doi.org/10.1111/j.1745-493X.2009.03166.x

Brasil. Ministério da Gestão e da Inovação em Serviços Públicos. (2026). *Portal Nacional de Contratações Públicas: Dados Abertos*. https://www.gov.br/pncp/pt-br/acesso-a-informacao/dados-abertos

Brasil. Secretaria do Tesouro Nacional. (2026). *SICONFI: documentação e Declaração de Contas Anuais*. https://www.siconfi.tesouro.gov.br/

Choi, T. Y., & Krause, D. R. (2006). The supply base and its complexity: Implications for transaction costs, risks, responsiveness, and innovation. *Journal of Operations Management, 24*(5), 637-652. https://doi.org/10.1016/j.jom.2005.07.002

Caniëls, M. C. J., & Gelderman, C. J. (2005). Purchasing strategies in the Kraljic matrix: A power and dependence perspective. *Journal of Purchasing and Supply Management, 11*(2-3), 141-155. https://doi.org/10.1016/j.pursup.2005.10.004

Bode, C., & Wagner, S. M. (2015). Structural drivers of upstream supply chain complexity and the frequency of supply chain disruptions. *Journal of Operations Management, 36*, 215-228. https://doi.org/10.1016/j.jom.2014.12.004

Craighead, C. W., Blackhurst, J., Rungtusanatham, M. J., & Handfield, R. B. (2007). The severity of supply chain disruptions: Design characteristics and mitigation capabilities. *Decision Sciences, 38*(1), 131-156. https://doi.org/10.1111/j.1540-5915.2007.00151.x

Fonseca, F. T. (2025). *Patterns in Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil* [Master's dissertation, NOVA Information Management School]. http://hdl.handle.net/10362/190144

Fountoukidis, I. G., Antoniou, I. E., & Varsakelis, N. C. (2023). Competitive conditions in the public procurement markets: an investigation with network analysis. *Journal of Industrial and Business Economics, 50*, 347-368. https://doi.org/10.1007/s40812-022-00251-z

Fountoukidis, I., Dafli, E., Antoniou, I., & Varsakelis, N. (2026a). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN working paper. https://doi.org/10.2139/ssrn.6765160

Fountoukidis, I. G., Dafli, E. L., Antoniou, I. E., & Varsakelis, N. C. (2026b). *Recurrence as a Governance Signal: Diagnostic Network Metrics for Public Procurement Oversight in Greece*. GreeSE Papers on Greece and Southeast Europe, No. 219, Hellenic Observatory, London School of Economics and Political Science.

Hendricks, K. B., & Singhal, V. R. (2003). The effect of supply chain glitches on shareholder wealth. *Journal of Operations Management, 21*(5), 501-522. https://doi.org/10.1016/j.jom.2003.02.003

Herfindahl, O. C. (1950). *Concentration in the U.S. Steel Industry* [Doctoral dissertation, Columbia University].

Hirschman, A. O. (1945). *National Power and the Structure of Foreign Trade*. University of California Press.

Jiang, S., Yeung, A. C. L., Han, Z., & Huo, B. (2023). The effect of customer and supplier concentrations on firm resilience during the COVID-19 pandemic: Resource dependence and power balancing. *Journal of Operations Management, 69*(3), 497-518. https://doi.org/10.1002/joom.1236

Kim, Y., Chen, Y.-S., & Linderman, K. (2015). Supply network disruption and resilience: A network structural perspective. *Journal of Operations Management, 33-34*, 43-59. https://doi.org/10.1016/j.jom.2014.10.006

Kleindorfer, P. R., & Saad, G. H. (2005). Managing disruption risks in supply chains. *Production and Operations Management, 14*(1), 53-68. https://doi.org/10.1111/j.1937-5956.2005.tb00009.x

Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.

OECD. (2024). *Toolkit for Resilient Public Procurement Strategies to Minimise Risks of Supply Disruption*. OECD.

Pfeffer, J., & Salancik, G. R. (1978). *The External Control of Organizations: A Resource Dependence Perspective*. Harper & Row.

Pliatsidis, A. C. (2024). Analyzing concentration in the Greek public procurement market: a network theory approach. *Journal of Industrial and Business Economics, 51*, 431-480. https://doi.org/10.1007/s40812-023-00291-z

Polyviou, M., Wiedmer, R., Chae, S., Rogers, Z. S., & Mena, C. (2023). To concentrate or to diversify the supply base? Implications from the U.S. apparel supply chain during the COVID-19 pandemic. *Journal of Business Logistics, 44*(3), 502-527. https://doi.org/10.1111/jbl.12335

Popa, M. (2019). Uncovering the structure of public procurement transactions. *Business and Politics, 21*(3), 351-384. https://doi.org/10.1017/bap.2019.1

Sturm, N. F., Candia, C., Damásio, B., & Pinheiro, F. L. (2025). High earnings through firm influence: the role of hierarchical structures in public procurement. *EPJ Data Science, 14*, Article 27. https://doi.org/10.1140/epjds/s13688-025-00543-z

Uzzi, B. (1996). The sources and consequences of embeddedness for the economic performance of organizations: The network effect. *American Sociological Review, 61*(4), 674-698. https://doi.org/10.2307/2096399

Wachs, J., Fazekas, M., & Kertész, J. (2021). Corruption risk in contracting markets: a network science perspective. *International Journal of Data Science and Analytics, 12*, 45-60. https://doi.org/10.1007/s41060-019-00204-1

Waxenecker, H., & Prell, C. (2024). Corruption dynamics in public procurement: A longitudinal network analysis of local construction contracts in Guatemala. *Social Networks, 79*, 154-167. https://doi.org/10.1016/j.socnet.2024.07.001

# Reprodutibilidade e disponibilidade de dados

O repositório público do projeto está disponível em:

https://github.com/Jacson-Nascimento/Jacson-Nascimento/tree/research/dois-papers-robustez-2025/research/dependencia-fornecedores-compras-publicas

Ele contém scripts, bases públicas minimizadas de fornecedores pessoa jurídica, resultados e logs de execução necessários para auditar as análises. Os dados brutos são obtidos das interfaces públicas e dados abertos do PNCP; o repositório documenta as regras de coleta, filtros, chaves e transformação aplicadas antes da produção das bases analíticas.

Os principais scripts são `analisar_acumulado_2025_global.py`, `robustez_estrutural_generica.py`, `robustez_modelos_municipio_generica.py`, `calcular_exposicao_loo_generica.py`, `diagnosticos_longitudinais_loo_jan_jun_2025.py` e `robustez_cnpj_raiz_paper1.py`.

Os resultados auditáveis permanecem em `results/carteira_acumulada_2025_06_global/`, `results/robustez_estrutural_2025_06/`, `results/robustez_modelos_municipio_2025_06/`, `results/exposicao_loo_2025_04/`, `results/exposicao_loo_2025_05/`, `results/exposicao_loo_2025_06/`, `results/diagnosticos_longitudinais_loo_jan_jun_2025/` e `results/robustez_cnpj_raiz_2025_06/`. Cada robustez nova possui log de execução versionado junto às saídas correspondentes.
