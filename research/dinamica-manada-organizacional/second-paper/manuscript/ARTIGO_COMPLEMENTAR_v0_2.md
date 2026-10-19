# CONCENTRAÇÃO DE INFLUÊNCIA E REVERSÃO DA MAIORIA INFORMACIONAL

## Uma análise secundária da dinâmica de manada em redes organizacionais

**Jacson Cruz do Nascimento**  
Mestre em Economia | Bacharel em Ciências Contábeis  
Brasília, DF, Brasil  
ORCID: 0009-0006-6535-9569  
ISNI: 0000 0005 3052 9869

**Versão 0.2 - revisão técnico-acadêmica de 12 de setembro de 2026**

Artigo complementar ao preprint *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*.  
DOI da realização de referência: 10.5281/zenodo.21985858.

## Resumo

Este estudo realiza uma análise secundária do experimento computacional apresentado em *Dinâmica de Manada Organizacional* e investiga a reversão informacional, definida como a situação em que a maioria dos agentes possui sinais individuais na direção correta, mas o agregado ponderado pela estrutura de influência aponta para a direção errada. A contribuição não consiste em demonstrar genericamente que centralização pode prejudicar a sabedoria coletiva, resultado já estabelecido na literatura de aprendizagem em redes, mas em decompor esse mecanismo no arcabouço organizacional hierárquico do estudo-base e relacioná-lo à formação e à intensidade da semente de manada. Na realização publicada de 10.000 replicações, todas as maiorias nominais estavam corretas, com mínimo de 63,33% de agentes corretos, enquanto 17,29% das replicações produziram agregado estrutural incorreto. Sob os sinais gaussianos independentes do modelo, a probabilidade de reversão admite solução fechada e é igual a 17,01% no cenário-base, valor consistente com a simulação. Um executivo concentra 52,65% do peso estacionário e os seis agentes superiores, 95,64%, reduzindo o tamanho efetivo de fontes de 60 agentes nominais para 3,14. A robustez estrutural foi examinada em 500 novas redes Watts-Strogatz e em 1.000 permutações dos papéis hierárquicos na rede publicada. Nas novas redes, a probabilidade exata média de reversão foi 17,46%, com intervalo estrutural empírico de 16,93% a 18,43%. Nas permutações de papéis, a média foi 22,35%, indicando que a posição publicada não constitui uma configuração excepcionalmente adversa. A intensidade da semente incorreta diferencia fortemente os casos posteriormente amplificados em consenso incorreto, e o resultado é estável a cortes de manada entre 70% e 90%. As conclusões descrevem propriedades do modelo e não estimam prevalência de conformidade ou efeito manada em organizações reais.

**Palavras-chave:** efeito manada; dinâmica de opiniões; auditoria; julgamento profissional; hierarquia; influência social; independência informacional; sabedoria coletiva; redes organizacionais; Monte Carlo.

## 1 Introdução

Organizações recorrem a equipes, comitês, instâncias de revisão e estruturas de supervisão para agregar informação e reduzir erros individuais. Essa lógica pressupõe que diferentes participantes tragam sinais que preservem algum grau de independência. O número nominal de participantes, entretanto, não é equivalente ao número de fontes efetivamente capazes de alterar uma conclusão quando a estrutura atribui pesos muito diferentes às manifestações.

Esse problema não é novo na teoria de aprendizagem em redes. DeGroot (1974) formalizou a convergência de opiniões por médias ponderadas. Golub e Jackson (2010) mostram que a sabedoria coletiva em sociedades grandes depende de a influência do agente mais influente tornar-se pequena. Becker, Brackbill e Centola (2017) demonstram teórica e experimentalmente que redes descentralizadas podem melhorar a acurácia coletiva, enquanto redes centralizadas deslocam o julgamento em direção ao indivíduo central. Tian, Wang e Bullo (2023) mostram formalmente que a influência tende a melhorar a sabedoria quando maior poder social é destinado a indivíduos relativamente mais precisos e a deteriorá-la quando ocorre o contrário. Lorenz et al. (2011), por sua vez, mostram que influência social pode reduzir diversidade sem melhora correspondente da precisão.

Portanto, este artigo não reivindica como descoberta a proposição geral de que centralização pode prejudicar decisões coletivas. Sua contribuição é mais específica. O estudo-base introduziu um modelo organizacional no qual hierarquia, qualidade do sinal, influência social e custo de discordância são separados. A partir da mesma massa de dados, o presente trabalho pergunta: **como uma maioria nominalmente correta é revertida pela estrutura de influência, quanto dessa reversão pode ser calculado analiticamente e quais características da semente errada antecipam sua posterior amplificação?**

