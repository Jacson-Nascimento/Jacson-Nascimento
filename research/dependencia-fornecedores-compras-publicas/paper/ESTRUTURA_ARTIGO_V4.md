# Estrutura do Artigo v4

## Título provisório

**Dependência de Fornecedores nas Compras Públicas: Concentração da Carteira, Centralidade e Vulnerabilidade Sistêmica em Redes de Contratação**

### Título em inglês

**Supplier Dependency in Public Procurement: Portfolio Concentration, Centrality, and Systemic Vulnerability in Procurement Networks**

## Pergunta de pesquisa

Em que medida a dependência de fornecedores dos compradores públicos apresenta dimensões distintas de concentração monetária, recorrência contratual e exposição a fornecedores estruturalmente centrais, e quanto a análise de rede acrescenta às medidas locais da carteira para identificar vulnerabilidades persistentes e sistêmicas?

## Tese empírica que orienta a versão atual

A dependência de fornecedores não é adequadamente descrita por uma única medida. Os resultados acumulados até março de 2025 sustentam quatro distinções:

1. **concentração monetária local** — distribuição do valor contratado entre fornecedores de cada comprador;
2. **recorrência contratual** — distribuição da frequência de instrumentos entre fornecedores;
3. **exposição estrutural** — peso, na carteira do comprador, de fornecedores centrais na rede global;
4. **vulnerabilidade sistêmica coletiva** — perda potencial produzida pela retirada conjunta de conjuntos de fornecedores centrais.

A criticidade de um fornecedor isolado é conceitualmente distinta da vulnerabilidade sistêmica. Os testes mostram que choques individuais severos são raros em escala sistêmica, enquanto remoções direcionadas de conjuntos centrais geram efeitos muito superiores às remoções aleatórias.

## Contribuição central

O artigo propõe uma arquitetura de mensuração, e não um índice composto proprietário. A contribuição consiste em separar empiricamente:

- dependência financeira do comprador;
- recorrência da relação contratual;
- centralidade global do fornecedor;
- exposição estrutural do comprador;
- criticidade de fornecedor único;
- vulnerabilidade coletiva a choques direcionados.

Essa separação evita confundir HHI de carteira com poder de mercado, centralidade com risco de crédito e simulação estrutural com previsão de interrupção real.

## Princípios metodológicos consolidados

- comprador principal identificado pelo CNPJ institucional;
- município tratado como dimensão territorial e chave de integração fiscal, não como substituto do comprador;
- PortfolioHHI bruto acompanhado obrigatoriamente de HHI normalizado pelo piso `1/N`;
- CountHHI tratado como dimensão distinta da concentração monetária;
- Strength global adotado como ordenação principal dos choques; Degree como complemento;
- centralidades calculadas na rede global observada antes da seleção da subamostra elegível;
- ranking restrito mantido apenas como robustez;
- critérios de elegibilidade submetidos a sensibilidade 3/5, 5/10, 5/20 e 10/20;
- simulações direcionadas comparadas com 1.000 remoções aleatórias por cenário;
- `valorInicial` como variável monetária principal e `valorGlobal` como robustez;
- tipos de instrumento, empenhos, multiplicidade, compras compartilhadas e lags inconsistentes submetidos a testes específicos;
- SICONFI integrado apenas quando o vínculo comprador–município é não ambíguo;
- efeitos territoriais de macrorregião e erros-padrão agrupados por município nos modelos associativos;
- fractional logit como robustez para o HHI normalizado;
- nenhuma associação descrita como causal sem estratégia explícita de identificação;
- classificações de risco interpretadas como sinais de triagem dinâmica, não como evidência de irregularidade.

# 1. Introdução

## 1.1 Motivação

Um comprador público pode contratar muitos fornecedores e ainda depender economicamente de poucos deles. Da mesma forma, um fornecedor pode ser central na rede sem ser dominante em cada carteira individual. A contagem nominal, a distribuição do valor, a frequência contratual, a centralidade e a criticidade são objetos relacionados, mas não equivalentes.

