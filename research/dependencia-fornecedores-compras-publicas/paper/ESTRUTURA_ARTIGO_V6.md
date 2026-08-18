# Estrutura do Artigo v6 — consolidação após janeiro–maio de 2025

> Esta versão substitui a narrativa empírica da v5 e preserva suas definições, fórmulas, política de dados, referências de posicionamento e especificação metodológica quando não houver alteração explícita. A metodologia principal continua congelada durante a expansão mensal de 2025.

## Título provisório preferido

**Dependência Estrutural de Fornecedores nas Compras Públicas: Concentração da Carteira, Exposição em Rede e Vulnerabilidade a Choques Coletivos**

### Título em inglês

**Structural Supplier Dependency in Public Procurement: Portfolio Concentration, Network Exposure, and Vulnerability to Collective Shocks**

## Pergunta de pesquisa

Em que medida medidas locais de concentração da carteira capturam — ou deixam de capturar — a exposição dos compradores públicos a fornecedores globalmente centrais, e quão persistente e sistemicamente relevante é essa exposição quando conjuntos centrais de fornecedores são removidos da rede de contratação?

## Tese empírica da v6

A evidência acumulada até maio reforça que dependência de fornecedores é um fenômeno multidimensional. Quatro dimensões permanecem empiricamente distintas:

1. **concentração monetária local**, observada na distribuição do valor contratado entre fornecedores de cada comprador;
2. **recorrência contratual**, observada na repetição e distribuição dos instrumentos;
3. **exposição estrutural global**, definida pelo peso que fornecedores centrais na rede global têm na carteira de cada comprador;
4. **vulnerabilidade sistêmica coletiva**, definida pela perda de carteira associada à retirada conjunta de fornecedores globalmente centrais.

A v6 acrescenta uma quinta mensagem metodológica: **estatísticas de coortes acumuladas devem separar mudança dentro dos compradores persistentes de mudança de composição da amostra elegível**. Em abril e maio, novos elegíveis entram mais concentrados que os incumbentes, enquanto a concentração cai dentro dos compradores comuns.

# 1. Contribuição e posicionamento

## 1.1 O que permanece fora da reivindicação de originalidade isolada

Não apresentar como novidade, por si só:

- rede bipartida comprador–fornecedor;
- HHI, Degree ou Strength em compras públicas;
- divergência entre valor e contagem de contratos;
- combinação genérica de concentração com persistência relacional;
- comparação genérica entre ataques direcionados e remoções aleatórias.

A literatura identificada na v5, especialmente Fountoukidis, Antoniou e Varsakelis (2023) e os trabalhos de 2026 sobre institutional closure e value–count divergence, deve ser enfrentada diretamente.

## 1.2 Contribuição original mais defensável

A contribuição central permanece a integração, no nível da carteira do comprador, de:

1. participações monetárias locais;
2. centralidade global dos fornecedores;
3. identificação de **exposição estrutural oculta**;
4. simulação de **choques coletivos direcionados**, com perda medida no nível do comprador;
5. comparação com distribuições aleatórias empíricas;
6. validação longitudinal dos rankings e quadrantes;
7. separação explícita entre evolução longitudinal e efeito de composição das coortes acumuladas.

A originalidade não depende de um índice composto proprietário.

# 2. Evidência acumulada janeiro–maio

## 2.1 Escala da base

No acumulado janeiro–maio:

- **87.515** instrumentos PJ únicos;
- **80.820** instrumentos assinados em 2025;
- **2.197** compradores com métricas calculadas;
- **1.210** compradores elegíveis na regra principal 3 fornecedores / 5 instrumentos;
- **17.062** fornecedores na rede global.

A unidade principal continua sendo o CNPJ institucional do comprador. Município permanece dimensão territorial e chave de integração fiscal, não substituto do comprador.

## 2.2 Concentração monetária local

Na amostra elegível 3/5:

- HHI monetário mediano: **0,2420**;
- HHI monetário normalizado mediano: **0,1548**;
- número efetivo mediano de fornecedores: **4,13**;
- CR1 mediano: **0,3910**;
- CR4 mediano: **0,8206**.

A queda do HHI bruto em relação a abril não deve ser lida isoladamente. O HHI normalizado permanece próximo do nível anterior, e a análise longitudinal mostra que parte relevante da redução ocorre dentro das carteiras que já eram elegíveis.

## 2.3 Valor versus frequência

Até maio:

- CountHHI mediano: **0,0861**;
- CountHHI normalizado mediano: **0,00694**;
- Spearman HHI monetário × CountHHI: `ρ = 0,5744`;
- em **97,77%** dos compradores, o HHI monetário supera o CountHHI.

Essa divergência continua substantivamente importante, mas permanece como resultado de caracterização e robustez, não como reivindicação principal de originalidade.

## 2.4 Exposição estrutural não é redundante com HHI

A correlação entre HHI normalizado e exposição por Strength global permanece moderada (`ρ = 0,4092`). Há **153 compradores (12,64%)** no quadrante de baixa concentração relativa e alta exposição estrutural.

Portanto, concentração local e exposição estrutural compartilham informação, mas não são equivalentes.

# 3. Vulnerabilidade sistêmica coletiva

## 3.1 Resultado principal dos choques

Considerando perda mínima de 50% da carteira e ordenação por Strength global:

- remoção dos top 1% dos fornecedores: **8,26%** dos compradores severamente afetados, contra **0,33%** na média aleatória;
- top 5%: **33,47%**, contra **1,80%** aleatória;
- top 10%: **48,93%**, contra **4,14%** aleatória.

A diferença permanece muito superior à distribuição de remoções aleatórias, reforçando que a vulnerabilidade observada está concentrada em **conjuntos de fornecedores estruturalmente centrais**.

## 3.2 Interpretação correta

A simulação é um contrafactual estrutural mecânico. Ela não mede:

- probabilidade de falha;
- risco de crédito;
- capacidade produtiva;
- substituibilidade técnica;
- velocidade de recomposição da carteira;
- adaptação contratual ou renegociação.

Consequentemente, o termo “vulnerabilidade sistêmica” deve ser qualificado como vulnerabilidade da **rede observada sob remoção mecânica de nós**, e não previsão de interrupção real.

# 4. Persistência longitudinal do screening

## 4.1 Março → abril

Nos 780 compradores comuns:

- Strength: `ρ ≈ 0,932`;
- retenção no quartil superior: **85,1%**;
- retenção da exposição oculta: aproximadamente **80%**;
- quadrante estável: aproximadamente **82,6%**.

## 4.2 Abril → maio

Nos **1.013 compradores comuns**:

- Strength: `ρ = 0,9378`;
- retenção no quartil superior de Strength: **86,22%**;
- exposição oculta persistente: **112 de 135** compradores de abril, retenção de **82,96%**;
- Jaccard da exposição oculta: **0,7134**;
- quadrante completo estável: **85,88%**.

A persistência aumenta ligeiramente entre as duas transições mensais examinadas. Isso sustenta o uso dos indicadores como **sinais de triagem dinâmica**, não como atributos permanentes.

# 5. Efeito de composição das coortes acumuladas

## 5.1 Março → abril

A mediana agregada do HHI sobe de `0,2451` para `0,2470`, mas entre os compradores comuns cai. Os **233 novos elegíveis** entram com HHI mediano `0,3371`, seis fornecedores e sete instrumentos na mediana.

Logo, a alta agregada decorre de composição, e não de aumento da concentração dentro dos incumbentes.

## 5.2 Abril → maio

A mediana agregada cai de `0,2470` para `0,2420`. Nos mesmos 1.013 compradores, porém, o HHI mediano passa de `0,2470` para **0,2219**.