A aplicação à auditoria é motivada por evidência comportamental independente. Cardinaels et al. (2025) mostram que auditores juniores tendem a conformar-se mais a consensos formados por membros seniores e podem sentir menor conforto para compartilhar avaliações divergentes. Ying, Patel e Dela Cruz (2023) encontram que pressão percebida de influência social reforça o efeito das preferências conhecidas de sócios sobre julgamentos céticos. Gold, Kadous e Leiby (2024) mostram que sinais de status de especialistas podem ser confundidos com competência em avaliações de estimativas complexas. Esses estudos não validam os parâmetros do presente modelo, mas tornam plausível investigar separadamente status, informação e influência.

A análise oferece quatro extensões em relação ao artigo-base. Primeiro, define e quantifica a reversão entre maioria nominal e agregado estrutural. Segundo, deriva a probabilidade exata de semente errada sob a distribuição gaussiana já assumida pelo modelo, reduzindo a dependência de uma realização Monte Carlo específica. Terceiro, verifica robustez em novas redes e em diferentes posições dos papéis hierárquicos. Quarto, trata a semente errada como variável de intensidade, e não apenas como evento binário, para estudar sua suscetibilidade à amplificação.

## 2 Estrutura analítica

### 2.1 Maioria nominal e agregado estrutural

Seja (e_i) a evidência recebida pelo agente (i) e (	heta) o estado verdadeiro. A fração nominal de sinais corretos é:

[
A=rac{1}{N}sum_{i=1}^{N}1{operatorname{sign}(e_i)=operatorname{sign}(	heta)}.
]

Existe maioria informacional nominalmente correta quando (A>0,5).

A rede agrega sinais segundo o vetor estacionário (pi), definido por:

[
pi'W=pi', qquad sum_i pi_i=1.
]

O agregado estrutural é:

[
Z=pi'e.
]

A semente estrutural incorreta é:

[
S=1{operatorname{sign}(Z)
eqoperatorname{sign}(	heta)}.
]

Define-se **reversão informacional** quando a maioria nominal está correta, (A>0,5), mas (S=1).

### 2.2 Concentração e número efetivo de fontes

A concentração estrutural pode ser resumida por:

[
n_{eff}=rac{1}{sum_i pi_i^2}.
]

Quando todos os pesos são semelhantes, (n_{eff}) aproxima-se de (N). Quando poucos agentes concentram influência, o valor diminui. Essa medida descreve concentração de influência, não independência causal observada entre pessoas.

### 2.3 Probabilidade exata de reversão sob sinais gaussianos

No desenho-base:

[
e_i=	heta+arepsilon_i, qquad arepsilon_isim N(0,sigma_i^2),
]

com choques independentes entre agentes. Logo:

[
Z=pi'e=	heta+sum_i pi_iarepsilon_i.
]

Portanto:

[
Zsim N(	heta,V_pi),
]

em que:

[
V_pi=sum_i pi_i^2sigma_i^2.
]

Para (	heta
eq0), a probabilidade de o agregado estrutural assumir sinal oposto ao estado verdadeiro é:

[
P(S=1)=Phileft(-rac{|	heta|}{sqrt{V_pi}}ight).
]

A expressão mostra que o risco de reversão não depende apenas de concentração. Quando a precisão é heterogênea, importa **quem recebe o peso**. Duas redes com (n_{eff}) semelhante podem apresentar riscos diferentes se o peso estiver concentrado em agentes com (sigma_i) distintos. A quantidade (V_pi) combina influência e ruído informacional.

### 2.4 Intensidade da semente incorreta

A classificação (S) é binária. Para distinguir sementes próximas da fronteira de sementes fortemente deslocadas, define-se, condicionalmente a (S=1):

