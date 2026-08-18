# Estrutura do Artigo v5 — consolidação após janeiro–abril de 2025

> Este documento substitui a narrativa de contribuição/originalidade da v4 e preserva suas definições, fórmulas, política de dados e testes de robustez quando não houver alteração explícita abaixo.

## Título provisório preferido

**Dependência Estrutural de Fornecedores nas Compras Públicas: Concentração da Carteira, Exposição em Rede e Vulnerabilidade a Choques Coletivos**

### Título em inglês

**Structural Supplier Dependency in Public Procurement: Portfolio Concentration, Network Exposure, and Vulnerability to Collective Shocks**

## Pergunta de pesquisa revisada

Em que medida medidas locais de concentração da carteira capturam — ou deixam de capturar — a exposição dos compradores públicos a fornecedores globalmente centrais, e quão persistente e sistemicamente relevante é essa exposição quando conjuntos centrais de fornecedores são removidos da rede de contratação?

## Tese central da v5

A dependência de fornecedores deve ser tratada como fenômeno multidimensional. A evidência acumulada até abril de 2025 sustenta quatro componentes empiricamente distinguíveis:

1. **concentração monetária local**, medida pela distribuição do valor contratado na carteira do comprador;
2. **recorrência contratual**, medida pela distribuição e repetição dos instrumentos;
3. **exposição estrutural global**, medida pelo peso que fornecedores centrais na rede nacional/observada têm dentro de cada carteira;
4. **vulnerabilidade sistêmica coletiva**, medida pela perda de carteira gerada pela remoção conjunta de fornecedores globalmente centrais.

A contribuição não depende de um índice composto proprietário. O artigo demonstra que um comprador pode apresentar concentração local relativamente baixa e, simultaneamente, elevada exposição a fornecedores centrais — a **exposição estrutural oculta**. Também demonstra que a vulnerabilidade sistêmica observada decorre muito mais de combinações de fornecedores centrais do que de um único “superfornecedor”.

# 1. Reposicionamento de originalidade

## 1.1 O que não deve ser reivindicado como novidade isolada

A literatura recente tornou inadequado apresentar como contribuição inédita, por si só:

- o uso de redes bipartidas comprador–fornecedor em compras públicas;
- o uso de degree/weighted degree para monitoramento de fornecedores;
- a comparação entre participação por contagem e concentração por valor;
- a combinação genérica entre concentração e persistência de relações comprador–fornecedor;
- a ideia geral de comparar ataques direcionados e remoções aleatórias em redes.

Fountoukidis, Antoniou e Varsakelis (2023) já usam redes de autoridades e fornecedores, degree ponderado/não ponderado e entropia para monitorar condições competitivas em compras públicas. Em 2026, Fountoukidis et al. propõem um Institutional Closure Index que combina concentração com vínculos persistentes e embeddedness. Também em 2026, Fountoukidis propõe Value–Count Divergence para a discrepância entre rankings por contagem e por valor.

## 1.2 Contribuição original mais defensável

A originalidade será formulada como a **integração operacional e empiricamente testada** de quatro elementos que, em conjunto, não aparecem de forma equivalente nos trabalhos identificados:

1. **exposição do comprador à centralidade global dos seus fornecedores**, ponderada pela participação monetária de cada fornecedor na carteira;
2. **identificação de exposição estrutural oculta**, isto é, compradores que não parecem altamente concentrados localmente, mas dependem relativamente de fornecedores globalmente centrais;
3. **choques coletivos direcionados com perda definida no nível do comprador**, comparando conjuntos de fornecedores ordenados por Strength global a distribuições aleatórias empíricas e contabilizando compradores que perderiam ≥25%, ≥50% ou ≥75% da carteira observada;
4. **validação longitudinal do sinal**, com correlação de rankings, retenção no quartil superior, transição de quadrantes e efeito de composição decorrente da entrada de novos compradores na amostra elegível.

O contexto empírico brasileiro, a escala PNCP municipal, a integração incremental com SICONFI e o protocolo integralmente reproduzível reforçam a contribuição aplicada, mas não devem ser usados como substituto de contribuição conceitual.

# 2. Resultado empírico que passa a organizar o artigo

## 2.1 Concentração local e frequência são diferentes

Até abril, na especificação elegível 3/5:

- PortfolioHHI mediano: **0,2470**;
- PortfolioHHI normalizado mediano: **0,1532**;
- CountHHI mediano: **0,0909**;
- em **97,83%** dos compradores o HHI monetário supera o HHI por frequência.

A divergência entre valor e frequência é empiricamente forte, mas, diante da literatura de 2026, será tratada como **resultado de caracterização e controle**, não como principal reivindicação de originalidade.

