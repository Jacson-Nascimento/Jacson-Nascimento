# Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração de Carteira, Exposição em Rede e Vulnerabilidade a Choques Coletivos

**Structural Supplier Dependency in Municipal Public Procurement: Portfolio Concentration, Network Exposure, and Vulnerability to Collective Shocks**

**Jacson Cruz do Nascimento**

> **Versão de trabalho v0.2.** O recorte empírico principal utiliza instrumentos assinados em 2025 e observados nas publicações do Portal Nacional de Contratações Públicas entre 1º de janeiro e 30 de junho de 2025. A captura posterior do segundo semestre e de publicações tardias de 2026 compõe uma extensão anual separada e não é usada para alterar os resultados semestrais reportados nesta versão.

## Resumo

A dependência de fornecedores em compras públicas costuma ser aproximada pela concentração do valor contratado dentro da carteira de cada comprador. Essa perspectiva, embora informativa, não revela se os fornecedores relevantes localmente também ocupam posições centrais no sistema de contratação nem como a carteira responderia à indisponibilidade simultânea de fornecedores estruturalmente importantes. Este estudo integra o **Portal Nacional de Contratações Públicas (PNCP)**, o **Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro (SICONFI)** e informações territoriais do **Instituto Brasileiro de Geografia e Estatística (IBGE)** para examinar compradores públicos municipais observados no primeiro semestre de 2025. A base pública minimizada reúne 105.582 instrumentos de fornecedores **pessoa jurídica (PJ)**, dos quais 98.438 foram assinados em 2025. Foram calculadas métricas para 2.349 compradores institucionais, e a amostra principal inclui 1.347 compradores com pelo menos três fornecedores e cinco instrumentos. A concentração monetária é mensurada pelo **Índice Herfindahl-Hirschman (HHI)**, complementado por uma versão normalizada, razões de concentração e número efetivo de fornecedores. O HHI monetário mediano é 0,2365, o HHI normalizado é 0,1563 e o número efetivo mediano é 4,23. Em 98,14% dos compradores, a concentração por valor supera a concentração por frequência. A correlação de Spearman entre HHI normalizado e exposição ao Strength global dos fornecedores é 0,4081, e 13,14% dos compradores combinam concentração local relativa não extrema com elevada exposição estrutural. Simulações com 1.000 contrafactuais aleatórios mostram que a remoção direcionada dos 10% de fornecedores de maior Strength deixa 48,26% dos compradores com perda de pelo menos metade da carteira observada, contra 4,08% sob remoções aleatórias de mesmo tamanho. O ranking de exposição é temporalmente persistente: entre maio e junho, 90,76% dos compradores no quartil superior permanecem nesse grupo. Na integração PNCP-SICONFI, a cobertura de despesa empenhada alcança 99,18% da amostra com vínculo municipal único. Modelos associativos indicam relação negativa e persistente entre amplitude da base de fornecedores e HHI normalizado, enquanto recorrência contratual se mostra mais consistentemente associada à exposição estrutural do que à concentração local. O artigo contribui ao combinar, em uma única arquitetura reproduzível, concentração local, centralidade global, choques coletivos, persistência longitudinal e controles fiscais. As conclusões são válidas para os compradores observados e não implicam fraude, falha de continuidade ou causalidade.

**Palavras-chave:** compras públicas; concentração de fornecedores; análise de redes; vulnerabilidade estrutural; governança; auditoria baseada em dados.

## Abstract

Supplier dependency in public procurement is often approximated by the concentration of contracted value within each buyer's portfolio. Although informative, this local view does not reveal whether locally important suppliers are also central to the broader procurement system or how portfolios would respond to the simultaneous unavailability of structurally important suppliers. This study integrates Brazil's **National Public Procurement Portal (PNCP)**, the **Brazilian Public Sector Accounting and Fiscal Information System (SICONFI)**, and territorial information from the **Brazilian Institute of Geography and Statistics (IBGE)** to examine municipal public buyers observed during the first half of 2025. The minimized public dataset contains 105,582 instruments involving corporate suppliers, 98,438 of which were signed in 2025. Metrics are computed for 2,349 institutional buyers, and the main analytical sample contains 1,347 buyers with at least three suppliers and five instruments. Monetary concentration is measured with the **Herfindahl-Hirschman Index (HHI)**, complemented by a normalized form, concentration ratios, and the effective number of suppliers. Median monetary HHI is 0.2365, normalized HHI is 0.1563, and the median effective number of suppliers is 4.23. For 98.14% of buyers, value concentration exceeds frequency concentration. Spearman correlation between normalized HHI and exposure to suppliers' global Strength is 0.4081, while 13.14% of buyers combine non-extreme relative local concentration with high structural exposure. Simulations with 1,000 random counterfactuals show that targeted removal of the top 10% of suppliers by global Strength leaves 48.26% of buyers exposed to losses of at least half of their observed portfolio, compared with 4.08% under equally sized random removals. Exposure rankings are persistent over time: from May to June, 90.76% of buyers in the top quartile remain there. In the PNCP-SICONFI integration, committed-expenditure coverage reaches 99.18% of the sample with an unambiguous municipal link. Associative models show a persistent negative relationship between supplier-base breadth and normalized HHI, whereas contractual recurrence is more consistently related to structural exposure than to local concentration. The article contributes by combining local concentration, global centrality, collective shocks, longitudinal persistence, and fiscal controls in a reproducible empirical architecture. Results apply to observed buyers and do not imply fraud, actual service disruption, or causality.

**Keywords:** public procurement; supplier concentration; network analysis; structural vulnerability; governance; data-driven audit.