[
m=-	heta(pi'e).
]

Como o experimento usa (	heta=-1), sementes incorretas possuem (pi'e>0), de modo que (m>0). Valores pequenos representam reversões marginais. Valores elevados representam agregados estruturalmente mais deslocados para a direção errada.

## 3 Dados e método

### 3.1 Status da análise

Este trabalho é uma análise secundária e exploratória formulada após a conclusão do estudo-base. Não houve pré-registro do segundo artigo. Os 10.000 vetores de sinais e a rede de referência já existiam antes desta análise e permanecem inalterados. As extensões analíticas e os testes adicionais de robustez da versão 0.2 foram introduzidos após revisão técnico-acadêmica interna e são identificados como verificações posteriores, não como análises confirmatórias pré-especificadas.

Essa distinção é relevante para evitar interpretação indevida de resultados pós-hoc como hipóteses confirmadas ex ante.

### 3.2 Massa de referência

A análise principal reutiliza a realização depositada no Zenodo sob DOI 10.5281/zenodo.21985858. São 10.000 replicações com 60 agentes. A rede-base é Watts-Strogatz, com seis vizinhos iniciais, probabilidade de reconexão (p=0,12) e auto-influência na diagonal antes da ponderação hierárquica. A seed documentada é 20260816 e o gerador de referência utiliza NumPy default_rng, PCG64.

A hierarquia contém um executivo, cinco gestores, doze seniores e 42 demais agentes. No cenário de estresse:

[
sigma_i=0,90+h_i.
]

Assim, maior posição hierárquica está associada, por construção, a maior ruído. Trata-se de cenário de estresse destinado a colocar poder e precisão em conflito. Não é uma estimativa sobre executivos, gestores ou auditores reais.

### 3.3 Estratégia de análise

A análise possui seis blocos.

1. Verificação da coexistência entre maioria nominal correta e agregado estrutural incorreto.
2. Decomposição de (pi'e) pelos quatro níveis hierárquicos.
3. Cálculo de (P(S)) condicionado ao erro do executivo e ao número de gestores errados.
4. Estática comparativa em (kappa), mantendo fixos a rede e os 10.000 vetores de evidência.
5. Cálculo analítico de (P(S)) para cada (kappa).
6. Relação entre intensidade (m) e propagação posterior nos cenários ((eta,c)=(0,70,0,90)) e ((0,75,0,95)).

As medidas AUC e a regressão logística anteriormente exploradas são mantidas apenas no material suplementar como diagnósticos internos. Elas não são tratadas como validação preditiva, pois preditores e desfechos pertencem ao mesmo mecanismo matemático.

### 3.4 Robustez estrutural

Foram adicionados dois exercícios determinísticos de robustez.

No primeiro, geram-se 500 novas redes Watts-Strogatz com os mesmos parâmetros (N=60), (k=6) e (p=0,12), mantendo a atribuição hierárquica original. Para cada rede, calcula-se (W), (pi), (n_{eff}) e a probabilidade exata de reversão.

No segundo, preserva-se a rede publicada e realizam-se 1.000 permutações pseudoaleatórias dos papéis hierárquicos entre os nós. O par ((h_i,sigma_i)) é movido conjuntamente, preservando a associação entre posição hierárquica e precisão do cenário de estresse. Esse exercício testa se o resultado publicado depende de o executivo ter sido alocado, por acaso, a uma posição particularmente influente da rede.

As seeds dessas extensões são documentadas no código da versão 0.2.

### 3.5 Sensibilidade ao corte de manada

O artigo-base define manada como pelo menos 80% dos agentes terminando em direção incorreta. Para avaliar a dependência desse critério, a versão 0.2 recalcula (P(H|S)) para cortes (	au) entre 0,70 e 0,90.

## 4 Resultados

### 4.1 A maioria correta pode ser revertida sem estar próxima de um empate

A fração média de sinais corretos na realização de referência foi 84,0247%, e a menor fração observada foi 63,33%. Portanto, todas as 10.000 replicações possuíam maioria nominal correta.

Ainda assim, 1.729 replicações, 17,29%, produziram agregado estrutural incorreto.

Entre essas 1.729 reversões, a mediana da fração correta foi 81,67%. Em 75,59% dos casos, pelo menos 80% dos agentes possuíam sinal correto. Em 36,26%, pelo menos 85% estavam corretos. Em 6,30%, 90% ou mais estavam corretos.

A reversão não decorre, portanto, de uma votação nominal quase empatada.

### 4.2 A estimativa Monte Carlo coincide com a probabilidade analítica

No cenário-base, a variância do agregado estrutural implica desvio-padrão:

[
sqrt{V_pi}=1,048568.
]

Como (	heta=-1):

[
P(S=1)=Phileft(-rac{1}{1,048568}ight)=0,170122.
]

A probabilidade exata é, portanto, **17,01%**. A realização de 10.000 replicações produziu 17,29%, com IC95% de Wilson de aproximadamente 16,56% a 18,04%.

A diferença de 0,28 ponto percentual entre valor analítico e realização Monte Carlo é compatível com erro amostral da simulação. O resultado central de formação da semente não depende, portanto, do valor particular obtido pela seed 20260816.

### 4.3 Sessenta agentes nominais equivalem a pouco mais de três fontes efetivas

| Grupo | N | sigma | Sinais corretos | Peso estacionário total |
|---|---:|---:|---:|---:|
| Executivo | 1 | 1,90 | 69,75% | 52,65% |
| Gestores | 5 | 1,55 | 73,79% | 42,99% |
| Seniores | 12 | 1,20 | 79,76% | 3,18% |
| Demais | 42 | 0,90 | 86,80% | 1,18% |

O executivo concentra 52,65% da influência estacionária. Os cinco gestores acrescentam 42,99%. Os 54 agentes restantes compartilham 4,36%. O tamanho efetivo de fontes é 3,1408.

Esse resultado é consistente com a literatura de aprendizagem em redes, que relaciona concentração de poder social à perda de eficiência informacional. A contribuição do presente exercício está em mostrar essa concentração dentro da parametrização hierárquica do modelo e conectá-la diretamente a (V_pi) e à probabilidade de reversão.

### 4.4 O erro do executivo é quase necessário, mas não suficiente

O executivo recebeu sinal incorreto em 30,25% das replicações. Condicionada a esse evento:

[
P(S=1|E_{exec}=1)=55,83%.
]

Quando o executivo estava correto:

[
P(S=1|E_{exec}=0)=0,57%.
]

Entre as sementes incorretas, 97,69% ocorreram com executivo errado. Mesmo assim, o erro do executivo não é suficiente. Em aproximadamente 44% das replicações em que ele estava errado, os demais sinais ainda preservaram a direção correta do agregado.

Quando o executivo estava errado, a incidência de semente incorreta cresceu com o número de gestores também errados:

| Gestores errados | N | P(S dado executivo errado) |
|---:|---:|---:|
| 0 | 677 | 34,42% |
| 1 | 1.200 | 51,25% |
| 2 | 820 | 67,07% |
| 3 | 279 | 87,10% |
| 4 | 44 | 97,73% |
| 5 | 5 | 100,00% |

A localização estrutural do erro importa mais do que a contagem simples de sinais incorretos.

### 4.5 A decomposição do agregado localiza a reversão

Nas replicações sem semente errada, a contribuição média do executivo para (pi'e) foi -0,818. Nas replicações com semente errada, foi +0,890. A contribuição média dos gestores permaneceu negativa, passando de -0,453 para -0,291.

Seniores e demais agentes apresentaram contribuições médias pequenas ao agregado ponderado apesar de representarem 54 dos 60 integrantes. Isso não significa que sejam pouco informados. No cenário de estresse, eles são, em média, mais precisos. Sua capacidade de alterar (Z), contudo, é reduzida pela distribuição de (pi).

### 4.6 A estática comparativa é confirmada pela solução exata

| kappa | P(S) Monte Carlo | P(S) exata | n_eff | Peso executivo | Peso Top 6 |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,0000% | <0,0001% | 59,19 | 1,43% | 10,24% |
| 1 | 0,0000% | 0,00003% | 45,58 | 4,66% | 25,15% |
| 2 | 0,3900% | 0,2926% | 19,96 | 12,47% | 49,65% |
| 3 | 4,6100% | 4,4831% | 8,75 | 24,97% | 73,88% |
| 4 | 11,3300% | 11,2750% | 4,84 | 39,17% | 88,79% |
| 5 | 17,2900% | 17,0122% | 3,14 | 52,65% | 95,64% |

A realização Monte Carlo acompanha de perto a curva analítica. O aumento de (kappa) desloca peso para agentes hierarquicamente superiores e mais ruidosos no cenário de estresse, elevando (V_pi) e, consequentemente, a probabilidade de reversão.

A leitura correta não é que (n_{eff}) determine sozinho o risco. A relação depende simultaneamente de concentração e precisão. O parâmetro relevante para a probabilidade exata é (sum_i pi_i^2sigma_i^2).

### 4.7 O resultado não depende da rede publicada

Nas 500 novas redes Watts-Strogatz, mantendo os papéis hierárquicos fixos, a probabilidade exata média de semente incorreta foi **17,46%**, com mediana de 17,42%. O intervalo empírico entre os percentis 2,5 e 97,5 foi **16,93% a 18,43%**.

O (n_{eff}) médio foi 3,04, e o peso médio do executivo foi 53,90%.

A probabilidade exata da rede publicada, 17,01%, encontra-se próxima da região central da distribuição de novas redes. Assim, o resultado não depende materialmente de uma realização excepcional do grafo Watts-Strogatz.

### 4.8 O resultado também não depende de uma posição excepcionalmente influente do executivo

Nas 1.000 permutações dos papéis hierárquicos na rede publicada, a probabilidade exata média de reversão foi **22,35%**, com mediana de 22,37% e intervalo estrutural de **20,62% a 23,90%**.

O (n_{eff}) médio caiu para 2,07 e o peso médio do executivo subiu para 68,65%.

A probabilidade da configuração publicada, 17,01%, ficou abaixo de todas as 1.000 posições sorteadas. Esse resultado não prova que seja a configuração globalmente menos adversa, mas mostra que o achado-base não deriva de o executivo ter sido colocado por acaso em um nó excepcionalmente poderoso. Se algo, a posição publicada é conservadora em relação à amostra de alocações testadas.

### 4.9 A semente incorreta possui intensidade

| Quintil | Margem média | P(H dado S), beta=0,70 c=0,90 | P(H dado S), beta=0,75 c=0,95 |
|---:|---:|---:|---:|
| Q1 | 0,076 | 0,00% | 55,49% |
| Q2 | 0,233 | 19,94% | 100,00% |
| Q3 | 0,435 | 93,91% | 100,00% |
| Q4 | 0,717 | 100,00% | 100,00% |
| Q5 | 1,316 | 100,00% | 100,00% |

No cenário ((0,70,0,90)), nenhuma semente do primeiro quintil produz manada, enquanto 93,91% das sementes do terceiro quintil o fazem. Nos dois quintis superiores, a ocorrência é total. No cenário mais extremo, mais da metade das sementes mais fracas já ultrapassa o corte de manada, e todos os quintis seguintes chegam a 100%.

A AUC da margem é elevada no cenário-base, mas é tratada apenas como diagnóstico suplementar, porque a margem e o desfecho são produzidos pelo mesmo sistema. O resultado substantivo é ordinal: sementes estruturalmente mais deslocadas exigem menos amplificação adicional para produzir consenso incorreto.

### 4.10 O resultado não é sensível ao corte de 80%

| Corte tau | P(H dado S), beta=0,70 c=0,90 | P(H dado S), beta=0,75 c=0,95 |
|---:|---:|---:|
| 70% | 65,47% | 91,90% |
| 75% | 63,68% | 91,50% |
| 80% | 62,75% | 91,09% |
| 85% | 61,19% | 90,75% |
| 90% | 59,63% | 90,17% |

A interpretação permanece estável quando o corte de manada varia de 70% a 90%. O parâmetro de 80% é, portanto, uma convenção operacional do estudo-base, não o único ponto em que o mecanismo aparece.

## 5 Discussão

A versão 0.2 altera a interpretação do resultado em dois aspectos.

Primeiro, a concentração de influência não deve ser apresentada como mecanismo inédito. A literatura de redes já demonstra que agentes ou grupos excessivamente influentes podem impedir aprendizagem eficiente e que o efeito da influência depende da relação entre poder social e acurácia. O modelo estudado é consistente com essa tradição. Sua contribuição está em transportar essa lógica para um arcabouço organizacional que separa posição hierárquica, precisão do sinal, manifestação pública e amplificação posterior.

Segundo, a formação da semente não precisa ser tratada apenas como resultado de Monte Carlo. Sob a distribuição gaussiana já assumida, sua probabilidade é fechada e depende de (V_pi). Isso clarifica o mecanismo: concentração é problemática quando eleva a variância do agregado ao concentrar peso em sinais mais ruidosos. Se maior influência estiver associada a maior precisão, o mesmo canal pode reduzir (V_pi) e melhorar a decisão.

Essa conclusão aproxima o modelo dos resultados de Tian, Wang e Bullo (2023), segundo os quais a distribuição de poder social em relação à precisão dos indivíduos é central para determinar se influência melhora ou piora a sabedoria coletiva. O elemento adicional aqui é a decomposição entre formação da semente e sua amplificação posterior sob custo de discordância.

Para auditoria, o resultado deve ser lido como hipótese de mecanismo. Cardinaels et al. (2025), Ying, Patel e Dela Cruz (2023) e Gold, Kadous e Leiby (2024) fornecem evidência de que hierarquia, consenso sênior, pressão social e status podem afetar julgamentos. Nenhum desses estudos, porém, estima (W), (pi), (kappa) ou (m) do presente modelo. A ponte empírica ainda precisa ser construída.

## 6 Implicações para auditoria e governança

A implicação mais defensável é distinguir participação formal de independência informacional.

Uma revisão com vários participantes pode oferecer menos diversidade efetiva do que sua contagem nominal sugere se as posições forem formadas após exposição à conclusão de um membro dominante. Isso não implica que supervisão, senioridade ou expertise sejam indesejáveis. Em muitos contextos, dar maior peso a agentes mais informados é racional e pode melhorar a acurácia.

O risco aparece quando status e peso decisório não acompanham qualidade informacional.

O modelo sugere hipóteses experimentais, não controles já validados: registro individual antes da discussão, manifestação simultânea, ocultação temporária da posição do superior, separação explícita entre status e expertise e revisão por fonte informacional independente. A eficácia dessas intervenções deve ser estimada em participantes humanos.

## 7 Limitações

A principal limitação continua sendo a validade externa. Não há participantes humanos e os parâmetros não foram calibrados em organizações.

A solução analítica depende da hipótese de sinais gaussianos independentes. Correlação entre erros individuais, caudas pesadas ou outras distribuições podem alterar (P(S)). O resultado fechado deve ser interpretado dentro desse processo gerador.

As 500 novas redes mantêm a mesma família Watts-Strogatz e os mesmos parâmetros. Elas testam dependência da realização específica da rede, não robustez a todas as topologias possíveis.

As 1.000 permutações de papéis preservam a associação estilizada entre hierarquia e ruído e não representam um modelo empírico de alocação de cargos. Seu objetivo é exclusivamente testar dependência da posição nodal.

A análise é pós-hoc. A distinção entre resultados do estudo-base e extensões do segundo artigo precisa permanecer explícita.

A relação entre intensidade da semente e manada é interna ao mesmo sistema matemático. AUC elevada ou regressões classificatórias não devem ser tratadas como desempenho preditivo externo.

Por fim, a separação deste artigo em relação ao primeiro é conceitual, não amostral. Ambos compartilham a realização-base. O presente trabalho deve ser citado como análise secundária do mesmo experimento, com pergunta e estatísticas próprias.

## 8 Agenda de validação

O próximo estágio relevante é experimental.

Participantes podem receber sinais privados de precisão conhecida e registrar uma avaliação antes de observar a posição de outros membros. Em seguida, podem ser manipulados o status da fonte, a existência de consenso prévio, a ordem de manifestação e o custo percebido de discordância.

Esse desenho permitiria observar separadamente:

[
	ext{evidência privada} ightarrow 	ext{crença individual} ightarrow 	ext{manifestação pública}.
]

Uma segunda etapa pode estimar parâmetros aproximados de influência e conformidade. Uma terceira pode testar equipes profissionais em ambientes controlados. Somente depois disso medidas como (n_{eff}), (V_pi) ou (m) deveriam ser consideradas para diagnóstico aplicado.

## 9 Conclusão

O segundo artigo não demonstra uma nova lei geral sobre centralização. A literatura de aprendizagem em redes já estabeleceu que poder social concentrado pode prejudicar a sabedoria coletiva e que o efeito depende de quem recebe esse poder.

A contribuição específica deste estudo é mostrar como esse mecanismo aparece no arcabouço hierárquico do estudo-base e separar três componentes: maioria nominal, formação da semente estrutural e amplificação posterior.

Na realização publicada, todas as 10.000 maiorias nominais estavam corretas, mas 17,29% dos agregados estruturais estavam errados. A solução gaussiana fechada produz probabilidade de 17,01%, confirmando que o resultado não é artefato da seed Monte Carlo. Em 500 novas redes, a probabilidade média permaneceu próxima, 17,46%. A randomização dos papéis na rede publicada mostrou que a configuração original é menos adversa que as 1.000 alocações sorteadas.

O mecanismo central é expresso por:

[
V_pi=sum_i pi_i^2sigma_i^2.
]

A concentração importa porque altera quanto ruído informacional entra no agregado. Hierarquia, por si só, não determina o sinal do efeito.

A intensidade da semente acrescenta uma segunda camada. Sementes incorretas não são equivalentes: quanto mais distante o agregado se encontra da fronteira correta, menor a pressão adicional necessária para transformá-lo em consenso incorreto.

A implicação para auditoria permanece uma proposição de pesquisa: contar revisores ou manifestações não é suficiente para inferir independência informacional. A questão empiricamente relevante é quantas fontes independentes de evidência tiveram capacidade real de alterar a conclusão.

## Referências

BANERJEE, A. V. A simple model of herd behavior. *The Quarterly Journal of Economics*, v. 107, n. 3, p. 797-817, 1992.

BECKER, J.; BRACKBILL, D.; CENTOLA, D. Network dynamics of social influence in the wisdom of crowds. *Proceedings of the National Academy of Sciences*, v. 114, n. 26, p. E5070-E5076, 2017. DOI: 10.1073/pnas.1615978114.

BIKHCHANDANI, S.; HIRSHLEIFER, D.; WELCH, I. A theory of fads, fashion, custom, and cultural change as informational cascades. *Journal of Political Economy*, v. 100, n. 5, p. 992-1026, 1992. DOI: 10.1086/261849.

CARDINAELS, E.; DARMAWAN, V.; REUSEN, E.; STOUTHUYSEN, K. The influence of team consensus and inclusive climate on junior auditors' conformity and risk assessment sharing. *Journal of Accounting and Public Policy*, v. 52, art. 107334, 2025. DOI: 10.1016/j.jaccpubpol.2025.107334.

DEGROOT, M. H. Reaching a consensus. *Journal of the American Statistical Association*, v. 69, n. 345, p. 118-121, 1974. DOI: 10.1080/01621459.1974.10480137.

GOLD, A.; KADOUS, K.; LEIBY, J. Does status equal substance? The effects of specialist social status on auditor assessments of complex estimates. *The Accounting Review*, v. 99, n. 5, p. 197-222, 2024. DOI: 10.2308/TAR-2021-0298.

GOLUB, B.; JACKSON, M. O. Naive learning in social networks and the wisdom of crowds. *American Economic Journal: Microeconomics*, v. 2, n. 1, p. 112-149, 2010. DOI: 10.1257/mic.2.1.112.

LORENZ, J.; RAUHUT, H.; SCHWEITZER, F.; HELBING, D. How social influence can undermine the wisdom of crowd effect. *Proceedings of the National Academy of Sciences*, v. 108, n. 22, p. 9020-9025, 2011. DOI: 10.1073/pnas.1008636108.

MORRISON, E. W.; MILLIKEN, F. J. Organizational silence: a barrier to change and development in a pluralistic world. *Academy of Management Review*, v. 25, n. 4, p. 706-725, 2000. DOI: 10.5465/AMR.2000.3707697.

NASCIMENTO, J. C. do. *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*. Zenodo, 2026. DOI: 10.5281/zenodo.21985858.

TIAN, Y.; WANG, L.; BULLO, F. How social influence affects the wisdom of crowds in influence networks. *SIAM Journal on Control and Optimization*, v. 61, n. 4, p. 2334-2357, 2023. DOI: 10.1137/22M1492751.

YING, S. X.; PATEL, C.; DELA CRUZ, A. L. The influence of partners' known preferences on auditors' sceptical judgements: the moderating role of perceived social influence pressure. *Accounting & Finance*, v. 63, n. 3, p. 3193-3215, 2023. DOI: 10.1111/acfi.13030.

## Disponibilidade de dados e código

A realização de referência está depositada no Zenodo, DOI 10.5281/zenodo.21985858. O código-base encontra-se em research/dinamica-manada-organizacional. As rotinas complementares ficam em second-paper/.

A versão 0.2 acrescenta:
- probabilidade analítica da semente incorreta;
- 500 redes adicionais para robustez estrutural;
- 1.000 permutações de papéis hierárquicos;
- sensibilidade do critério de manada entre 70% e 90%;
- controles automáticos de reprodução.

## Declaração de escopo

As probabilidades reportadas descrevem o comportamento interno do modelo sob condições especificadas. Não devem ser interpretadas como prevalência estimada de conformidade, silêncio, efeito manada ou erro de julgamento em equipes reais. A análise é secundária, exploratória e não pré-registrada.