Os **197 novos elegíveis** entram mais concentrados:

- HHI mediano: **0,3218**;
- HHI normalizado: **0,1848**;
- seis fornecedores e sete instrumentos na mediana.

A diferença de HHI entre novos e compradores comuns em maio é aproximadamente **+0,0999**. Portanto, o efeito de composição atua para elevar a concentração agregada; a queda observada ocorre **apesar** disso, porque os compradores persistentes diversificam suas carteiras.

## 5.3 Regra de apresentação

Todas as tabelas temporais do artigo deverão distinguir:

- estatística transversal da amostra elegível em cada janela;
- mudança na subamostra comum;
- perfil dos entrantes;
- eventuais saídas da elegibilidade.

Não interpretar trajetória da mediana agregada como trajetória típica de um comprador sem essa decomposição.

# 6. Integração fiscal e modelos associativos

## 6.1 Cobertura SICONFI até maio

- **1.209** compradores com vínculo municipal único;
- **1.199** com despesa empenhada disponível;
- cobertura: **99,17%**;
- **674** municípios com total de despesa empenhada;
- cache consolidada sem duplicidades.

A coleta incremental reutiliza 602 municípios previamente bem-sucedidos e acrescenta somente 74 novos municípios em maio.

## 6.2 Especificação pré-fixada

Para o HHI normalizado:

`HHI_norm_b = β0 + β1 ln(Pop_b) + β2 ln(DespesaPC_b) + β3 ln(NFornec_b) + β4 ln(InstrPorFornec_b) + Região + ε_b`

- OLS;
- erros-padrão agrupados por município;
- efeitos fixos de macrorregião;
- fractional logit como robustez funcional.

Nenhuma covariável foi selecionada após observar maio.

## 6.3 Resultado janeiro–maio

Na amostra de **1.199 compradores e 674 clusters municipais**:

### OLS — HHI normalizado

- população: `β = 0,02184`, positiva e significativa;
- despesa per capita: `β = 0,01553`, não significativa;
- número de fornecedores: `β = -0,06649`, negativo e significativo;
- recorrência: `β = 0,00637`, não significativa.

### Fractional logit

- população: `β = 0,11753`, positiva e significativa;
- despesa per capita: não significativa;
- número de fornecedores: `β = -0,39323`, negativo e significativo;
- recorrência: praticamente nula e não significativa.

VIFs entre **1,15 e 1,51** não indicam multicolinearidade relevante.

# 7. Convergência dos coeficientes

A v6 passa a documentar explicitamente a trajetória da especificação pré-fixada, sem impor limiar pós-hoc de estabilidade.

## 7.1 População → HHI normalizado

OLS, janeiro–fevereiro até janeiro–maio:

`0,01546 → 0,01679 → 0,02053 → 0,02184`

- zero mudanças de sinal;
- significativa nas 4 de 4 janelas.

Fractional logit:

`0,08257 → 0,09111 → 0,11005 → 0,11753`

- positiva e significativa nas 4 de 4 janelas.

## 7.2 Número de fornecedores → HHI normalizado

OLS:

`-0,07955 → -0,07271 → -0,06673 → -0,06649`

- negativa nas 4 de 4 janelas;
- significativa nas 4 de 4;
- magnitude maio/abril = **0,996**, praticamente invariável.

Fractional logit:

`-0,45832 → -0,43001 → -0,39633 → -0,39323`

- negativa e significativa nas quatro janelas;
- magnitude maio/abril = **0,992**.

Essa é a relação com maior convergência quantitativa na especificação atual.

## 7.3 Despesa per capita → HHI

- muda de sinal ao longo das janelas;
- significativa em **0 de 4** janelas no OLS;
- também não mostra robustez no fractional logit.

Não deve receber interpretação substantiva central.

## 7.4 Recorrência → HHI e exposição