# 1. Introdução

A contratação pública conecta organizações governamentais a mercados privados de bens, serviços e obras. Essa conexão não é apenas transacional: ela produz relações repetidas, assimetrias de escala, dependências técnicas e exposições que podem permanecer invisíveis quando a análise se limita ao número nominal de fornecedores ou ao número de contratos. A teoria da organização industrial mostra que estruturas concentradas alteram o ambiente competitivo e a distribuição de poder econômico (Tirole, 1988). A teoria de incentivos aplicada à contratação pública acrescenta que desenho contratual, informação e incentivos condicionam o desempenho das relações entre comprador e fornecedor (Laffont & Tirole, 1993). Em compras públicas, tais questões são particularmente relevantes porque preço, qualidade, risco, concorrência e continuidade precisam ser tratados simultaneamente (Dimitri, Piga & Spagnolo, 2006).

A literatura empírica demonstra que desempenho de compras públicas depende de muito mais que o preço de adjudicação. Bandiera, Prat e Valletti (2009) mostram que diferenças persistentes no custo de aquisição podem decorrer de ineficiências passivas; Decarolis (2014) documenta o trade-off entre preço de adjudicação e desempenho ex post; Lewis-Faupel et al. (2016) mostram que contratação eletrônica pode modificar entrada, qualidade e origem dos vencedores; Coviello, Guglielmo e Spagnolo (2018) demonstram que discricionariedade pode alterar a repetição de vencedores sem necessariamente deteriorar desempenho; e Bosio et al. (2022) enfatizam a interação entre regras formais, prática administrativa e capacidade estatal. Esse conjunto de evidências sugere que relações comprador-fornecedor devem ser analisadas como estruturas econômicas e institucionais, não apenas como registros administrativos isolados.

A perspectiva de redes amplia essa leitura. Em redes econômicas, a posição de um agente pode importar tanto quanto seus atributos locais (Jackson, 2008; Newman, 2010). A centralidade mede diferentes formas de importância estrutural (Freeman, 1978), enquanto a literatura de robustez de redes demonstra que sistemas podem reagir de modo muito distinto a falhas aleatórias e ataques direcionados a nós centrais (Albert, Jeong & Barabási, 2000). Aplicações recentes em compras públicas mostram que estruturas de contratação podem apresentar elevada concentração, hierarquia e influência de firmas centrais (Pliatsidis, 2024; Sturm et al., 2025). Assim, a existência de muitos fornecedores para um comprador não garante, por si só, independência estrutural.

Este artigo investiga essa distinção nas compras públicas municipais brasileiras observadas no PNCP. A pergunta de pesquisa é: **em que medida a concentração local da carteira captura - ou deixa de capturar - a exposição dos compradores públicos a fornecedores globalmente centrais, e quão persistente e relevante é essa exposição quando conjuntos centrais de fornecedores são removidos da rede observada?**

A contribuição do estudo é deliberadamente incremental e multidimensional. Não se reivindica originalidade no uso isolado do HHI, em redes bipartidas, em centralidade, em recorrência ou em simulações de remoção. O avanço proposto está na articulação de cinco elementos: (i) concentração monetária da carteira institucional; (ii) contraste entre concentração por valor e por frequência; (iii) exposição de cada comprador à centralidade global de seus fornecedores; (iv) choques coletivos direcionados comparados a contrafactuais aleatórios; e (v) persistência longitudinal do sinal conforme a coorte observada se expande. Essa arquitetura é integrada a controles fiscais municipais e implementada em um pipeline reproduzível, com checkpoints, minimização de dados pessoais e verificações explícitas de qualidade.

O recorte é semestral e intermediário. São analisados instrumentos assinados em 2025 e observados nas publicações entre 1º de janeiro e 30 de junho de 2025. Como publicações tardias são relevantes, os resultados não constituem fechamento definitivo de todas as contratações assinadas no período. O segundo semestre e as publicações tardias capturadas em 2026 serão usados em uma extensão anual, permitindo avaliar convergência, representatividade territorial e sensibilidade ao truncamento temporal.

# 2. Fundamentação teórica e literatura

## 2.1 Concentração, organização industrial e dependência de fornecedores

O HHI é um índice clássico de concentração baseado na soma dos quadrados das participações dos agentes. Em organização industrial, índices de concentração sintetizam a desigualdade das participações econômicas e ajudam a caracterizar estruturas competitivas, embora não substituam a definição econômica do mercado relevante nem a análise de contestabilidade, barreiras à entrada e conduta estratégica (Tirole, 1988). Neste estudo, o HHI não é interpretado como medida de concentração de mercado. Ele mede **concentração da carteira de fornecedores do comprador**, isto é, o grau em que o valor contratado por uma organização pública está distribuído de forma desigual entre seus fornecedores observados.

Essa distinção é metodologicamente central. A base do PNCP oferece categorias administrativas amplas e, nos testes realizados, campos de classificação de item não apresentaram granularidade suficiente para sustentar de modo uniforme uma definição de mercado relevante. Tratar todo o conjunto de "Compras" como um mercado seria excessivamente forte. Por isso, o objeto é a dependência financeira do comprador em sua carteira, e não poder de mercado do fornecedor.

A teoria econômica da contratação também recomenda cautela em interpretações simples. Laffont e Tirole (1993) mostram que incentivos, informação privada e desenho de mecanismos moldam relações contratuais. Dimitri, Piga e Spagnolo (2006) enfatizam que procurement é atividade dinâmica e repetida, na qual decisões de curto prazo podem afetar relações de longo prazo, risco e estrutura da base de fornecedores. Esse ponto é diretamente relevante para a recorrência: repetição de relações pode refletir eficiência, especialização, custos de troca ou fechamento institucional, dependendo do contexto.