## 1.2 Problema

Indicadores puramente locais podem omitir a posição estrutural dos fornecedores. Por outro lado, centralidade global isolada não informa quanto cada comprador efetivamente perderia diante de um choque. O problema de pesquisa exige combinar a perspectiva da carteira com a perspectiva da rede.

## 1.3 Pergunta de pesquisa

Apresentar a pergunta central e delimitar que o objeto é dependência da carteira e vulnerabilidade estrutural, não concentração antitruste de mercado.

## 1.4 Contribuições

- mensuração da dependência monetária por HHI bruto e normalizado, CR1, CR4 e número efetivo;
- separação entre concentração por valor e por frequência;
- mensuração de exposição a fornecedores centrais em rede bipartida comprador–fornecedor;
- distinção entre centralidade, criticidade individual e vulnerabilidade sistêmica coletiva;
- simulações direcionadas versus distribuição aleatória empírica;
- teste longitudinal de estabilidade dos sinais de risco;
- decomposição da mudança do HHI entre reponderação e entrada de novos fornecedores;
- integração incremental com controles fiscais do SICONFI;
- protocolo reproduzível, versionado e auditável.

## 1.5 Limites conceituais

PortfolioHHI não mede poder de mercado. Strength não mede solvência, substituibilidade técnica ou probabilidade de falha. A remoção de um fornecedor é um contrafactual estrutural mecânico. Os resultados não constituem diagnóstico de fraude, irregularidade ou risco de crédito.

# 2. Literatura

## 2.1 Dependência de fornecedores e concentração da base de suprimentos

Supplier dependency, sourcing concentration, supply-base concentration, supplier portfolio management e resiliência de suprimentos.

## 2.2 Compras públicas

Repetição de fornecedores, governança, compras compartilhadas, escala, concentração relacional e riscos de continuidade de fornecimento.

## 2.3 Redes comprador–fornecedor

Redes bipartidas, degree, strength, centralidade, robustez de redes, ataques direcionados e vulnerabilidade coletiva.

## 2.4 Critical suppliers e risco sistêmico

Distinguir fornecedor crítico local, nó central e vulnerabilidade do sistema à perda simultânea de nós centrais. A literatura deve sustentar que importância topológica e dependência econômica são dimensões complementares.

## 2.5 Auditoria e priorização baseada em risco

Indicadores quantitativos como mecanismos de screening, seleção de unidades e priorização de análises, sem equivalência automática a achado ou irregularidade.

# 3. Dados

## 3.1 PNCP

- instrumentos contratuais e empenhos;
- CNPJ do comprador institucional;
- fornecedor PJ na base pública identificada;
- valor inicial e valor global;
- datas de assinatura/publicação;
- tipo de instrumento;
- contratação de origem;
- indicador de origem externa/compra compartilhada.

## 3.2 SICONFI/DCA

- despesa empenhada;
- despesa liquidada;
- despesa paga;
- população disponível no retorno;
- integração incremental por código IBGE.

## 3.3 IBGE e dimensão territorial

UF e macrorregião; população e demais atributos somente quando necessários para validação ou extensão.

## 3.4 Receita Federal/CNPJ

Possível enriquecimento empresarial futuro, com atenção à natureza temporal dos atributos cadastrais. Não é requisito para a contribuição principal.

## 3.5 Política de dados

Base pública identificada restrita a PJ. PF/PE aparecem apenas em diagnósticos agregados. Identificadores de fornecedores PJ podem ser mantidos nos artefatos técnicos necessários à replicação e triagem, sem interpretação reputacional automática.

# 4. Construção da Amostra

## 4.1 Coleta por data de publicação

A API do PNCP é percorrida por data de publicação. As janelas são particionadas em blocos pequenos, com persistência imediata, hash SHA-256 e resumo de qualidade após cada bloco.

