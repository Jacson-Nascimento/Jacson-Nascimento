# CONCENTRAÇÃO DE INFLUÊNCIA E REVERSÃO DA MAIORIA INFORMACIONAL

## Uma análise complementar da dinâmica de manada em redes organizacionais

**Jacson Cruz do Nascimento**  
Mestre em Economia | Bacharel em Ciências Contábeis  
Brasília, DF, Brasil  
ORCID: 0009-0006-6535-9569  
ISNI: 0000 0005 3052 9869

Artigo complementar ao preprint *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*.  
DOI da realização de referência: 10.5281/zenodo.21985858.

## Resumo

Este estudo realiza uma análise secundária do experimento computacional apresentado em *Dinâmica de Manada Organizacional*, utilizando a realização de referência de 10.000 replicações, os sinais individuais dos 60 agentes, a matriz de influência, os pesos estacionários e os desfechos de propagação arquivados no material suplementar. O objetivo é investigar a anatomia da reversão informacional, definida como a situação em que a maioria dos agentes possui informação individual na direção correta, mas o agregado ponderado pela estrutura de influência aponta para a direção errada. Em todas as 10.000 replicações, a maioria nominal estava correta, com mínimo de 63,33% de agentes corretos. Ainda assim, o agregado estrutural foi incorreto em 17,29% das replicações. Um único executivo concentra 52,65% do peso estacionário e os seis agentes superiores, 95,64%, reduzindo o tamanho efetivo de fontes de 60 agentes nominais para 3,14. Quando o executivo estava errado, a probabilidade de semente estrutural incorreta foi 55,83%, contra 0,57% quando estava correto. Uma análise contrafactual, mantendo constantes a rede e os 10.000 vetores de evidência, mostra que o aumento da sensibilidade hierárquica reduz o tamanho efetivo de fontes e eleva progressivamente a frequência de reversões. O artigo também propõe uma medida contínua de intensidade da semente incorreta. Essa intensidade discrimina fortemente quais sementes são posteriormente amplificadas em consenso incorreto. Os resultados reforçam a distinção entre número nominal de participantes e independência informacional efetiva. As conclusões permanecem restritas ao mecanismo computacional analisado e não constituem estimativas de prevalência em organizações reais.

**Palavras-chave:** efeito manada; dinâmica de opiniões; auditoria; julgamento profissional; hierarquia; influência social; independência informacional; consenso; redes organizacionais; Monte Carlo.

## 1 Introdução

Organizações recorrem a equipes, comitês, instâncias de revisão e supervisão para agregar informação e reduzir erros individuais. Essa lógica pressupõe que diferentes participantes aportem informação com algum grau de independência. O número de pessoas envolvidas, entretanto, não é equivalente ao número de fontes informacionais efetivas quando posições de maior status recebem peso muito superior às demais.

Modelos de dinâmica de opiniões demonstram que redes de influência podem produzir convergência mesmo a partir de sinais heterogêneos. A literatura de cascatas informacionais acrescenta que indivíduos podem abandonar sinais privados ao observar manifestações alheias. Evidência experimental também mostra que influência social pode reduzir a diversidade de respostas sem elevar a acurácia coletiva. Em auditoria, estudos recentes documentam maior conformidade de auditores juniores diante de consenso de membros seniores e efeitos das preferências conhecidas de sócios sobre julgamentos profissionais.

O estudo-base formalizou três etapas: evidência individual, formação da semente estrutural e amplificação social. O presente artigo desloca a pergunta. Em vez de investigar novamente se uma semente incorreta pode ser amplificada, examina como uma maioria informacional correta pode ser derrotada pela estrutura de influência e quais características dessa reversão antecipam sua propagação.

A contribuição é tripla. Primeiro, distingue maioria numérica e maioria estrutural. Segundo, decompõe o agregado pelos níveis hierárquicos e identifica onde a reversão se forma. Terceiro, substitui parcialmente a classificação binária da semente por uma medida contínua de intensidade, permitindo diferenciar sementes marginais de sementes fortemente deslocadas.

## 2 Estrutura analítica