## 2.2 Evidência empírica mainstream em compras públicas

Cinco contribuições de periódicos de ampla circulação acadêmica delimitam o espaço empírico do artigo. Bandiera, Prat e Valletti (2009), no *American Economic Review*, distinguem desperdício ativo e passivo e mostram heterogeneidade persistente entre compradores públicos. Decarolis (2014), no *American Economic Journal: Applied Economics*, demonstra que regras de adjudicação podem gerar trade-offs entre economia inicial e desempenho posterior. Lewis-Faupel et al. (2016), no *American Economic Journal: Economic Policy*, mostram que contratação eletrônica altera entrada e qualidade dos fornecedores, inclusive ampliando a presença de vencedores de fora da região. Coviello, Guglielmo e Spagnolo (2018), em *Management Science*, encontram que maior discricionariedade pode aumentar vitórias repetidas sem necessariamente piorar resultados observados. Bosio et al. (2022), no *American Economic Review*, mostram que legislação, prática e capacidade do setor público interagem na determinação de resultados de procurement.

Esses trabalhos não estudam exatamente a exposição estrutural definida aqui, mas estabelecem três premissas: a identidade e repetição dos fornecedores importam; regras e capacidade institucional afetam a configuração das relações; e a análise precisa distinguir estrutura formal de resultados econômicos. O presente artigo usa essas premissas para formular uma medida de dependência que não se reduz ao preço ou à frequência de adjudicações.

## 2.3 Redes econômicas, centralidade e robustez

A representação comprador-fornecedor como rede bipartida é natural: compradores e fornecedores formam dois conjuntos de nós, ligados por instrumentos contratuais ponderados por valor. Jackson (2008) e Newman (2010) fornecem a base conceitual para redes sociais e econômicas, incluindo redes ponderadas e bipartidas. Freeman (1978) sistematiza noções de centralidade; neste estudo, duas medidas operacionais são especialmente úteis: **grau (Degree)**, o número de compradores distintos atendidos por um fornecedor, e **força (Strength)**, a soma do valor de suas relações na rede.

A literatura de robustez justifica comparar remoções aleatórias e direcionadas. Albert, Jeong e Barabási (2000) mostram que redes heterogêneas podem ser robustas a falhas aleatórias, mas vulneráveis a ataques direcionados aos nós mais conectados. O paralelismo aqui é estritamente estrutural: a remoção de um fornecedor no experimento não equivale a falência, sanção ou interrupção real. A simulação pergunta quanto do valor observado da carteira estaria conectado ao conjunto removido, mantendo a rede estática.

No domínio de compras públicas, Pliatsidis (2024) aplica teoria de redes à concentração de contratação na Grécia, reforçando que distribuição de graus e relações entre autoridades e operadores econômicos contém informação sobre concentração. Sturm et al. (2025) mostram, em dados portugueses de larga escala, que firmas estruturalmente influentes ocupam posições relevantes em hierarquias de procurement. Trabalhos brasileiros em redes de co-participação também demonstram a utilidade de métodos relacionais para caracterizar licitações municipais. O artigo, portanto, não se apresenta como primeira aplicação de redes à contratação pública; sua contribuição está em como as medidas são integradas no nível da carteira institucional e testadas dinamicamente.

## 2.4 Lacuna e contribuição específica

A lacuna explorada é a diferença entre duas perguntas que indicadores tradicionais misturam: **"quão concentrada é a minha carteira?"** e **"quão sistemicamente centrais são os fornecedores dos quais minha carteira depende?"**. Dois compradores podem apresentar HHI semelhante, mas um contratar fornecedores periféricos e outro direcionar grande parte do valor a fornecedores que atendem muitos compradores ou concentram valor no sistema. O segundo comprador pode ser mais exposto a choques que atingem conjuntos centrais, mesmo sem apresentar concentração local excepcional.

A contribuição analítica é, assim, um diagnóstico multidimensional com interpretação conservadora. A combinação entre HHI normalizado e exposição ao Strength global identifica um quadrante denominado **exposição estrutural oculta**: compradores cuja concentração relativa não está no quartil superior, mas cuja exposição a fornecedores globalmente centrais está. Esse rótulo é apenas mecanismo de triagem; não constitui conclusão normativa nem evidência de irregularidade.

# 3. Contexto institucional, dados e construção da amostra

## 3.1 Portal Nacional de Contratações Públicas

O PNCP é o sítio eletrônico oficial destinado à divulgação centralizada dos atos exigidos pela Lei nº 14.133/2021. Os dados abertos são acessíveis por **interface de programação de aplicações (API)** e podem ser consultados sem cadastro. A captura deste estudo utiliza o serviço de contratos e empenhos com força de contrato por data de publicação.

A chave primária do instrumento é `numeroControlePNCP`. A contratação de origem é preservada, mas não usada para deduplicação simples, pois uma mesma contratação pode gerar múltiplos instrumentos e fornecedores distintos. O comprador é identificado pelo **Cadastro Nacional da Pessoa Jurídica (CNPJ)** do órgão ou entidade do instrumento. Essa decisão é superior à simples agregação por município da unidade executora, pois evita fundir instituições juridicamente distintas e permite separar compras compartilhadas ou instrumentos cuja contratação de origem pertence a outro CNPJ.

A base pública identificada é limitada a fornecedores PJ. Registros de **pessoa física (PF)** e pessoa estrangeira são mantidos em diagnósticos agregados e em cópia privada para robustez, evitando republicação desnecessária de identificadores pessoais. A decisão é de governança de dados, não exclusão substantiva silenciosa.