Para HHI local, recorrência é não significativa em **4 de 4 janelas** no OLS e converge para aproximadamente zero no fractional logit.

Para exposição Strength, em contraste:

`0,08288 → 0,06213 → 0,04647`

- positiva nas 3 de 3 janelas;
- significativa nas 3 de 3.

O número de fornecedores também permanece positivamente associado à exposição Strength nas três janelas.

Esse contraste passa a ser um dos resultados organizadores do artigo: **diversificação local reduz concentração, mas não elimina — e pode coexistir com — exposição a fornecedores globalmente centrais**.

# 8. Organização recomendada dos resultados

1. Formação da amostra, política de dados e qualidade.
2. Concentração monetária local: HHI bruto/normalizado, CR1, CR4, Neff.
3. Valor versus frequência: CountHHI e divergência como caracterização.
4. Estrutura da rede global: Degree, Strength, distribuição e alcance.
5. Exposição estrutural do comprador.
6. Matriz concentração × exposição e exposição estrutural oculta.
7. Criticidade de fornecedor único.
8. Vulnerabilidade coletiva: ataques direcionados versus aleatórios.
9. Persistência longitudinal dos rankings e quadrantes.
10. Efeito de composição das coortes acumuladas.
11. Integração fiscal e modelos associativos.
12. Convergência dos coeficientes ao ampliar a janela.
13. Robustezes e limitações.

# 9. Frase de contribuição revisada

> Este estudo mostra que a dependência de fornecedores em compras públicas não se reduz à concentração observada dentro de cada carteira. Ao combinar participações monetárias locais com a posição global dos fornecedores em uma rede comprador–fornecedor, identificamos compradores cuja concentração aparente é baixa, mas cuja exposição a fornecedores estruturalmente centrais é elevada. A vulnerabilidade sob remoções direcionadas é muito superior à observada em contrafactuais aleatórios e os sinais de exposição permanecem fortemente correlacionados entre janelas sucessivas. A análise longitudinal mostra ainda que a diversificação das carteiras reduz a concentração local sem necessariamente reduzir a exposição à centralidade global, evidenciando dimensões distintas de dependência.

# 10. Limitações prioritárias

- janeiro–maio ainda é uma coorte parcial de publicações, não o ano fechado;
- publicações tardias podem alterar a rede final;
- a composição da amostra elegível muda com a janela;
- `valorInicial` não equivale a execução financeira;
- HHI de carteira não é medida antitruste de poder de mercado;
- Strength não mede substituibilidade, solvência ou capacidade produtiva;
- simulações de remoção não modelam adaptação, substituição ou renegociação;
- integração SICONFI é restrita a compradores com vínculo territorial não ambíguo;
- modelos fiscais são associativos;
- significância recorrente não cria identificação causal;
- classificações de risco são relativas à amostra e à janela;
- nenhuma métrica implica fraude, favorecimento ou irregularidade.

# 11. Congelamento metodológico para junho em diante

A especificação principal permanece congelada. Junho e meses posteriores servem para avaliar:

- persistência dos rankings;
- estabilidade dos quadrantes;
- evolução do efeito de composição;
- convergência ou reversão dos coeficientes pré-fixados;
- estabilidade dos choques direcionados versus aleatórios;
- alteração da cobertura e qualidade da base.

Qualquer alteração metodológica deverá ser motivada por problema de qualidade, inconsistência matemática ou evidência bibliográfica substantiva e implementada como robustez separada.

# Referências de posicionamento preservadas da v5

- Fountoukidis, I. G., Antoniou, I. E., & Varsakelis, N. C. (2023). *Competitive conditions in the public procurement markets: an investigation with network analysis*. Journal of Industrial and Business Economics, 50, 347–368. DOI: 10.1007/s40812-022-00251-z.
- Fountoukidis, I. G., Dafli, E., Antoniou, I., & Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160.
- Fountoukidis, I. G. (2026). *Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement*. SSRN 6897598.