## 4.2 Ano econômico por data de assinatura

O painel de 2025 usa instrumentos assinados em 2025, ainda que publicados posteriormente dentro da janela de coleta.

## 4.3 Publicações tardias

A versão anual deverá incorporar janela adicional em 2026 para capturar publicações tardias de instrumentos assinados em 2025.

## 4.4 Chaves e duplicidades

`numeroControlePNCP` é a chave do instrumento. `numeroControlePNCPCompra` vincula o instrumento à contratação de origem e não é usado como chave de deduplicação.

## 4.5 Compras compartilhadas

A diferença entre CNPJ do instrumento e CNPJ da contratação de origem é preservada. A exclusão de origem externa é teste de robustez, não especificação principal.

## 4.6 Tipos de instrumento e multiplicidade

A especificação principal preserva os instrumentos observados. Serão reportadas robustezes:

- exclusão de empenhos;
- colapso conservador `compra × comprador × fornecedor` ao maior valor observado;
- distribuição por tipo de instrumento.

## 4.7 Critérios de elegibilidade

Especificação operacional atual: pelo menos 3 fornecedores e 5 instrumentos. O artigo reportará sensibilidade a 5/10, 5/20 e 10/20; o corte final anual somente será congelado após a conclusão da coleta.

# 5. Metodologia

## 5.1 Participação financeira do fornecedor

Para comprador `b`, fornecedor `s` e período `t`:

`V_bst = Σ_k V_k`

`q_bst = V_bst / Σ_s V_bst`

## 5.2 PortfolioHHI bruto

`PortfolioHHI_bt = Σ_s q_bst²`

## 5.3 PortfolioHHI normalizado

Para `N_bt > 1`:

`PortfolioHHI_norm_bt = (PortfolioHHI_bt - 1/N_bt) / (1 - 1/N_bt)`

A versão normalizada reduz o componente mecânico do piso associado ao número de fornecedores.

## 5.4 CR1, CR4 e número efetivo

`CR1_bt = max_s(q_bst)`

`CR4_bt = Σ_{s ∈ Top4} q_bst`

`Neff_bt = 1 / PortfolioHHI_bt`

## 5.5 Concentração por frequência

`p_bst = n_bst / Σ_s n_bst`

`CountHHI_bt = Σ_s p_bst²`

Calcular também `CountHHI_norm` com piso `1/N`.

## 5.6 Divergência valor–frequência

Comparar HHI bruto/normalizado por valor e frequência, diferenças, rankings, proporções e número efetivo.

## 5.7 Rede global comprador–fornecedor

`G_t = (B,S,E)`

`Degree_st = |{b : V_bst > 0}|`

`Strength_st = Σ_b V_bst`

As métricas são calculadas na rede global observada antes da filtragem da amostra elegível.

## 5.8 Exposição estrutural do comprador

Usando percentis globais:

`Edegree_bt = Σ_s q_bst Pdegree_st`

`Estrength_bt = Σ_s q_bst Pstrength_st`

Strength é a medida principal de exposição estrutural; Degree é complementar.

## 5.9 Matriz concentração × exposição

Classificar compradores relativamente aos percentis de HHI e exposição Strength:

- baixa concentração / baixa exposição;
- baixa concentração / alta exposição = **exposição estrutural oculta**;
- alta concentração / baixa exposição;
- alta concentração / alta exposição = **criticidade combinada**.

Os rótulos são classificações analíticas relativas e dinâmicas.

## 5.10 Simulações de choque sistêmico

Para conjunto removido `R`:

`Loss_bt(R) = Σ_{s∈R} q_bst`

Para limiar `τ`:

`Severe_t(R,τ) = (1/N_B) Σ_b I[Loss_bt(R) >= τ]`

Comparar:

- remoção aleatória;
- remoção por Strength global;
- remoção por Degree global;
- 1%, 5% e 10% dos fornecedores;
- limiares de perda de 25%, 50% e 75%;
- 1.000 sorteios aleatórios com semente fixa e intervalo empírico de 95%.

## 5.11 Criticidade de fornecedor único

Para cada fornecedor `s`, retirar somente esse nó e calcular:

`SingleLoss_bs = q_bs`

Contar quantos compradores perdem pelo menos 25%, 50% e 75% da carteira. Essa análise distingue um fornecedor localmente crítico da vulnerabilidade a conjuntos de fornecedores centrais.

## 5.12 Ranking restrito como robustez

Repetir centralidades na rede elegível apenas como verificação de sensibilidade. A especificação principal permanece global.

## 5.13 Estabilidade longitudinal dos sinais

Para compradores elegíveis em janelas sucessivas, medir:

- correlação de Spearman dos rankings;
- retenção no quartil superior;
- Jaccard dos conjuntos sinalizados;
- matriz de transição dos quadrantes;
- estabilidade da classificação de exposição oculta.

A persistência serve para avaliar utilidade de screening; não transforma a classificação em atributo permanente.

## 5.14 Decomposição temporal do HHI

Para janelas `t` e `t+1`, decompor sequencialmente:

`ΔHHI = (HHI_antigos_reponderados - HHI_t) + (HHI_t+1 - HHI_antigos_reponderados)`

Primeiro se reponderam apenas fornecedores já existentes; depois se incorporam os entrantes. A identidade é exata para o HHI bruto na ordem escolhida, mas não possui interpretação causal.

## 5.15 Integração fiscal incremental

Para compradores com município único, reutilizar observações SICONFI já coletadas e consultar somente novos códigos IBGE à medida que a coorte cresce.

Variáveis principais:

- `ln(População)`;
- `ln(DespesaEmpenhada per capita)`;
- macrorregião;
- `ln(N fornecedores)`;
- `ln(Instrumentos por fornecedor)`.

`ProcurementIntensity = ValorContratadoPNCP / DespesaEmpenhadaSICONFI` permanece diagnóstico de escala em coortes parciais.

## 5.16 Modelos associativos

Especificação preferida para `PortfolioHHI_norm`:

`HHI_norm_b = β0 + β1 ln(Pop_b) + β2 ln(DespesaPC_b) + β3 ln(NFornec_b) + β4 ln(InstrPorFornec_b) + Região + ε_b`

Inferência principal: OLS com erros-padrão agrupados por município. Robustez: fractional logit com a mesma estrutura. Modelos adicionais: gap valor–frequência e exposição Strength.

# 6. Resultados — ordem narrativa recomendada

## 6.1 Formação da amostra e qualidade

Fluxo de registros, duplicidades, tipos de fornecedor, lags, instrumentos, compradores e fornecedores.

## 6.2 Concentração da carteira

HHI bruto, HHI normalizado, CR1, CR4 e número efetivo. Mostrar que o nível absoluto depende da maturidade da carteira e do corte de elegibilidade.

## 6.3 Valor versus frequência

Documentar a persistente diferença entre concentração monetária e concentração por frequência.

## 6.4 Estrutura da rede e exposição oculta

Apresentar Strength, Degree, exposição do comprador e matriz concentração × exposição. Destacar que HHI local e exposição estrutural são correlacionados apenas parcialmente.

## 6.5 Choques direcionados versus aleatórios

Resultado principal de vulnerabilidade sistêmica: retirada conjunta dos fornecedores mais centrais por Strength produz impacto muito superior ao cenário aleatório.

## 6.6 Criticidade individual versus vulnerabilidade coletiva

Resultado-chave da versão v4: a retirada de um único fornecedor raramente produz impacto sistêmico amplo. Até março, apenas 224 de 9.583 fornecedores geram perda >=50% em ao menos um comprador; somente 2 atingem cinco ou mais compradores; o máximo é 7/780. Portanto, os grandes choques direcionados decorrem da combinação de nós centrais, não de um superfornecedor universal.