## 3.2 Recorte temporal e atraso de publicação

A coleta é organizada pela data de publicação, mas a análise econômica principal mantém instrumentos com data de assinatura em 2025 e `valorInicial > 0`. Assim, um instrumento publicado em junho, mas assinado em exercício anterior, não entra no agregado econômico de 2025. O atraso de publicação é calculado como a diferença entre data de publicação e data de assinatura.

A distribuição do atraso tem cauda longa, justificando a separação entre janela de captura e exercício econômico. Casos de lag negativo foram preservados e testados em sensibilidade; sua exclusão não altera materialmente os resultados. A extensão anual continuará capturando publicações posteriores referentes a contratos assinados em 2025.

## 3.3 Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro e Instituto Brasileiro de Geografia e Estatística

Os controles fiscais provêm do SICONFI, especialmente da **Declaração das Contas Anuais (DCA)** referente ao exercício de 2025. O vínculo territorial utiliza o código municipal do IBGE. População e despesa empenhada permitem construir medidas de escala, como despesa empenhada per capita. Nos modelos, compradores são mantidos quando o vínculo municipal é único e a informação fiscal está disponível.

Na amostra semestral, 1.346 compradores elegíveis apresentam vínculo municipal único e 1.335 possuem despesa empenhada, correspondendo a cobertura fiscal de 99,18% da amostra elegível com vínculo territorial não ambíguo. Esses dados não transformam o desenho em painel causal; funcionam como controles observacionais externos à estrutura da carteira.

## 3.4 Amostra e presença territorial

A base pública acumulada janeiro-junho reúne 105.582 instrumentos PJ únicos, 98.438 assinados em 2025. Há métricas para 2.349 compradores institucionais. A amostra analítica principal contém 1.347 compradores com pelo menos três fornecedores e cinco instrumentos. Cortes mais estritos - 5/10, 5/20 e 10/20 - são usados em robustez.

A presença territorial não é probabilística. Diagnósticos posteriores mostram forte heterogeneidade entre unidades federativas na continuidade observacional. Portanto, o artigo evita frases como "os municípios brasileiros apresentam" e prefere "os compradores municipais observados no PNCP". Ausência de um município em um mês não é interpretada como falha de reporte, pois pode refletir ausência real de instrumentos publicados. A extensão anual e a captura tardia serão usadas para avaliar se a presença observacional se amplia suficientemente para análises comparativas mais ambiciosas.

# 4. Estratégia empírica

## 4.1 Concentração monetária da carteira

Para cada comprador `b` e fornecedor `s`, o valor agregado da relação é:

`V_bs = Σ_k V_k`,

onde `V_k` é o valor inicial positivo do instrumento `k`. A participação monetária do fornecedor é:

`q_bs = V_bs / Σ_s V_bs`.

O HHI da carteira é:

`HHI_b = Σ_s q_bs²`.

Também são calculadas a **razão de concentração do maior fornecedor (CR1)**, a **razão de concentração dos quatro maiores fornecedores (CR4)** e o número efetivo de fornecedores:

`N_eff,b = 1 / HHI_b`.

Como o limite inferior do HHI depende do número de fornecedores, emprega-se ainda:

`HHI_norm,b = (HHI_b - 1/N_b) / (1 - 1/N_b)`, para `N_b > 1`.

## 4.2 Concentração por frequência

Substituindo participações monetárias por participações no número de instrumentos, obtém-se um HHI por frequência. A comparação entre HHI monetário e HHI por frequência mede a diferença entre diversificação formal das contratações e diversificação econômica do valor. Não se presume que um deles seja "correto" e o outro "errado"; eles respondem a dimensões diferentes.

## 4.3 Rede global e centralidade dos fornecedores

A rede `G=(B,S,E)` é bipartida: `B` contém compradores, `S` fornecedores e `E` relações comprador-fornecedor. O peso de uma relação é `V_bs`. Para cada fornecedor são calculados:

- **Degree:** número de compradores distintos conectados ao fornecedor;
- **Strength:** soma do valor agregado das relações do fornecedor;
- **Reach:** proporção de compradores da rede conectados ao fornecedor.

A ordenação principal de vulnerabilidade usa Strength global. Degree permanece como medida complementar porque testes de compras compartilhadas mostram maior sensibilidade dessa métrica à arquitetura institucional da contratação.

## 4.4 Exposição estrutural do comprador

O percentil de Strength global de cada fornecedor, `PStrength_s`, é combinado com a participação monetária local:

`ExposureStrength_b = Σ_s q_bs PStrength_s`.

A medida aumenta quando grande parte da carteira do comprador está alocada em fornecedores centrais na rede global. HHI e ExposureStrength são conceitualmente diferentes: o primeiro mede desigualdade interna; o segundo mede exposição a posição sistêmica.

A exposição estrutural oculta é definida, de forma relativa, como HHI normalizado abaixo do quartil superior e ExposureStrength acima do quartil superior da amostra elegível. O corte por quartis é uma regra de triagem, não um limiar normativo de risco.

## 4.5 Simulações de choque coletivo

Para um conjunto removido `R` de fornecedores:

`Loss_b(R) = Σ_{s∈R} q_bs`.

São simuladas remoções de 1%, 5% e 10% dos fornecedores globais. O cenário direcionado remove fornecedores em ordem decrescente de Strength; o contrafactual executa 1.000 remoções aleatórias de mesmo tamanho, com semente fixa. Um comprador é classificado como severamente exposto quando `Loss_b(R) >= 0,50`. A comparação não estima probabilidade de falha; mede sensibilidade mecânica da carteira à retirada de um conjunto de nós.

