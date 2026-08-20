# Resultados da robustez LOO e decisões para os dois papers

## Objetivo

Registrar os resultados auditáveis das robustezes adicionadas após a avaliação crítica do artigo e as consequências metodológicas para o Paper 1 e o Paper 2.

Os resultados abaixo foram produzidos por workflows reproduzíveis e possuem arquivos de saída e `log_execucao.txt` versionados na branch `research/dois-papers-robustez-2025`.

## 1. Correção principal: exposição Strength bruta

A medida de exposição do comprador baseada diretamente no Strength global mostrou forte componente de auto-inclusão.

Na amostra de 1.347 compradores elegíveis:

- Strength bruto x Strength LOO: `rho = 0,264704`;
- retenção do quartil superior após LOO: 38,87%;
- contribuição própria mediana ponderada do comprador ao Strength: 75,89%.

Decisão:

- **Strength bruto continua como medida principal de importância sistêmica monetária do fornecedor e ranking dos choques**;
- **Strength LOO passa a ser a medida preferencial de exposição externa do comprador**;
- **Degree LOO permanece complementar**;
- exposição Strength bruta aparece somente para comparabilidade histórica.

## 2. Validação das medidas externalizadas

- Degree bruto x Degree LOO: `rho = 0,982139`;
- Strength LOO x Degree LOO: `rho = 0,950043`;
- retenção do quartil superior Degree: 89,61%.

As medidas externalizadas convergem fortemente entre si.

## 3. HHI x exposição externa

- HHI normalizado x Strength LOO: `rho = -0,01829`, `p = 0,502`;
- HHI normalizado x Degree LOO: `rho = -0,07627`, `p = 0,0051`.

Decisão:

A tese central passa a ser formulada como **baixa redundância entre concentração local e exposição externa**, em vez de correlação positiva moderada entre HHI e Strength bruto.

## 4. Discordância concentração-exposição

Classificação: HHI abaixo do Q75 e exposição no Q75 ou acima.

- Strength LOO: 221 compradores, 16,41%;
- Degree LOO: 237 compradores, 17,59%;
- sobreposição Strength LOO x Degree LOO: 89,14%.

O benchmark mecânico sob independência dos cortes é 18,75%.

Decisão:

- substituir a expressão preferencial “exposição estrutural oculta” por **discordância concentração-exposição** ou **exposição externa não capturada pelo HHI**;
- não apresentar o percentual como prevalência anormal;
- usar gap de percentis e resíduo da exposição após HHI como robustezes contínuas.

## 5. Stress test com nulo mais exigente

Contrafactual adicional: 1.000 sorteios de igual número de fornecedores, sem reposição, com probabilidade proporcional ao Strength.

Perda de pelo menos 50% da carteira:

| Remoção | Direcionado | Aleatório ponderado | Intervalo empírico 2,5%-97,5% |
|---|---:|---:|---:|
| Top 1% | 8,91% | 5,46% | 4,31%-6,61% |
| Top 5% | 34,15% | 22,88% | 20,34%-24,94% |
| Top 10% | 48,26% | 38,52% | 36,75%-40,31% |

Massa total de Strength concentrada nos grupos direcionados:

- top 1%: 57,56%;
- top 5%: 79,47%;
- top 10%: 87,41%.

Decisão:

O cenário direcionado permanece acima do nulo ponderado. O diagnóstico de número variável de fornecedores necessário para atingir massa semelhante de Strength será tratado somente como evidência descritiva de concentração sistêmica, não como contrafactual comparável.

## 6. Robustez municipal dos modelos

Foram adicionados:

- WLS com peso `1/N_m`;
- OLS agregado ao município;
- CR1 e CR4 como outcomes de concentração;
- Strength LOO e Degree LOO como outcomes de exposição externa.

### Concentração local

No HHI normalizado, população permanece positiva, despesa per capita permanece sem robustez e número de fornecedores permanece negativo. Recorrência deixa de ser significativa a 5% quando o peso municipal é equalizado.

### Exposição externa

Strength LOO e Degree LOO apresentam resultados consistentes:

- número de fornecedores deixa de ser significativo;
- recorrência permanece positiva e altamente significativa;
- população passa a apresentar associação negativa;
- despesa per capita é negativa, com significância dependente da métrica e da especificação.

Decisão:

Abandonar como resultado substantivo a antiga associação positiva entre número de fornecedores e exposição Strength bruta. Destacar, com linguagem associativa, o contraste entre recorrência frágil para concentração local e recorrência consistente para exposição externa.

## 7. Persistência longitudinal LOO

### Abril para maio

- compradores comuns: 1.013;
- Strength LOO: `rho = 0,8962`;
- Degree LOO: `rho = 0,9091`;
- retenção da discordância Strength LOO: 85,96%;
- retenção da discordância Degree LOO: 87,57%;
- estabilidade do quadrante completo: 86,48% e 87,07%.

### Maio para junho

- compradores comuns: 1.210;
- Strength LOO: `rho = 0,9266`;
- Degree LOO: `rho = 0,9416`;
- retenção da discordância Strength LOO: 90,40%;
- retenção da discordância Degree LOO: 90,61%;
- estabilidade do quadrante completo: 89,50% e 90,41%.

Decisão:

A evidência de persistência longitudinal permanece e deverá usar medidas LOO como especificação principal de exposição do comprador.

## 8. Efeito de composição

Entre maio e junho, os 137 entrantes apresentaram:

- HHI mediano: 0,3606, acima dos compradores comuns, 0,2233;
- Strength LOO mediano: 0,2048, abaixo dos comuns, 0,3106;
- Degree LOO mediano: 0,1996, abaixo dos comuns, 0,3044.

Isso reforça a necessidade de decompor estatísticas transversais entre compradores comuns, entrantes e saídas.

## 9. Consequências editoriais

### Paper 1

Manuscrito principal: `paper/PAPER1_JAN_JUN_2025_V3.md`.

Papel: proposição e validação inicial do framework corrigido.

### Paper 2

Especificação anual: `paper/PAPER2_ANUAL_2025_V2.md`.

Papel: validação temporal anual usando Strength LOO e Degree LOO para exposição do comprador, mantendo Strength bruto nos stress tests.

## 10. Arquivos de auditoria

### Robustez estrutural

- `results/robustez_estrutural_2025_06/resumo_robustez_estrutural.json`
- `results/robustez_estrutural_2025_06/log_execucao.txt`

### Modelos municipais

- `results/robustez_modelos_municipio_2025_06/resumo_robustez_modelos.json`
- `results/robustez_modelos_municipio_2025_06/log_execucao.txt`

### Longitudinal LOO

- `results/diagnosticos_longitudinais_loo_jan_jun_2025/resumo_longitudinal_loo.json`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/log_execucao.txt`

## 11. Regras preservadas

Nenhuma mudança foi feita na metodologia de coleta mensal do PNCP, nas chaves, na política de privacidade ou na regra temporal anual. As alterações são correções de mensuração e robustez motivadas por diagnóstico quantitativo e registradas antes do fechamento anual do Paper 2.