## 6.7 Estabilidade temporal do screening

Nos 569 compradores elegíveis em jan–fev e jan–mar:

- exposição Strength: `ρ ≈ 0,921`;
- retenção do quartil superior Strength: `≈80,4%`;
- estabilidade do quadrante completo: `≈82,3%`;
- retenção dos casos de exposição oculta: `≈77,8%`.

Interpretação: sinal persistente o suficiente para triagem, mas dinâmico.

## 6.8 Por que o HHI cai com a maturação da carteira

Decomposição jan–fev → jan–mar:

- 82,1% dos compradores comuns recebem novos fornecedores;
- mediana de 4 entrantes;
- efeito mediano da reponderação antiga ≈ 0;
- efeito mediano da entrada = -0,0182 no HHI;
- nos compradores com entrantes, delta HHI mediano = -0,0350;
- nos sem entrantes, delta mediano = 0.

A queda do HHI é predominantemente compatível com diluição pela entrada de fornecedores à medida que a carteira se forma.

## 6.9 Integração fiscal e modelos associativos

Cobertura SICONFI jan–mar: aproximadamente 99%. Apresentar modelos com VIF baixo, efeitos de região e clusters municipais. Resultado associativo estável: população positiva e número de fornecedores negativo para HHI normalizado; despesa per capita sem associação relevante. Para exposição Strength, recorrência e amplitude da carteira apresentam padrão distinto, reforçando a separação conceitual entre HHI e vulnerabilidade estrutural.

# 7. Robustez

## 7.1 Critérios de elegibilidade

3/5, 5/10, 5/20 e 10/20.

## 7.2 HHI bruto versus normalizado

Mostrar que níveis absolutos variam com tamanho da carteira, mas os resultados substantivos principais persistem.

## 7.3 Ranking global versus restrito

Global principal; restrito complementar.

## 7.4 Strength versus Degree

Strength principal devido à maior estabilidade a compras compartilhadas, maior relação com perda de carteira e melhor aderência à vulnerabilidade monetária.

## 7.5 Valor inicial versus valor global

Na coorte jan–mar, 99,67% dos instrumentos com ambos positivos apresentam valores praticamente iguais; resultados permanecem invariantes.

## 7.6 Tipos de instrumento e multiplicidade

Comparar todos os instrumentos, exclusão de empenhos e colapso conservador compra–comprador–fornecedor. A estrutura central dos achados persiste.

## 7.7 Compras compartilhadas

Excluir `origem_externa` e comparar amostra comum. Strength deve permanecer como métrica principal devido à maior robustez observada.

## 7.8 Lags negativos

Exclusão de observações com lag negativo como teste; impacto desprezível nos resultados.

## 7.9 Bootstrap condicional

Intervalos de reamostragem dos compradores para medianas e proporções. Explicitar que não corrigem viés de cobertura.

## 7.10 Forma funcional econométrica

OLS agrupado por município versus fractional logit; efeitos territoriais de região versus especificações mais granulares.

# 8. Discussão

## 8.1 Dependência é multidimensional

A diferença entre concentração por valor, frequência, centralidade e criticidade deve ser o eixo conceitual da discussão.

## 8.2 A vulnerabilidade é coletiva

O principal achado de rede não é a existência de um fornecedor universalmente crítico, mas a sensibilidade da rede a conjuntos centrais de fornecedores. Essa distinção deve evitar linguagem excessiva sobre single points of failure.

## 8.3 Screening dinâmico

A estabilidade dos rankings sustenta uso dos indicadores para priorização, mas as transições observadas impedem tratá-los como classificações permanentes.

## 8.4 Maturação da carteira e HHI

A entrada de fornecedores reduz mecanicamente e economicamente a concentração observada em muitas carteiras. O artigo deve evitar comparar níveis de HHI de janelas com maturidades muito diferentes sem controles e normalização.