## 4.6 Persistência e efeito de composição

As janelas acumuladas mensais permitem testar se o sinal de exposição é estável ou apenas artefato de uma fotografia. Entre janelas consecutivas calculam-se correlação de Spearman dos rankings, retenção no quartil superior e transição nos quadrantes concentração-exposição. Compradores comuns são analisados separadamente de novos elegíveis, evitando confundir mudança individual com mudança de composição.

## 4.7 Modelos associativos PNCP-SICONFI

A especificação principal é estimada por **Mínimos Quadrados Ordinários (MQO)** com erros-padrão agrupados por município e efeitos de macrorregião:

`HHI_norm,b = β0 + β1 ln(Pop_b) + β2 ln(DespesaPC_b) + β3 ln(NFornec_b) + β4 ln(InstrPorFornec_b) + Região + ε_b`.

Como o desfecho é limitado, um logit fracionário é usado como robustez funcional. Um segundo conjunto de modelos usa ExposureStrength como variável dependente. Antes da estimação, o **fator de inflação da variância (VIF, do inglês variance inflation factor)** é monitorado. Após reparametrização para população, despesa per capita, número de fornecedores e instrumentos por fornecedor, os VIFs permanecem aproximadamente entre 1,14 e 1,50.

Todos os coeficientes são interpretados como associações condicionais. O desenho não identifica efeitos causais.

# 5. Resultados

## 5.1 Concentração local e divergência valor-frequência

Na amostra principal, o HHI monetário mediano é 0,2365 e o HHI normalizado mediano é 0,1563. O número efetivo mediano é 4,23 fornecedores. O CR1 mediano é 38,37% e o CR4 mediano é 80,37%. Em contraste, o HHI por frequência mediano é 0,0816 e sua versão normalizada é aproximadamente 0,00682.

Em 98,14% dos compradores elegíveis, o HHI monetário supera o HHI por frequência. O resultado mostra que grande número de instrumentos não implica distribuição equilibrada do valor. A mediana de número efetivo sugere que, em termos monetários, a carteira típica se comporta como se tivesse pouco mais de quatro fornecedores de igual peso, mesmo quando o número nominal de fornecedores é muito maior.

A evolução das janelas acumuladas mostra relativa estabilidade. Entre janeiro e junho, o HHI mediano oscila entre 0,237 e 0,247, enquanto o HHI normalizado cresce de aproximadamente 0,146 para 0,156. A interpretação do nível deve considerar o crescimento da amostra e o efeito mecânico do número de fornecedores; por isso o artigo apresenta as duas versões e testa cortes de elegibilidade mais restritos.

## 5.2 Exposição estrutural e informação adicional da rede

A correlação de Spearman entre HHI normalizado e ExposureStrength é 0,4081. A associação positiva indica que concentração e exposição não são independentes, mas a magnitude está longe de redundância. Entre 1.347 compradores, 177 - 13,14% - encontram-se no quadrante de exposição estrutural oculta.

Esse resultado é a primeira evidência direta da contribuição da perspectiva de rede: um comprador pode não estar no quartil superior de concentração local e, ainda assim, alocar parcela relevante de sua carteira em fornecedores que concentram valor em múltiplas relações do sistema. Para auditoria e governança, esse quadrante é candidato natural a triagem adicional sobre substituibilidade, contingência e planejamento da demanda.

## 5.3 Choques coletivos direcionados

A diferença entre remoção direcionada e aleatória é substancial. Considerando perda de pelo menos 50% da carteira, a retirada do 1% de fornecedores de maior Strength deixa 8,91% dos compradores severamente expostos, contra 0,32% em média nas remoções aleatórias. Com 5% removidos, os valores são 34,15% e 1,79%. Com 10%, 48,26% e 4,08%.

O padrão é coerente com a ideia geral de vulnerabilidade a ataques direcionados em redes heterogêneas (Albert, Jeong & Barabási, 2000), mas a interpretação econômica é mais restrita. A simulação não pressupõe que esses fornecedores falhem simultaneamente nem que não existam substitutos. Ela demonstra que o valor contratado está topologicamente organizado de modo que conjuntos relativamente pequenos de fornecedores centrais atravessam muitas carteiras.

Análises de criticidade individual mostram que o efeito não é dominado por um único nó. Poucos fornecedores, isoladamente, fariam vários compradores perderem metade da carteira. A vulnerabilidade emerge sobretudo da **remoção conjunta de um conjunto central**, reforçando o uso da expressão "vulnerabilidade estrutural coletiva".

## 5.4 Persistência temporal

A exposição estrutural é altamente persistente nas janelas observadas. Entre maio e junho, 1.210 compradores são comuns às duas amostras elegíveis. A correlação de Spearman do ranking de ExposureStrength é 0,9570; a correlação de Degree é 0,9319. Entre os compradores no quartil superior de Strength em maio, 90,76% permanecem no quartil superior em junho. A retenção da exposição estrutural oculta é 86,27%, e 88,68% permanecem no mesmo quadrante completo.

Esse resultado fortalece a interpretação das métricas como sinal de triagem. Um indicador instável mudaria radicalmente com a simples adição de um mês. Aqui, a estrutura individual apresenta elevada persistência mesmo com entrada de novos instrumentos e fornecedores. Ainda assim, o sinal não deve ser transformado em rótulo permanente: a rede é dinâmica e a captura ainda é incompleta.

## 5.5 Efeito de composição dos novos elegíveis

