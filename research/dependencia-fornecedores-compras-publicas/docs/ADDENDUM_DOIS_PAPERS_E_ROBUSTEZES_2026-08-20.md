# Addendum metodológico e editorial — dois papers e robustezes

Data: 20/08/2026

Este documento complementa, sem substituir, o handoff e a metodologia congelada do projeto. A coleta mensal janeiro-dezembro de 2025 continua exatamente conforme o protocolo vigente. As mudanças abaixo afetam a estratégia de publicação, o posicionamento da contribuição e análises de robustez separadas.

## 1. Decisão editorial

O projeto produzirá dois papers.

### Paper 1

Janela empírica: publicações PNCP de janeiro a junho de 2025, com métricas econômicas restritas a instrumentos assinados em 2025.

Pergunta: em que medida a concentração da carteira captura ou deixa de capturar a exposição do comprador a fornecedores globalmente centrais e como essa exposição se manifesta sob choques coletivos?

Papel: proposição e validação inicial do framework.

Arquivo: `paper/PAPER1_JAN_JUN_2025_V1.md`.

### Paper 2

Janela empírica: ano de 2025 completo, com publicação janeiro-dezembro e captura tardia em 2026 de instrumentos assinados em 2025.

Pergunta: quão persistentes são os rankings, classificações e stress tests ao longo do ano e quão sensíveis são à expansão da rede, composição das coortes e publicação tardia?

Papel: validação temporal anual do framework.

Arquivo: `paper/PAPER2_ANUAL_2025_V1.md`.

## 2. Escopo corrigido

Os dados principais filtram esfera municipal e Poder Executivo. Títulos e conclusões devem falar em **compras públicas municipais** ou em **compradores públicos municipais observados no PNCP**, evitando generalização para todo o setor público brasileiro.

## 3. Originalidade: formulação conservadora

Não reivindicar originalidade isolada para:

- HHI;
- CR1/CR4;
- CountHHI;
- redes bipartidas;
- Degree;
- Strength;
- persistência de relações;
- centralidade;
- ataques direcionados.

A contribuição defendida é a integração, no nível do comprador, de concentração monetária local, posição global do fornecedor, exposição ponderada da carteira, discordância entre concentração e exposição, stress tests e persistência longitudinal.

## 4. Literatura recente a incorporar

### Institutional Closure Index

Fountoukidis, I.; Dafli, E.; Antoniou, I.; Varsakelis, N. (2026). *Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data*. SSRN 6765160, posted 18 May 2026.

O trabalho combina concentração, persistência e embeddedness em indicador de autoridade contratante. Deve ser citado explicitamente. A diferenciação do presente projeto está na exposição da carteira à posição global dos fornecedores e na vulnerabilidade sob choques sistêmicos simulados.

### Redes portuguesas de compras públicas

Trabalho publicado em EPJ Data Science em 2025 sobre earnings, hierarquia e influência em redes de compras públicas portuguesas. Usar para situar centralidade, concentração, comunidades e influência de fornecedores como literatura precedente.

### Redes de contratação no Brasil

Incorporar estudo recente que aplica análise de redes a contratações públicas federais brasileiras entre 2022 e meados de 2024. Isso elimina qualquer reivindicação de pioneirismo nacional no uso de network analysis.

### Supplier concentration e network position

Incorporar literatura de 2025-2026 que relaciona concentração de fornecedores, posição de rede, desempenho e resiliência em cadeias de suprimento. Usar como fundamento conceitual, sem importar relações causais do setor privado para o setor público.

## 5. Nova nomenclatura para o quadrante

A classificação histórica:

`HHI < Q75` e `Exposição Strength >= Q75`

permanece por comparabilidade, mas o texto deve evitar a expressão “baixa concentração” como descrição automática de `HHI < Q75`.

Preferir:

- **discordância concentração-exposição**;
- **exposição estrutural não capturada pelo HHI**.

