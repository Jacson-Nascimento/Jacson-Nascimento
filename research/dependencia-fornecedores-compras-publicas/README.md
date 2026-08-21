# Dependência de Fornecedores e Compras Públicas

Projeto quantitativo sobre concentração da carteira de fornecedores, exposição externa em rede, recorrência contratual e vulnerabilidade estrutural nas compras públicas municipais.

## Estratégia de publicação

O projeto possui dois papers complementares.

### Paper 1: janeiro a junho de 2025

**Preprint:** *Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição Externa em Rede e Testes de Estresse*.

Versão de circulação acadêmica e registro de precedência:

`paper/PAPER1_JAN_JUN_2025_PREPRINT_V1.md`

**Versão corrente para submissão a periódico:** *Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração Local, Exposição Externa Leave-One-Buyer-Out e Testes de Estresse*.

`paper/PAPER1_JOURNAL_VERSION_V2.md`

Histórico editorial para periódico:

`paper/PAPER1_JOURNAL_VERSION_V1.md`

A Journal Version V2 preserva o preprint e a V1 como histórico. Ela incorpora hipóteses analíticas não calibradas por limiares observados, esclarece a unidade dos modelos fiscais e a ponderação WLS, diferencia indisponibilidade estática de processos de mitigação e recuperação, amplia a aplicação gerencial dos quadrantes e adiciona robustez por CNPJ raiz. A especificação principal de coleta, chaves, elegibilidade, LOO e stress testing permanece preservada.

Histórico de desenvolvimento: `PAPER1_JAN_JUN_2025_V1.md`, `V2.md` e `V3.md`.

### Paper 2: ano de 2025 completo

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

Especificação anual corrente:

`paper/PAPER2_ANUAL_2025_V2.md`

O Paper 2 deve citar o Paper 1 e evitar reprodução integral de contribuição, tabelas e discussão. Sua contribuição própria é longitudinal e de validação anual, incluindo a captura tardia de instrumentos assinados em 2025 e publicados em 2026.

## Unidade e regras preservadas

Unidade principal de análise:

`comprador institucional (CNPJ) × fornecedor × ano`

Regras:

- comprador principal = CNPJ institucional do órgão ou entidade;
- chave do instrumento = `numeroControlePNCP`, materializada como `id_contrato`;
- `numeroControlePNCPCompra` é somente ligação com a compra e nunca chave de deduplicação;
- município é dimensão territorial e fonte de controles fiscais;
- bases públicas identificadas contêm somente fornecedores pessoa jurídica;
- HHI mede concentração da carteira do comprador, não concentração antitruste de mercado relevante;
- modelos econométricos são associativos e não causais;
- HHI, recorrência, persistência e centralidade não implicam fraude ou favorecimento;
- acumulados janeiro-M não representam o ano completo.

## Distinção conceitual central

### Importância sistêmica do fornecedor

`Strength_j = sum_b(V_bj)`

O Strength global bruto mede massa monetária sistêmica observada e permanece o ranking principal dos testes de estresse.

### Exposição externa do comprador

Para comprador `b`:

`Strength_j^(-b) = Strength_j - V_bj`

`Degree_j^(-b) = Degree_j - I(V_bj > 0)`

Strength LOO é a medida preferencial de exposição externa. Degree LOO é complementar. A exposição Strength bruta permanece apenas para comparabilidade histórica.

## Resultados auditados do Paper 1

A coorte janeiro-junho contém 105.582 instrumentos PJ únicos, dos quais 98.438 foram assinados em 2025. Há 2.349 compradores com métricas, 1.347 elegíveis no critério principal e 20.367 fornecedores na rede global.

Resultados centrais:

- Strength bruto vs. Strength LOO: `rho = 0,2647`;
- Degree bruto vs. Degree LOO: `rho = 0,9821`;
- Strength LOO vs. Degree LOO: `rho = 0,9500`;
- HHI normalizado vs. Strength LOO: `rho = -0,0183`;
- HHI normalizado vs. Degree LOO: `rho = -0,0763`;
- discordância por Strength LOO: 221 compradores, 16,41%;
- discordância por Degree LOO: 237 compradores, 17,59%;
- sobreposição entre classificações LOO: 89,14%.

O benchmark mecânico sob independência dos cortes Q75 é 18,75%. Esses percentuais não representam prevalência anormal nem evidência de irregularidade.

## Persistência longitudinal LOO

Abril-maio:

- `rho` Strength LOO: 0,8962;
- `rho` Degree LOO: 0,9091;
- retenção da discordância: 85,96% e 87,57%.

Maio-junho:

- `rho` Strength LOO: 0,9266;
- `rho` Degree LOO: 0,9416;
- retenção da discordância: 90,40% e 90,61%.

A persistência é interpretada como estabilidade de screening, não permanência causal de risco.

## Testes de estresse

Para perda simulada de pelo menos 50% da carteira:

- top 1% direcionado: 8,91%, contra 5,46% no benchmark ponderado por Strength;
- top 5%: 34,15%, contra 22,88%;
- top 10%: 48,26%, contra 38,52%.

Os testes são cenários estáticos de indisponibilidade da rede observada. Não modelam duração, estoques, substituição, renegociação ou recuperação.

## Robustez por CNPJ raiz

Script:

`scripts/robustez_cnpj_raiz_paper1.py`

Workflow:

`.github/workflows/robustez-cnpj-raiz-paper1.yml`

Resultados:

`results/robustez_cnpj_raiz_2025_06/`

Na amostra fixa de 1.347 compradores, a agregação de estabelecimentos pelos oito primeiros dígitos do CNPJ preserva os resultados:

- HHI normalizado original vs. raiz: `rho = 0,9991`;
- CR1: `rho = 0,9988`;
- número de fornecedores: `rho = 0,9997`;
- Strength LOO: `rho = 0,9877`;
- Degree LOO: `rho = 0,9881`;
- Strength LOO raiz vs. Degree LOO raiz: `rho = 0,9491`;
- HHI normalizado raiz vs. Strength LOO raiz: `rho = -0,0084`;
- HHI normalizado raiz vs. Degree LOO raiz: `rho = -0,0682`.

A elegibilidade permanece em 1.347 compradores. A discordância Strength LOO passa de 221 para 220 compradores, com retenção de 95,48%; Degree LOO passa de 237 para 234, com retenção de 96,62%.

No stress test por raiz, as perdas severas direcionadas nos top 1%, 5% e 10% são 9,13%, 34,60% e 49,07%, contra 5,65%, 23,36% e 39,22% no benchmark ponderado.

CNPJ raiz aproxima a consolidação matriz-filial, mas não representa necessariamente grupo econômico sob controle comum.

## Modelos complementares

A integração SICONFI segue duas unidades analíticas distintas:

- 1.335 compradores com despesa empenhada disponível entram no WLS no nível do comprador;
- esses compradores pertencem a 725 municípios, utilizados como observações na robustez agregada municipal.

O número 725, portanto, representa mudança da unidade de análise e não perda de quase metade da amostra por ausência fiscal.

No WLS, cada comprador do município `m` recebe peso `1/N_m`. A finalidade é equalizar aproximadamente o peso total de cada município, pois as covariáveis fiscais municipais são repetidas para múltiplos CNPJs compradores. Não se trata de ponderação por variância inversa. Os erros-padrão são agrupados por município.

## Reprodutibilidade

Scripts principais:

- `scripts/analisar_acumulado_2025_global.py`
- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`
- `scripts/calcular_exposicao_loo_generica.py`
- `scripts/diagnosticos_longitudinais_loo_jan_jun_2025.py`
- `scripts/robustez_cnpj_raiz_paper1.py`

Resultados e logs:

- `results/carteira_acumulada_2025_06_global/`
- `results/robustez_estrutural_2025_06/`
- `results/robustez_modelos_municipio_2025_06/`
- `results/exposicao_loo_2025_04/`
- `results/exposicao_loo_2025_05/`
- `results/exposicao_loo_2025_06/`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/`
- `results/robustez_cnpj_raiz_2025_06/`.

Cada robustez nova possui `log_execucao.txt` versionado junto às saídas correspondentes.

## Regra temporal anual

- coleta por data de publicação no PNCP;
- período econômico anual: instrumentos assinados de 01/01/2025 a 31/12/2025;
- após dezembro, captura tardia em 2026 de instrumentos assinados em 2025;
- a base anual será congelada somente depois da captura tardia e das validações de duplicidade, janela temporal e hash.

## Estado atual

O Paper 1 possui três marcos editoriais deliberadamente preservados: `PAPER1_JAN_JUN_2025_PREPRINT_V1.md` para circulação e precedência, `PAPER1_JOURNAL_VERSION_V1.md` como primeira versão para periódico e `PAPER1_JOURNAL_VERSION_V2.md` como versão corrente de submissão em desenvolvimento. A V2 incorpora a robustez por CNPJ raiz e os ajustes teóricos, econométricos e gerenciais do ciclo de revisão de 21/08/2026. O Paper 2 permanece aberto e não deve receber resultados anuais antes do fechamento janeiro-dezembro e da captura tardia de 2026.