A mediana transversal pode enganar quando a amostra cresce. Entre maio e junho, a amostra elegível aumenta de 1.210 para 1.347 compradores. Os 137 novos elegíveis entram mais concentrados, com HHI mediano de 0,3606, enquanto os compradores comuns apresentam 0,2233 em junho. Dentro dos compradores comuns, a variação mediana do HHI é -0,00828.

Assim, parte da trajetória agregada é efeito de composição: compradores entram no critério 3/5 quando suas carteiras ainda são pequenas. A análise longitudinal separa esse fenômeno de mudanças efetivas dentro do mesmo comprador. Essa decomposição é importante para estudos futuros com dados acumulados ou painéis desbalanceados de procurement.

## 5.6 Integração fiscal e modelos associativos

A amostra fiscal contém 1.335 compradores com dados válidos, distribuídos em 725 clusters municipais. Os VIFs permanecem entre 1,14 e 1,50, não indicando multicolinearidade relevante na especificação reparametrizada.

No modelo MQO para HHI normalizado, log população apresenta coeficiente 0,02482 (`p<0,001`), log despesa per capita 0,02610 (`p=0,178`), log número de fornecedores -0,06754 (`p<0,001`) e log instrumentos por fornecedor 0,02752 (`p=0,033`). O logit fracionário preserva o sinal positivo de população e o sinal negativo do número de fornecedores, mas a recorrência não é significativa (`β=0,12177; p=0,123`). Ao acompanhar cinco janelas, recorrência é significativa para HHI em apenas uma no MQO e em nenhuma no logit fracionário; portanto, sua associação com concentração local é classificada como frágil.

O contraste aparece em ExposureStrength: população (`β=0,01303`), número de fornecedores (`β=0,02846`) e recorrência (`β=0,04687`) são positivos e estatisticamente significativos (`p<0,001`), enquanto despesa per capita não é significativa. A associação de recorrência com exposição estrutural permanece positiva e significativa nas quatro janelas comparáveis.

O resultado é substantivamente importante: **ampliar a base de fornecedores está associado a menor concentração local, mas carteiras maiores e mais recorrentes podem continuar mais expostas a fornecedores globalmente centrais**. A dependência, portanto, não se resume a quantos fornecedores existem.

# 6. Robustez e verificações de qualidade

A primeira robustez varia o critério de elegibilidade. As conclusões qualitativas sobre divergência valor-frequência, exposição oculta e correlação entre HHI normalizado e ExposureStrength persistem nos cortes 5/10, 5/20 e 10/20. O nível absoluto do HHI diminui quando se exigem carteiras maiores, o que confirma a necessidade de reportar HHI normalizado e evitar um único valor como estimativa universal de concentração.

A segunda robustez examina tipos de instrumento. Empenhos representam parcela material do número de linhas, mas fração pequena do valor observado; sua exclusão praticamente não altera o HHI monetário nem o choque por Strength. Uma especificação conservadora que colapsa cada combinação contratação-comprador-fornecedor ao maior instrumento também preserva os resultados principais, reduzindo preocupação com multiplicidade econômica.

A terceira robustez substitui `valorInicial` por `valorGlobal`. Na ampla maioria dos instrumentos com ambos os valores positivos, as duas grandezas coincidem ou são muito próximas; as métricas agregadas permanecem semelhantes. O `valorInicial` é mantido por maior estabilidade de interpretação e o `valorGlobal` funciona como sensibilidade.

A quarta robustez exclui lags de publicação negativos. O impacto é desprezível. Esses registros permanecem sinalizados como inconsistências temporais para auditoria do dado, mas não dirigem os resultados.

A quinta robustez considera compras compartilhadas. Excluir relações cuja contratação de origem pertence a outro CNPJ afeta mais o Degree do que o Strength. Isso motivou a escolha de Strength global como ranking principal dos choques e de Degree como medida complementar.

Finalmente, o pipeline possui verificações de unicidade de `numeroControlePNCP`, janela de publicação, hashes dos arquivos mensais, minimização da base pública e persistência imediata de checkpoints. Esses controles não substituem a qualidade da fonte original, mas reduzem risco de erro de engenharia e tornam o processo auditável.

# 7. Discussão

Os resultados sustentam uma leitura multidimensional da dependência de fornecedores. A primeira dimensão é **concentração local**: em que medida poucos fornecedores concentram o valor contratado pelo comprador. A segunda é **exposição estrutural**: quão centrais são, no sistema, os fornecedores aos quais a carteira está vinculada. A terceira é **vulnerabilidade coletiva**: quanto da carteira estaria diretamente associado a um conjunto removido de fornecedores centrais. A quarta é **persistência**: se o sinal continua aparecendo conforme a base se expande.

A distinção ajuda a reconciliar resultados aparentemente paradoxais. O número de fornecedores tem associação negativa com HHI, como esperado: carteiras mais amplas tendem a ser menos concentradas localmente. Entretanto, o mesmo número de fornecedores e a recorrência estão positivamente associados à exposição estrutural. Uma possível interpretação é que compradores de maior escala e complexidade diversificam a base nominal, mas continuam contratando empresas que também ocupam posições relevantes em muitas outras carteiras. O artigo não identifica o mecanismo causal dessa associação; ela pode refletir escala, especialização, capacidade técnica, padronização, compras compartilhadas ou características setoriais não observadas.

Para governança e auditoria, a implicação não é "evitar fornecedores centrais". Centralidade pode ser resultado de qualidade, escala, especialização ou eficiência. O uso adequado das métricas é priorizar perguntas adicionais: existe substituto tecnicamente viável? Há concentração de conhecimento? Existem planos de contingência? A demanda pode ser parcelada sem perda de eficiência? Compras compartilhadas aumentam ou reduzem risco operacional? A evidência quantitativa funciona como mapa de atenção, não como julgamento de conformidade.