## 8.5 Aplicação em auditoria e governança

Usos legítimos:

- priorização de unidades para análise;
- seleção de carteiras de fornecedores;
- identificação de dependências ocultas;
- planejamento de testes de continuidade e substituibilidade;
- discussão de concentração operacional e resiliência.

O indicador não substitui evidência de auditoria nem avaliação jurídica/econômica específica.

# 9. Limitações

- cobertura e maturidade histórica do PNCP;
- publicações tardias;
- valor contratado não equivale a execução financeira;
- centralidade não mede substituibilidade técnica;
- simulações não modelam resposta adaptativa do comprador;
- remoções direcionadas são contrafactuais estruturais, não probabilidades de falha;
- HHI depende do conjunto de fornecedores observado e da maturidade da janela;
- controles SICONFI pertencem ao município e podem ser compartilhados por múltiplos compradores;
- modelos associativos permanecem sujeitos a variáveis omitidas;
- screening relativo depende da composição da amostra;
- base anual ainda é necessária antes de afirmações nacionais definitivas.

# 10. Conclusão — argumento esperado

A conclusão deverá sustentar que a dependência de fornecedores públicos possui dimensões locais e sistêmicas que não são intercambiáveis. A concentração monetária identifica desequilíbrio interno da carteira; a recorrência descreve repetição contratual; a centralidade revela posição do fornecedor na rede; a criticidade individual mede dependência direta; e os choques conjuntos revelam vulnerabilidade sistêmica coletiva. A utilidade prática está em combinar essas métricas para triagem e governança de risco, sem transformá-las em diagnósticos automáticos de irregularidade.

# Tabelas previstas

1. Formação da amostra e qualidade dos dados.
2. Estatísticas de concentração por valor e frequência.
3. Sensibilidade dos critérios de elegibilidade.
4. Centralidade e exposição estrutural.
5. Matriz concentração × exposição.
6. Choques Strength/Degree versus aleatório.
7. Criticidade de fornecedor único.
8. Estabilidade longitudinal dos rankings e quadrantes.
9. Decomposição da mudança do HHI.
10. Cobertura e estatísticas SICONFI.
11. Modelos OLS agrupados por município.
12. Robustez fractional logit.
13. Robustez de instrumentos, valores, compras compartilhadas e lags.

# Figuras previstas

1. Fluxograma da construção da amostra.
2. Distribuição do HHI bruto e normalizado.
3. HHI por valor versus HHI por frequência.
4. Rede bipartida agregada ou distribuição das centralidades, evitando visualização ilegível da rede completa.
5. Matriz HHI × exposição Strength.
6. Curvas de dano direcionado versus aleatório.
7. Distribuição da criticidade de fornecedor único.
8. Sankey/matriz de transição dos quadrantes entre janelas.
9. Decomposição da variação do HHI com e sem entrantes.
10. Estabilidade cumulativa mensal das métricas centrais.

# Apêndices previstos

- dicionário de variáveis;
- regras de identificação do comprador;
- política de dados PJ/PF/PE;
- hashes e manifestos das partições;
- detalhes da API e retries;
- sensibilidade de elegibilidade;
- ranking global versus restrito;
- tipos de instrumento e multiplicidade;
- valorInicial versus valorGlobal;
- compras compartilhadas;
- lags temporais;
- bootstrap condicional;
- modelos alternativos;
- criticidade individual completa;
- decomposição temporal do HHI;
- protocolo de replicação.

# Estado da evidência na v4

Os resultados até março de 2025 devem ser apresentados como **diagnóstico acumulado intermediário**. Eles já são suficientes para fixar a arquitetura metodológica e a narrativa analítica, mas não para substituir a base anual. Abril e os meses seguintes devem ser usados principalmente para testar estabilidade, ampliar cobertura e verificar se os principais padrões persistem, evitando reformular a metodologia a cada novo mês sem evidência de falha estrutural.