A métrica não mede irregularidade. O benchmark mecânico sob independência entre classificações é 18,75%, portanto a prevalência observada não deve ser vendida como excesso anormal. O resultado relevante é a não redundância entre métricas e a identidade dos compradores classificados.

## 6. Robustez leave-one-buyer-out

Problema: o Strength global do fornecedor inclui o valor do próprio comprador cuja exposição está sendo medida.

Robustez:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Recalcular ranking e exposição específicos do comprador.

Resultados a reportar:

- rho original versus LOO;
- delta mediano e percentis;
- retenção do quartil superior;
- mudança no quadrante de discordância;
- contribuição própria ponderada no Strength.

Script: `scripts/robustez_estrutural_generica.py`.

## 7. Robustez do stress test

O teste principal permanece: top 1%, 5% e 10% por Strength versus remoções aleatórias uniformes de igual número de fornecedores.

Adicionar:

1. remoção aleatória de igual `k` com probabilidade de sorteio proporcional ao Strength;
2. remoção aleatória de número variável de fornecedores até alcançar aproximadamente a mesma massa sistêmica de Strength retirada pelo ataque direcionado.

Esses nulos adicionais reduzem a objeção de que a diferença decorre apenas do fato mecânico de fornecedores de maior Strength concentrarem mais valor agregado.

Script: `scripts/robustez_estrutural_generica.py`.

## 8. Robustez da discordância HHI-exposição

Além do quadrante principal, calcular:

- percentil de HHI;
- percentil de exposição;
- `gap = PctExposure - PctHHI`;
- resíduo da exposição após regressão simples em HHI normalizado.

Essas métricas são robustness/screening, não novas definições principais.

## 9. Robustez dos modelos SICONFI

Problema: população e despesa são municipais, enquanto a unidade principal do modelo é o CNPJ comprador. Municípios com vários compradores podem receber peso implícito maior.

Adicionar:

- WLS no nível comprador com `peso = 1/N_compradores_municipio`;
- OLS em base agregada ao município;
- CR1 e CR4 como outcomes alternativos.

O número de fornecedores deve ser descrito como controle estrutural, pois é matematicamente relacionado a medidas de concentração e à normalização do HHI.

Script: `scripts/robustez_modelos_municipio_generica.py`.

## 10. Papel dos modelos econométricos

Os modelos SICONFI deixam de ser eixo central do manuscrito e passam a seção complementar de heterogeneidade/associação.

Hierarquia do Paper 1:

1. concentração local;
2. rede global;
3. exposição estrutural;
4. discordância concentração-exposição;
5. stress tests;
6. persistência longitudinal;
7. robustezes;
8. modelos fiscais associativos.

Hierarquia do Paper 2:

1. evolução mensal da rede;
2. persistência dos rankings;
3. composição das coortes;
4. estabilidade dos stress tests;
5. robustezes;
6. captura tardia;
7. estabilidade associativa fiscal.

## 11. Regras que permanecem inalteradas

- comprador principal = CNPJ institucional;
- chave do instrumento = `numeroControlePNCP`;
- nunca deduplicar por `numeroControlePNCPCompra`;
- concentração principal = carteira do comprador, não mercado relevante;
- GitHub público = fornecedores PJ identificados;
- nenhuma republicação de CPF/nome PF;
- Strength global = especificação principal dos choques;
- Degree = complementar;
- associação econométrica não é causalidade;
- HHI isolado não implica fraude/favoritismo;
- ausência mensal de município não implica falha de reporte;
- janeiro-M não equivale ao ano completo;
- coleta anual por publicação, período econômico por assinatura;
- após dezembro, captura tardia em 2026 antes do congelamento anual.

## 12. Regra de não redundância entre papers

O Paper 2 deve citar o Paper 1 como origem do framework. Não repetir integralmente introdução, revisão, tabelas ou interpretação do primeiro semestre. A publicação anual precisa ter contribuição própria centrada em persistência, expansão de rede, composição, captura tardia e validação temporal.