## 2.2 Exposição estrutural não é redundante com HHI

A correlação entre HHI normalizado e exposição por Strength global é moderada (`ρ ≈ 0,382` em janeiro–abril). Há **135 compradores (13,33%)** classificados como baixa concentração relativa e alta exposição estrutural na especificação 3/5.

Esse resultado sustenta a proposição de que medidas puramente locais não esgotam a dependência da carteira.

## 2.3 Choques coletivos são muito mais relevantes que choques individuais

Com perda mínima de 50% da carteira:

- remoção direcionada dos top 1% por Strength: **8,59%** dos compradores severamente afetados, contra **0,33%** em média nas remoções aleatórias;
- top 5%: **33,86%** contra **1,80%**;
- top 10%: **47,58%** contra **4,14%**.

A análise de fornecedor único mostrou anteriormente que apenas poucos fornecedores conseguem afetar severamente vários compradores de forma isolada. Logo, a narrativa deve ser de **fragilidade por conjuntos centrais**, não de dependência do sistema em um único nó.

## 2.4 O sinal é longitudinalmente persistente

Entre março e abril, nos 780 compradores comuns:

- exposição Strength: `ρ = 0,932`;
- retenção no quartil superior de Strength: **85,13%**;
- quadrante completo estável: **82,56%**;
- retenção da exposição estrutural oculta: **80,0%**.

Esses resultados permitem interpretar a exposição estrutural como **sinal de screening persistente**, sem tratá-la como atributo permanente.

## 2.5 A evolução agregada sofre efeito de composição

A mediana agregada do HHI sobe levemente de março para abril (`0,2451 → 0,2470`), mas nos 780 compradores comuns cai para `0,2130` em abril. Os **233 novos elegíveis** apresentam HHI mediano `0,3371`, apenas 6 fornecedores e 7 instrumentos na mediana.

Portanto, estatísticas de janelas acumuladas devem separar:

- evolução dentro de compradores persistentes;
- efeito da entrada de compradores recém-elegíveis.

Esse diagnóstico passa a ser parte explícita da seção de robustez temporal.

# 3. Modelos associativos — papel na v5

Os modelos servem para verificar se os padrões estruturais permanecem após controles fiscais, territoriais e de tamanho da carteira. Não constituem o núcleo causal do artigo.

Na janela janeiro–abril (`n = 1.002`, 600 clusters municipais):

- VIFs: **1,15–1,50**;
- população permanece positivamente associada ao HHI normalizado no OLS e no fractional logit;
- número de fornecedores permanece negativamente associado ao HHI normalizado, com magnitude semelhante à de janeiro–março;
- despesa per capita permanece sem associação robusta;
- recorrência converge aproximadamente a zero nos modelos de HHI;
- recorrência permanece positiva e estatisticamente associada à exposição Strength.

O contraste final é substantivamente útil: **recorrência não é um determinante estável da concentração local, mas está associada à exposição a fornecedores centrais**, reforçando a separação entre as dimensões.

# 4. Estrutura recomendada da seção de literatura

## 4.1 Concentração e diversidade da base de fornecedores

HHI, CR1/CR4, número efetivo, concentração da carteira e sourcing concentration.

## 4.2 Redes de compras públicas

Redes bipartidas autoridade–fornecedor, degree, weighted degree, entropy, comunidades e monitoring.

Referência obrigatória:

- Fountoukidis, I. G.; Antoniou, I. E.; Varsakelis, N. C. (2023). *Competitive conditions in the public procurement markets: an investigation with network analysis*. Journal of Industrial and Business Economics, 50, 347–368. DOI: 10.1007/s40812-022-00251-z.

## 4.3 Persistência relacional e institutional closure

Referência recente a confrontar diretamente:

- Fountoukidis, I. G.; Dafli, E.; Antoniou, I.; Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN, posted 18 May 2026, abstract 6765160.

Diferenciação: o nosso artigo não propõe fechamento institucional como composição concentração×persistência; investiga quanto da carteira de cada comprador está exposta a fornecedores globalmente centrais e testa a vulnerabilidade sob choques coletivos.

## 4.4 Valor versus contagem

Referência recente a confrontar:

- Fountoukidis, I. G. (2026). *Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement*. SSRN, posted 24 June 2026, abstract 6897598.

Diferenciação: PortfolioHHI versus CountHHI será tratado como diagnóstico de heterogeneidade da carteira, não como contribuição exclusiva; o passo adicional é relacionar a carteira à posição global dos fornecedores e à perda simulada do comprador.