# 8. Contribuição do estudo

A contribuição é composta por cinco elementos. Primeiro, o artigo redefine a concentração observada como **concentração da carteira institucional**, evitando confundir o HHI com concentração de mercado relevante quando a taxonomia do item não é suficientemente granular. Segundo, introduz uma ponte operacional entre dependência local e centralidade global, mensurando exposição ao Strength dos fornecedores. Terceiro, quantifica vulnerabilidade coletiva por remoções direcionadas e compara o resultado a 1.000 contrafactuais aleatórios. Quarto, acompanha a estabilidade mensal dos rankings e decompõe a mudança entre incumbentes e novos elegíveis. Quinto, integra controles fiscais municipais e explicita um pipeline reproduzível, com governança de dados e verificações de qualidade.

Em relação à literatura, o artigo não concorre com a teoria de procurement, com a literatura de eficiência de leilões ou com aplicações gerais de redes. Sua contribuição é conectar essas tradições em um diagnóstico voltado ao comprador institucional e à gestão de dependência. Esse posicionamento reduz risco de superestimação da originalidade e torna a proposição empírica mais falsificável: se a exposição de rede não acrescentasse informação ao HHI, se os choques direcionados não se distinguissem dos aleatórios ou se o ranking fosse instável, a arquitetura perderia utilidade. Os resultados semestrais indicam o contrário, mas a validação anual ainda é necessária.

# 9. Limitações

A primeira limitação é temporal. O artigo observa publicações até 30 de junho de 2025 e não todos os instrumentos assinados no semestre que possam ter sido publicados depois. A presença de caudas longas no lag de publicação implica truncamento à direita. A versão anual deverá incorporar publicações tardias em 2026 antes de qualquer afirmação de fechamento do exercício.

A segunda limitação é territorial e amostral. Os compradores observados não formam amostra probabilística dos municípios brasileiros. A intensidade de contratação, a adoção do PNCP e a cronologia de publicação variam entre entes. Portanto, as conclusões são sobre compradores municipais observados na rede, não sobre todos os municípios do país.

A terceira limitação é econômica. `valorInicial` mede valor contratual, não execução financeira, pagamento ou consumo. HHI de carteira não é HHI de mercado; não há definição uniforme de mercado relevante por produto. Centralidade não mede substituibilidade técnica, capacidade produtiva, saúde financeira ou qualidade do fornecedor.

A quarta limitação é do experimento de choque. A remoção de nós é estática e mecânica: não modela entrada de substitutos, renegociação, estoques, contratação emergencial, capacidade ociosa, cascatas de segunda ordem ou adaptação do comprador. O resultado é exposição direta da carteira, não previsão de interrupção de serviço.

A quinta limitação é econométrica. Os modelos são associativos e sujeitos a seleção, simultaneidade e variáveis omitidas. Número de fornecedores e recorrência são endógenos ao próprio processo de contratação. Efeitos de macrorregião e erros agrupados melhoram a inferência, mas não resolvem identificação causal.

A sexta limitação decorre da própria governança da base pública: fornecedores PF são excluídos da versão identificada publicada. Diagnósticos agregados sugerem que a decisão não dirige a concentração monetária principal, mas estudos sobre mercados intensivos em profissionais individuais podem exigir tratamento específico.

# 10. Agenda de pesquisas futuras

A primeira extensão é fechar 2025, incorporando agosto-dezembro e uma janela de captura tardia em 2026. Isso permitirá medir quanto os indicadores convergem e estimar a sensibilidade ao truncamento de publicação.

A segunda é construir comparação intertemporal com 2024 - e eventualmente 2023 - desde que diagnósticos de presença observacional indiquem comparabilidade adequada. Um painel mais longo permitiria estudar persistência estrutural, entrada e saída de fornecedores e transições entre quadrantes de risco.

A terceira frente é enriquecer a definição econômica do objeto. Se campos de item ou taxonomias externas permitirem classificação consistente, futuras análises poderão estimar concentração por famílias comparáveis de bens e serviços, aproximando a noção de mercado relevante sem abandonar a análise de carteira institucional.

A quarta é incorporar atributos dos fornecedores, como atividade econômica, idade, porte, localização, situação cadastral e indicadores financeiros, testando se centralidade estrutural está associada a maior capacidade de absorção de demanda ou a vulnerabilidades financeiras específicas.

A quinta é modelar substituição e cascatas. Uma simulação dinâmica poderia permitir realocação da demanda para fornecedores sobreviventes, limites de capacidade e custos de troca. Isso aproximaria a análise de continuidade operacional e permitiria distinguir exposição bruta de perda efetivamente não substituível.

A sexta é avançar na identificação causal. Mudanças regulatórias, limiares de modalidade, adoção de contratação eletrônica, compras compartilhadas ou regras de centralização podem fornecer desenhos quase-experimentais para estudar como arquitetura de procurement altera concentração e exposição estrutural.

A sétima é validar os sinais quantitativos por estudos de caso de auditoria e gestão de riscos. Amostras estratificadas de compradores nos quatro quadrantes poderiam ser submetidas a análise documental para verificar se a exposição de rede corresponde a dependência técnica, econômica ou operacional observável.

# 11. Conclusão