Seja e_i a evidência recebida pelo agente i e theta o estado verdadeiro. A fração nominal de agentes corretos é:

A = (1/N) soma_i 1[sign(e_i) = sign(theta)].

Uma maioria informacional correta existe quando A > 0,5.

A rede, porém, agrega sinais segundo o vetor estacionário pi, definido por pi'W = pi' e soma_i pi_i = 1. O agregado estrutural é:

Z = pi'e.

A semente estrutural incorreta é:

S = 1[sign(Z) != sign(theta)].

Define-se reversão informacional quando A > 0,5 e S = 1.

A concentração é resumida por:

n_eff = 1 / soma_i pi_i^2.

Quando os pesos são próximos, n_eff aproxima-se de N. Quando poucos agentes concentram influência, n_eff cai.

Para distinguir sementes de diferentes magnitudes, define-se, condicionalmente a S=1:

m = -theta (pi'e).

Como no experimento theta=-1, sementes incorretas possuem pi'e > 0 e, portanto, m > 0. Valores pequenos representam reversões próximas da fronteira; valores elevados representam agregados estruturalmente mais deslocados para a direção errada.

## 3 Dados e método

A análise utiliza exatamente a realização de referência depositada no Zenodo sob DOI 10.5281/zenodo.21985858. São 10.000 replicações com 60 agentes. A rede-base é Watts-Strogatz, com seis vizinhos iniciais, probabilidade de reconexão de 0,12 e auto-influência na diagonal antes da ponderação hierárquica. A seed documentada é 20260816 e o gerador de referência utiliza NumPy default_rng, PCG64.

A hierarquia contém um executivo, cinco gestores, doze seniores e 42 demais agentes. No cenário de estresse, sigma_i = 0,90 + h_i. Assim, maior posição hierárquica está associada, por construção, a maior ruído. Trata-se de escolha de estresse, não de estimativa sobre organizações reais.

A análise complementar executa cinco blocos. Primeiro, verifica a coexistência entre maioria nominal correta e agregado estrutural errado. Segundo, decompõe pi'e pelos quatro grupos hierárquicos. Terceiro, estima P(S) condicionada ao erro do executivo e ao número de gestores errados. Quarto, mantém fixos A e os 10.000 vetores de sinais e altera somente kappa, recalculando pi(kappa), n_eff e P(S). Quinto, divide as 1.729 sementes incorretas em quintis de m e observa a incidência de manada em dois cenários arquivados: beta=0,70, c=0,90 e beta=0,75, c=0,95.

Como diagnóstico adicional, estima-se regressão logística de S sobre erro do executivo e contagens de erros entre gestores, seniores e demais agentes. Esse modelo é descritivo da realização simulada e não deve ser interpretado como inferência populacional sobre organizações humanas.

## 4 Resultados

### 4.1 A maioria correta pode perder sem estar próxima de um empate

A fração média de sinais corretos foi 84,0247%, e a menor fração correta observada foi 63,33%. Portanto, todas as 10.000 replicações possuíam maioria nominal correta. Ainda assim, 1.729 delas, 17,29%, produziram semente estrutural incorreta.

Entre as 1.729 reversões, a mediana da fração correta foi 81,67%. Em 75,59% dos casos de reversão, pelo menos 80% dos agentes possuíam sinais corretos. Em 36,26%, pelo menos 85% estavam corretos. Em 6,30%, 90% ou mais estavam corretos.

O erro agregado, portanto, não surge de maioria informacional dividida. Surge da ponderação estrutural dos sinais.

### 4.2 Sessenta agentes nominais equivalem a pouco mais de três fontes efetivas

| Grupo | N | sigma | Sinais corretos | Peso estacionário total |
|---|---:|---:|---:|---:|
| Executivo | 1 | 1,90 | 69,75% | 52,65% |
| Gestores | 5 | 1,55 | 73,79% | 42,99% |
| Seniores | 12 | 1,20 | 79,76% | 3,18% |
| Demais | 42 | 0,90 | 86,80% | 1,18% |

O executivo concentra 52,65% da influência estacionária. Os cinco gestores acrescentam 42,99%. Os 54 agentes restantes compartilham apenas 4,36% do peso. O tamanho efetivo de fontes é 3,1408.

O peso do executivo é aproximadamente 1.867 vezes o peso médio de um agente do grupo inferior. O peso médio de um gestor é cerca de 305 vezes o peso médio desse grupo.

### 4.3 O erro do executivo é quase necessário, mas não suficiente

O executivo recebeu sinal errado em 30,25% das replicações. Condicionada a esse evento, a probabilidade de semente estrutural incorreta foi 55,83%. Quando o executivo estava correto, foi 0,57%.

Entre as sementes incorretas, 97,69% ocorreram com executivo errado. Isso não implica determinação mecânica. Em aproximadamente 44% das replicações com executivo errado, os demais sinais ainda foram suficientes para preservar o sinal correto do agregado.

Quando o executivo estava errado, P(S) aumentou com o número de gestores também errados:

| Gestores errados | N | P(S | executivo errado) |
|---:|---:|---:|
| 0 | 677 | 34,42% |
| 1 | 1.200 | 51,25% |
| 2 | 820 | 67,07% |
| 3 | 279 | 87,10% |
| 4 | 44 | 97,73% |
| 5 | 5 | 100,00% |

A identidade estrutural do erro importa mais do que a simples contagem de agentes errados.

### 4.4 A decomposição do agregado localiza a reversão

Nas replicações sem semente errada, a contribuição média do executivo para pi'e foi -0,818. Nas replicações com semente errada, foi +0,890. A contribuição média dos gestores permaneceu negativa, passando de -0,453 para -0,291. Seniores e demais agentes apresentaram contribuições médias pequenas devido ao peso estrutural reduzido.

O mecanismo não equivale à afirmação genérica de que níveis inferiores são pouco informados. No desenho, ocorre o oposto. Eles são, em média, mais precisos. O problema é que sua capacidade de alterar o agregado é mínima.

### 4.5 Concentração crescente produz reversões mantendo a informação constante

| kappa | P(S) | n_eff | Peso executivo | Peso Top 6 |
|---:|---:|---:|---:|---:|
| 0 | 0,00% | 59,19 | 1,43% | 10,24% |
| 1 | 0,00% | 45,58 | 4,66% | 25,15% |
| 2 | 0,39% | 19,96 | 12,47% | 49,65% |
| 3 | 4,61% | 8,75 | 24,97% | 73,88% |
| 4 | 11,33% | 4,84 | 39,17% | 88,79% |
| 5 | 17,29% | 3,14 | 52,65% | 95,64% |

O exercício mantém a mesma rede de adjacência e os mesmos 10.000 conjuntos de evidências. A única alteração é o reponderamento hierárquico. Entre kappa=0 e kappa=5, o tamanho efetivo de fontes cai aproximadamente 94,7% e a realização passa de zero reversões para 1.729.

Os valores não definem limiar universal. Eles demonstram uma propriedade mecânica do cenário: a concentração é suficiente para converter situações previamente corretas em agregados incorretos sem mudar a informação disponível.

### 4.6 A semente incorreta possui intensidade

| Quintil | Margem média | P(H|S), beta=0,70 c=0,90 | P(H|S), beta=0,75 c=0,95 |
|---:|---:|---:|---:|
| Q1 | 0,076 | 0,00% | 55,49% |
| Q2 | 0,233 | 19,94% | 100,00% |
| Q3 | 0,435 | 93,91% | 100,00% |
| Q4 | 0,717 | 100,00% | 100,00% |
| Q5 | 1,316 | 100,00% | 100,00% |

No cenário beta=0,70 e c=0,90, nenhuma semente do primeiro quintil produz manada. No terceiro quintil, 93,91% produzem. Nos dois quintis superiores, a ocorrência é total. No cenário mais extremo, mesmo o primeiro quintil apresenta 55,49% de manada, e todos os demais chegam a 100%.

A AUC da margem para classificar eventos de manada é 0,993 no primeiro cenário e 0,998 no segundo. Esses números não constituem validação preditiva externa. Previsor e desfecho pertencem ao mesmo mecanismo matemático. O resultado mostra apenas que a codificação binária de S descarta informação relevante sobre o grau de vulnerabilidade da semente.

### 4.7 Diagnóstico logístico

O modelo logístico descritivo apresentou AUC de 0,944. Mantidas as demais contagens constantes, o erro do executivo correspondeu a odds ratio aproximada de 358,25, e cada gestor adicional errado a odds ratio de 2,35. As contagens entre seniores e demais agentes acrescentaram pouca capacidade classificatória depois de considerados os estratos superiores.

Esses coeficientes não devem ser transportados para organizações reais. Eles resumem a geometria do cenário-base.

## 5 Discussão

Os resultados distinguem participação formal de contribuição informacional efetiva. A organização simulada contém 60 agentes, mas a distribuição de pesos reduz o sistema a pouco mais de três fontes efetivas. Assim, grande maioria correta pode coexistir com decisão estrutural errada.

A interpretação adequada não é que hierarquia seja inerentemente prejudicial. O cenário foi deliberadamente construído com associação negativa entre posição e precisão. Se agentes mais influentes forem também mais informados, concentração pode melhorar o resultado. A questão substantiva é a correspondência entre poder e qualidade informacional.

A evidência experimental em auditoria fornece plausibilidade comportamental ao mecanismo, sem validar seus parâmetros. Cardinaels et al. (2025) encontram maior conformidade de auditores juniores quando o consenso se origina de membros seniores e menor conforto para compartilhar avaliação própria em determinadas condições. Ying, Patel e Dela Cruz (2023) mostram que pressão percebida de influência social reforça o efeito das preferências conhecidas de sócios sobre julgamentos céticos. Gold, Kadous e Leiby (2024) examinam como status social de especialistas influencia avaliações de estimativas complexas.

O resultado complementar mais relevante é que sementes erradas não são homogêneas. Sua distância da fronteira ajuda a explicar quanto de pressão social adicional é necessário para produzir consenso incorreto. O objeto de estudo pode, portanto, ser expandido de P(H|S) para P(H|S,m,W,beta,c).

## 6 Implicações para auditoria e governança

A implicação imediata não é construir indicador operacional a partir de n_eff ou da margem m. Nenhuma dessas medidas foi calibrada em equipes humanas. A implicação é metodológica: revisões múltiplas não garantem múltiplas origens independentes de evidência quando os revisores conhecem previamente a posição dominante e possuem capacidade desigual de influenciar a conclusão.

Isso sugere hipóteses testáveis para experimentos: registro individual antes da discussão; manifestação simultânea; ocultação temporária da posição do superior; separação entre status e expertise; e inclusão de revisão por fonte informacional independente. A eficácia dessas intervenções precisa ser estimada, não presumida.

## 7 Limitações

O estudo é teórico-computacional. Não há participantes humanos. Os parâmetros de influência, conformidade e sensibilidade hierárquica não foram estimados em organizações. O cenário-base associa intencionalmente maior hierarquia a maior ruído. A estática comparativa utiliza uma única rede e a mesma realização de 10.000 vetores de sinais. Portanto, demonstra o efeito mecânico do reponderamento dentro desse sistema, não uma distribuição universal de limiares.

Este artigo também restringe seus novos resultados ao núcleo integralmente reproduzível do pacote publicado. Módulos de Sobol, topologias alternativas e extensão não linear do manuscrito-base não são reaproveitados aqui como base de novos resultados quando a especificação integral necessária à reprodução exata não acompanha o mesmo pacote.

## 8 Agenda de validação

O passo seguinte deve ser empírico. Um experimento controlado pode fornecer sinais privados de precisão conhecida e manipular conhecimento prévio da posição de um superior, ordem das manifestações e possibilidade de registrar avaliação privada antes da discussão. Isso permitiria separar evidência, crença privada e manifestação pública.

Uma segunda etapa pode estimar parâmetros aproximados de influência e conformidade. Uma terceira pode testar redes de equipes profissionais em ambientes controlados. Somente depois disso medidas de concentração ou intensidade de semente deveriam ser consideradas para uso aplicado.

## 9 Conclusão

No cenário analisado, a maioria não perde por falta de informação correta. Ela perde porque a estrutura determina quais informações contam. Todas as 10.000 replicações possuíam maioria nominal correta, mas 17,29% produziram agregado estrutural incorreto. O aumento da sensibilidade hierárquica, mantendo exatamente a mesma informação disponível, reduziu o tamanho efetivo de fontes de 59,19 para 3,14 e elevou as reversões de zero para 17,29%.

O erro do executivo esteve presente em 97,69% das sementes erradas, mas não foi suficiente por si só. A reversão dependeu da combinação entre posição estrutural, magnitude dos sinais e contribuições dos demais agentes. Além disso, a intensidade da semente antecipou fortemente sua amplificação posterior.

A conclusão permanece restrita ao desenho computacional. Ela não demonstra que organizações reais possuem as mesmas magnitudes e não sustenta a tese de que hierarquia seja necessariamente nociva. O resultado mais defensável é outro: contar participantes não é equivalente a contar fontes informacionais independentes.

A pergunta relevante para pesquisa futura é: quantas fontes de informação tiveram capacidade real de alterar a conclusão?

## Referências

BANERJEE, A. V. A simple model of herd behavior. *The Quarterly Journal of Economics*, v. 107, n. 3, p. 797-817, 1992.

BIKHCHANDANI, S.; HIRSHLEIFER, D.; WELCH, I. A theory of fads, fashion, custom, and cultural change as informational cascades. *Journal of Political Economy*, v. 100, n. 5, p. 992-1026, 1992. DOI: 10.1086/261849.

CARDINAELS, E.; DARMAWAN, V.; REUSEN, E.; STOUTHUYSEN, K. The influence of team consensus and inclusive climate on junior auditors’ conformity and risk assessment sharing. *Journal of Accounting and Public Policy*, v. 52, art. 107334, 2025. DOI: 10.1016/j.jaccpubpol.2025.107334.

DEGROOT, M. H. Reaching a consensus. *Journal of the American Statistical Association*, v. 69, n. 345, p. 118-121, 1974. DOI: 10.1080/01621459.1974.10480137.

GOLD, A.; KADOUS, K.; LEIBY, J. Does status equal substance? The effects of specialist social status on auditor assessments of complex estimates. *The Accounting Review*, v. 99, n. 5, p. 197-222, 2024. DOI: 10.2308/TAR-2021-0298.

LORENZ, J.; RAUHUT, H.; SCHWEITZER, F.; HELBING, D. How social influence can undermine the wisdom of crowd effect. *Proceedings of the National Academy of Sciences*, v. 108, n. 22, p. 9020-9025, 2011. DOI: 10.1073/pnas.1008636108.

MORRISON, E. W.; MILLIKEN, F. J. Organizational silence: a barrier to change and development in a pluralistic world. *Academy of Management Review*, v. 25, n. 4, p. 706-725, 2000. DOI: 10.5465/AMR.2000.3707697.

NASCIMENTO, J. C. do. *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*. Zenodo, 2026. DOI: 10.5281/zenodo.21985858.

YING, S. X.; PATEL, C.; DELA CRUZ, A. L. The influence of partners' known preferences on auditors' sceptical judgements: the moderating role of perceived social influence pressure. *Accounting & Finance*, v. 63, n. 3, p. 3193-3215, 2023. DOI: 10.1111/acfi.13030.

## Disponibilidade de dados e código

A realização de referência está depositada no Zenodo, DOI 10.5281/zenodo.21985858. O código-base encontra-se em research/dinamica-manada-organizacional. As rotinas complementares deste artigo ficam em second-paper/ e reutilizam a mesma matriz, a mesma seed e os mesmos 10.000 vetores de evidência.

## Declaração de escopo

As probabilidades apresentadas descrevem o comportamento interno do modelo sob condições especificadas. Não devem ser interpretadas como prevalência estimada de conformidade, silêncio ou efeito manada em equipes de auditoria ou outras organizações.