## 4.5 Robustez, ataques direcionados e risco sistêmico

Revisar literatura de robustez de redes e supply-chain systemic risk, deixando explícito que a simulação é mecânica: não mede probabilidade de default, substituibilidade técnica ou interrupção real.

## 4.6 Auditoria e screening

Conectar a exposição estrutural a priorização baseada em risco: o indicador seleciona casos para análise aprofundada; não constitui achado, prova de irregularidade ou classificação reputacional.

# 5. Metodologia que permanece congelada

Preservar da v4, salvo teste adicional documentado:

- comprador = CNPJ institucional;
- fornecedores PJ na base pública identificada;
- `valorInicial` principal;
- PortfolioHHI bruto + normalizado;
- CountHHI bruto + normalizado;
- CR1, CR4 e Neff;
- rede global antes da elegibilidade;
- Strength global como ranking principal e Degree como complementar;
- exposição do comprador ponderada pelo share monetário;
- critério operacional atual 3 fornecedores / 5 instrumentos com sensibilidade 5/10, 5/20 e 10/20;
- choques 1%, 5% e 10%; perdas 25%, 50% e 75%; 1.000 sorteios aleatórios;
- criticidade de fornecedor único como diagnóstico complementar;
- SICONFI somente para vínculo territorial único;
- OLS com efeitos de região e erro agrupado por município;
- fractional logit como robustez;
- nenhuma interpretação causal sem estratégia específica.

# 6. Nova organização dos resultados

1. **Formação da amostra e qualidade dos dados**.
2. **Concentração monetária local**: HHI, HHI norm, CR1, CR4, Neff.
3. **Valor versus frequência**: resultado de caracterização, explicitamente relacionado à literatura VCD.
4. **Estrutura da rede global**: Degree, Strength, alcance e caudas.
5. **Exposição estrutural do comprador** e matriz concentração×exposição.
6. **Exposição estrutural oculta**.
7. **Criticidade de fornecedor único**.
8. **Vulnerabilidade sistêmica coletiva**: ataques direcionados versus aleatórios.
9. **Persistência longitudinal do sinal**.
10. **Efeito de composição das coortes acumuladas**.
11. **Integração fiscal e modelos associativos**.
12. **Robustezes**.

# 7. Frase de contribuição sugerida para a introdução

> Este estudo mostra que a dependência de fornecedores em compras públicas não se reduz à concentração observada dentro de cada carteira. Ao combinar participações monetárias locais com a posição global dos fornecedores em uma rede comprador–fornecedor, identificamos compradores cuja concentração aparente é baixa, mas cuja exposição a fornecedores estruturalmente centrais é elevada. Demonstramos ainda que a vulnerabilidade sistêmica emerge principalmente da remoção conjunta de conjuntos centrais de fornecedores, é muito superior a contrafactuais aleatórios e apresenta persistência significativa ao longo de janelas sucessivas de contratação.

# 8. Limitações que devem aparecer de forma proeminente

- coortes de publicação acumuladas não equivalem ao ano fechado;
- a entrada de novos elegíveis altera estatísticas agregadas;
- `valorInicial` não equivale a execução financeira;
- centralidade não mede substituibilidade técnica, risco de crédito ou capacidade produtiva;
- remoções simuladas não modelam adaptação, substituição ou renegociação;
- Strength é dependente da escala monetária observada e deve ser acompanhado de Degree e testes de sensibilidade;
- cobertura do PNCP e publicações tardias podem alterar a rede final;
- modelos fiscais são associativos;
- rótulos de risco são relativos à amostra e à janela temporal;
- nenhuma métrica implica fraude, favorecimento ou irregularidade.

# 9. Próximo congelamento metodológico

Não alterar novamente a especificação principal durante a expansão mensal de 2025. Os próximos meses devem ser usados para testar estabilidade e convergência dos resultados. Alterações metodológicas somente entram se forem motivadas por falha de qualidade, inconsistência matemática ou evidência bibliográfica substantiva e deverão ser executadas como robustez separada.

# Referências de posicionamento incorporadas na v5

- Fountoukidis, I. G., Antoniou, I. E., & Varsakelis, N. C. (2023). Competitive conditions in the public procurement markets: an investigation with network analysis. *Journal of Industrial and Business Economics*, 50, 347–368. https://doi.org/10.1007/s40812-022-00251-z
- Fountoukidis, I. G., Dafli, E., Antoniou, I., & Varsakelis, N. (2026). Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data. SSRN, abstract 6765160. Posted 18 May 2026.
- Fountoukidis, I. G. (2026). Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement. SSRN, abstract 6897598. Posted 24 June 2026.