A evidência do primeiro semestre de 2025 mostra que dependência de fornecedores nas compras públicas municipais observadas no PNCP é um fenômeno multidimensional. Concentração monetária local, recorrência contratual e exposição estrutural global são relacionadas, mas não equivalentes. Em 98,14% dos compradores elegíveis, a concentração por valor é superior à concentração por frequência. Cerca de 13% apresentam exposição estrutural elevada sem pertencer ao quartil superior de concentração local.

A rede acrescenta informação que o HHI não contém. Choques direcionados a conjuntos de fornecedores com maior Strength produzem exposição muito superior a remoções aleatórias do mesmo tamanho: no cenário de 10%, 48,26% dos compradores perdem pelo menos metade da carteira observada, contra 4,08% no contrafactual aleatório. O sinal também é persistente ao longo do tempo, com retenção de 90,76% no quartil superior de exposição entre maio e junho.

Nos modelos associativos, amplitude da base de fornecedores se relaciona de forma robusta a menor concentração local. Recorrência, por sua vez, não apresenta associação estável com HHI, mas se relaciona consistentemente à exposição estrutural. Essa diferença reforça a tese do artigo: **diversificação nominal e independência estrutural não são sinônimos**.

Para gestão de riscos e auditoria, o resultado recomenda combinar indicadores locais com medidas de posição sistêmica e simulações de dependência coletiva. A contribuição deve ser usada como triagem orientada por dados, nunca como atalho para inferir fraude ou falha operacional. A extensão anual testará a estabilidade das conclusões com maior cobertura temporal, publicações tardias e análises adicionais de representatividade.

# Disponibilidade de dados, código e reprodutibilidade

Os dados primários são públicos e provêm do PNCP, SICONFI e IBGE. Scripts de captura, tratamento, consolidação, métricas, simulações e modelos são versionados no repositório de pesquisa. A base pública identificada contém apenas fornecedores PJ; identificadores de PF permanecem fora do repositório público. O pipeline mantém hashes, manifestos, checkpoints mensais e registros técnicos de decisões metodológicas e incidentes de qualidade.

# Referências

ALBERT, Réka; JEONG, Hawoong; BARABÁSI, Albert-László. Error and attack tolerance of complex networks. *Nature*, v. 406, p. 378-382, 2000. Identificador de Objeto Digital (DOI): 10.1038/35019019.

BANDIERA, Oriana; PRAT, Andrea; VALLETTI, Tommaso. Active and passive waste in government spending: evidence from a policy experiment. *American Economic Review*, v. 99, n. 4, p. 1278-1308, 2009. DOI: 10.1257/aer.99.4.1278.

BOSIO, Erica; DJANKOV, Simeon; GLAESER, Edward; SHLEIFER, Andrei. Public procurement in law and practice. *American Economic Review*, v. 112, n. 4, p. 1091-1117, 2022. DOI: 10.1257/aer.20200738.

COVIELLO, Decio; GUGLIELMO, Andrea; SPAGNOLO, Giancarlo. The effect of discretion on procurement performance. *Management Science*, v. 64, n. 2, p. 715-738, 2018. DOI: 10.1287/mnsc.2016.2628.

DECAROLIS, Francesco. Awarding price, contract performance, and bids screening: evidence from procurement auctions. *American Economic Journal: Applied Economics*, v. 6, n. 1, p. 108-132, 2014. DOI: 10.1257/app.6.1.108.

DIMITRI, Nicola; PIGA, Gustavo; SPAGNOLO, Giancarlo (eds.). *Handbook of Procurement*. Cambridge: Cambridge University Press, 2006. DOI: 10.1017/CBO9780511492556.

FREEMAN, Linton C. Centrality in social networks: conceptual clarification. *Social Networks*, v. 1, n. 3, p. 215-239, 1978/1979. DOI: 10.1016/0378-8733(78)90021-7.

JACKSON, Matthew O. *Social and Economic Networks*. Princeton: Princeton University Press, 2008. DOI: 10.2307/j.ctvcm4gh1.

LAFFONT, Jean-Jacques; TIROLE, Jean. *A Theory of Incentives in Procurement and Regulation*. Cambridge, Massachusetts: MIT Press, 1993.

LEWIS-FAUPEL, Sean; NEGGERS, Yusuf; OLKEN, Benjamin A.; PANDE, Rohini. Can electronic procurement improve infrastructure provision? Evidence from public works in India and Indonesia. *American Economic Journal: Economic Policy*, v. 8, n. 3, p. 258-283, 2016. DOI: 10.1257/pol.20140258.

NEWMAN, Mark E. J. *Networks: An Introduction*. Oxford: Oxford University Press, 2010. DOI: 10.1093/acprof:oso/9780199206650.001.0001.

PLIATSIDIS, Andreas Christos. Analyzing concentration in the Greek public procurement market: a network theory approach. *Journal of Industrial and Business Economics*, v. 51, p. 431-480, 2024. DOI: 10.1007/s40812-023-00291-z.

STURM, Niclas Frederic; CANDIA, Cristian; DAMÁSIO, Bruno; PINHEIRO, Flávio L. High earnings through firm influence: the role of hierarchical structures in public procurement. *EPJ Data Science*, v. 14, art. 27, 2025.

TIROLE, Jean. *The Theory of Industrial Organization*. Cambridge, Massachusetts: MIT Press, 1988.

BRASIL. Portal Nacional de Contratações Públicas. *Dados Abertos e documentação de APIs*. Brasília, Distrito Federal: Governo Federal.

BRASIL. Tesouro Nacional. *Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro: documentação da Declaração das Contas Anuais*. Brasília, Distrito Federal: Secretaria do Tesouro Nacional.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. *Códigos dos Municípios e Divisão Territorial Brasileira*. Rio de Janeiro: IBGE.
