# Dependência de Fornecedores e Compras Públicas

Projeto quantitativo sobre concentração da carteira de fornecedores, exposição externa em rede, recorrência contratual e vulnerabilidade estrutural nas compras públicas municipais.

## Estratégia de publicação

O projeto possui dois papers complementares.

### Paper 1: janeiro a junho de 2025

**Preprint:** *Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração da Carteira, Exposição Externa em Rede e Testes de Estresse*.

**Journal Version V1:** *Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração Local, Exposição Externa Leave-One-Buyer-Out e Testes de Estresse*.

Objetivo: propor e validar o framework que combina concentração local da carteira, exposição externa leave-one-buyer-out, discordância concentração-exposição, testes de estresse e persistência longitudinal.

**Versão de circulação acadêmica e registro de precedência:**

`paper/PAPER1_JAN_JUN_2025_PREPRINT_V1.md`

**Versão separada para futura submissão a periódico:**

`paper/PAPER1_JOURNAL_VERSION_V1.md`

A Journal Version V1 preserva integralmente a metodologia e os resultados auditados do preprint, mas reforça o posicionamento científico, amplia a literatura consolidada anterior a 2025, reduz ressalvas repetitivas e padroniza a apresentação numérica.

Histórico de desenvolvimento: `PAPER1_JAN_JUN_2025_V1.md`, `V2.md` e `V3.md`.

Artefatos editoriais:

- referências do preprint: `paper/references_paper1.bib`;
- referências consolidadas da journal version: `paper/references_paper1_journal_v1.bib`;
- figuras vetoriais: `paper/figures/`;
- tabelas reproduzíveis: `paper/tables/`;
- nota de fechamento do preprint: `paper/NOTA_EDITORIAL_PREPRINT_PAPER1_2026-08-20.md`.

### Paper 2: ano de 2025 completo

**Persistência Temporal da Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Evidência Anual, Redes e Testes de Estresse**

Objetivo: testar a estabilidade do framework durante janeiro-dezembro, decompor efeitos de composição, acompanhar os testes de estresse e as associações fiscais e medir a sensibilidade à captura tardia de instrumentos assinados em 2025 e publicados em 2026.

Especificação anual corrente:

`paper/PAPER2_ANUAL_2025_V2.md`

O Paper 2 deve citar o Paper 1 e evitar repetição integral de texto, tabelas e contribuição. Sua contribuição própria é longitudinal e de validação anual.

## Unidade e regras de identificação

Unidade principal de análise:

`comprador institucional (CNPJ) × fornecedor × ano`

Regras preservadas:

- comprador principal = CNPJ institucional do órgão ou entidade;
- chave do instrumento = `numeroControlePNCP`, materializada como `id_contrato`;
- `numeroControlePNCPCompra` é somente ligação com a compra e nunca chave de deduplicação;
- município é dimensão territorial e fonte de controles;
- bases públicas identificadas contêm somente fornecedores pessoa jurídica;
- HHI mede concentração da carteira do comprador, não concentração antitruste de mercado relevante.

## Distinção conceitual central

A robustez leave-one-buyer-out separou duas funções do Strength.

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

- correlação exposição Strength bruta vs. Strength LOO: `rho = 0,2647`;
- correlação Degree bruto vs. Degree LOO: `rho = 0,9821`;
- Strength LOO vs. Degree LOO: `rho = 0,9500`;
- HHI normalizado vs. Strength LOO: `rho = -0,0183`;
- HHI normalizado vs. Degree LOO: `rho = -0,0763`;
- discordância concentração-exposição por Strength LOO: 221 compradores, 16,41%;
- por Degree LOO: 237 compradores, 17,59%;
- sobreposição entre classificações LOO: 89,14%.

O benchmark mecânico sob independência dos cortes Q75 é 18,75%. Esses percentuais não representam prevalência anormal nem evidência de fraude.

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

O ranking principal dos choques permanece o Strength bruto. Para perda simulada de pelo menos 50% da carteira:

- top 1% direcionado: 8,91%, contra 5,46% em sorteios de igual tamanho ponderados por Strength;
- top 5%: 34,15%, contra 22,88%;
- top 10%: 48,26%, contra 38,52%.

Os top 1%, 5% e 10% concentram 57,56%, 79,47% e 87,41% da massa total de Strength observada.

O procedimento com número variável de fornecedores para igualar massa de Strength é apenas diagnóstico de concentração sistêmica, não contrafactual comparável de superioridade do ataque direcionado.

## Modelos complementares

A integração SICONFI é associativa e não causal. As robustezes incluem:

- WLS com peso `1/N_m`, equalizando peso municipal;
- modelo agregado ao município;
- CR1 e CR4 como outcomes alternativos ao HHI normalizado;
- Strength LOO e Degree LOO como outcomes de exposição externa.

Com a externalização, a antiga associação positiva entre número de fornecedores e exposição Strength desaparece. Recorrência contratual permanece positiva e consistente nos modelos de exposição externa, mas é frágil nos modelos de concentração local.

## Journal Version V1: alterações editoriais

A versão para periódico implementa quatro ajustes sem recalcular a base ou alterar a metodologia:

1. reforço explícito no título, resumo e abstract de que a contribuição está na integração entre concentração local, exposição LOO, discordância e stress testing;
2. ampliação do lastro teórico com literatura consolidada sobre dependência de recursos, complexidade da base de fornecedores, redes, disrupção e resiliência;
3. condensação de ressalvas repetitivas, concentrando limites interpretativos em métodos, discussão e limitações;
4. padronização de correlações e coeficientes em quatro casas decimais e percentuais em duas casas, inclusive nas figuras específicas da journal version.

A versão editorial em Word/PDF possui 12 páginas e passou por inspeção visual, auditoria de acessibilidade e preflight de PDF.

## Reprodutibilidade

Scripts principais:

- `scripts/analisar_acumulado_2025_global.py`
- `scripts/robustez_estrutural_generica.py`
- `scripts/robustez_modelos_municipio_generica.py`
- `scripts/calcular_exposicao_loo_generica.py`
- `scripts/diagnosticos_longitudinais_loo_jan_jun_2025.py`

Resultados e logs:

- `results/carteira_acumulada_2025_06_global/`
- `results/robustez_estrutural_2025_06/`
- `results/robustez_modelos_municipio_2025_06/`
- `results/exposicao_loo_2025_04/`
- `results/exposicao_loo_2025_05/`
- `results/exposicao_loo_2025_06/`
- `results/diagnosticos_longitudinais_loo_jan_jun_2025/`

Os novos resultados possuem `log_execucao.txt` versionado junto às saídas correspondentes.

## Regras de interpretação

- HHI, recorrência, persistência e centralidade não implicam fraude ou favorecimento.
- centralidade não mede probabilidade de falha ou substituibilidade técnica.
- testes de estresse são cenários mecânicos de perda de carteira.
- modelos econométricos são associativos.
- ausência mensal de município não implica falha de reporte.
- acumulados janeiro-M não representam o ano completo.

## Regra temporal anual

- coleta por data de publicação no PNCP;
- período econômico anual: instrumentos assinados de 01/01/2025 a 31/12/2025;
- após dezembro, captura tardia em 2026 de instrumentos assinados em 2025;
- a base anual será congelada somente depois da captura tardia e das validações de duplicidade, janela temporal e hash.

## Estado atual

O Paper 1 possui duas versões editoriais deliberadamente separadas: `PAPER1_JAN_JUN_2025_PREPRINT_V1.md`, preservado para circulação e precedência, e `PAPER1_JOURNAL_VERSION_V1.md`, preparada para futura submissão a periódico. A Journal Version V1 amplia a literatura consolidada e enxuga a redação, sem alterar qualquer resultado auditado. O Paper 2 permanece aberto e não deve receber resultados anuais antes da conclusão de janeiro-dezembro e da captura tardia de 2026.