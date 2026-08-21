# Journal Version V2 e robustez por CNPJ raiz

Data: 21/08/2026

## Objetivo

Registrar os ajustes realizados após a avaliação editorial do Paper 1 e os resultados da robustez que agrega estabelecimentos de fornecedores pela raiz do CNPJ.

## Correções metodológicas da rodada de revisão

1. A definição de discordância foi reescrita em linguagem direta e em notação matemática para evitar corrupção de renderização: comprador com HHI abaixo do 75º percentil e exposição LOO no 75º percentil ou acima.
2. Discussão e conclusão foram separadas funcionalmente. A discussão passou a enfatizar mecanismo, literatura, validade e interpretação; a conclusão foi condensada em três parágrafos.
3. Foram formalizadas cinco hipóteses analíticas direcionais, sem limiares numéricos calibrados pelos resultados e com declaração explícita de que não houve preregistro.
4. O stress test passou a distinguir remoção estática da rede de processos reais de duração, mitigação e recuperação.
5. A passagem de 1.347 compradores para 725 foi esclarecida: 1.335 compradores entram no WLS e pertencem a 725 municípios; 725 é a unidade da robustez agregada municipal.
6. O WLS foi justificado pelo peso `1/N_m`, que equaliza aproximadamente o peso total dos municípios cujas covariáveis fiscais são repetidas para múltiplos compradores. Não é ponderação por variância inversa.
7. A interpretação substantiva de regressões nível-log passou a usar `beta * ln(2)` para representar duplicação do regressor.
8. A tabela de screening foi ampliada com verificações gerenciais por quadrante.
9. A comparação com Pliatsidis (2024) permanece qualitativa, pois o estudo grego trabalha com subnetworks por grupos CPV e medida de concentração derivada da distribuição de Degree, não com HHI/CR1 de carteira por comprador.
10. O repositório público e os scripts auditáveis são indicados explicitamente na seção de reprodutibilidade.

## Robustez por CNPJ raiz

Script: `scripts/robustez_cnpj_raiz_paper1.py`

Workflow: `.github/workflows/robustez-cnpj-raiz-paper1.yml`

Saídas: `results/robustez_cnpj_raiz_2025_06/`

A análise utiliza os oito primeiros dígitos do CNPJ de fornecedor PJ como unidade alternativa. Identificadores fora do padrão de 14 dígitos são mantidos individualizados.

### Validação dos identificadores

- instrumentos econômicos PJ: 98.438;
- identificadores de 14 dígitos válidos: 98.407, 99,97%;
- fornecedores CNPJ completo na rede original: 20.367;
- CNPJ raízes na rede: 20.092;
- raízes com múltiplos estabelecimentos: 163, 0,81%;
- máximo de estabelecimentos sob uma mesma raiz: 22.

### Amostra fixa de 1.347 compradores

Nenhum comprador cai abaixo do critério de três fornecedores após a agregação, e a elegibilidade recalculada permanece em 1.347.

Medianas, CNPJ completo para CNPJ raiz:

- HHI: 0,236465 para 0,236521;
- HHI normalizado: 0,156335 para 0,156335;
- CR1: 0,383678 para 0,384960;
- número de fornecedores: 14 para 14;
- Strength LOO: 0,298937 para 0,309857;
- Degree LOO: 0,295817 para 0,306559.

Correlações de ranking original versus raiz:

- HHI normalizado: rho = 0,9991;
- CR1: rho = 0,9988;
- número de fornecedores: rho = 0,9997;
- Strength LOO: rho = 0,9877;
- Degree LOO: rho = 0,9881.

Na especificação por raiz:

- Strength LOO vs. Degree LOO: rho = 0,9491;
- HHI normalizado vs. Strength LOO: rho = -0,0084, p = 0,7591;
- HHI normalizado vs. Degree LOO: rho = -0,0682, p = 0,0123.

### Discordância concentração-exposição

Strength LOO:

- original: 221 compradores, 16,41%;
- raiz: 220 compradores, 16,33%;
- retenção da classificação original: 95,48%.

Degree LOO:

- original: 237 compradores, 17,59%;
- raiz: 234 compradores, 17,37%;
- retenção da classificação original: 96,62%.

Sobreposição entre Strength LOO e Degree LOO na especificação por raiz: 88,64%.

### Stress test por CNPJ raiz

Perda simulada de pelo menos 50% da carteira:

- top 1%: direcionado 9,13%; benchmark ponderado 5,65%;
- top 5%: direcionado 34,60%; benchmark ponderado 23,36%;
- top 10%: direcionado 49,07%; benchmark ponderado 39,22%.

A massa de Strength nos top 1%, 5% e 10% é 57,69%, 79,64% e 87,54%, respectivamente.

## Interpretação

A agregação matriz-filial pela raiz do CNPJ não altera substantivamente a conclusão do Paper 1. Rankings de concentração e exposição permanecem quase invariantes, a elegibilidade não muda, as classificações de discordância apresentam retenção superior a 95% e os stress tests preservam o contraste entre remoção direcionada e benchmark ponderado.

A robustez não deve ser apresentada como consolidação de grupo econômico. Empresas sob controle comum podem operar com raízes distintas, exigindo informação societária adicional para uma consolidação econômica completa.

## Arquivo editorial corrente

`paper/PAPER1_JOURNAL_VERSION_V2.md`

O preprint `paper/PAPER1_JAN_JUN_2025_PREPRINT_V1.md` e a `paper/PAPER1_JOURNAL_VERSION_V1.md` permanecem preservados como histórico. Nenhuma regra de coleta, chave de identificação ou período econômico foi alterada nesta rodada.