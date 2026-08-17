# Dinâmica de Manada Organizacional

**Autor:** Jacson Cruz do Nascimento  
**Preprint:** versão 1.0, 17 de agosto de 2026  
**Natureza:** proof of concept teórico-computacional, não revisado por pares

Este diretório reúne o material computacional necessário para auditar e reproduzir o núcleo do preprint **Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional**.

## Escopo reproduzido

O pacote cobre o cenário-base Monte Carlo e os resultados centrais validados independentemente:

- 60 agentes;
- estado verdadeiro `theta = -1`;
- rede Watts-Strogatz com `k = 6` e `p = 0.12`;
- `rho = 0.20`;
- `kappa = 5` no cenário-base;
- `beta` entre 0.05 e 0.75;
- `lambda = 0.80 - beta`;
- `c` entre 0 e 0.95;
- 10.000 replicações;
- seed documentada `20260816`;
- critério de manada: pelo menos 80% dos agentes incorretos no equilíbrio.

A hierarquia é formada por 1 executivo (`h=1.00`), 5 gestores (`h=0.65`), 12 seniores (`h=0.30`) e 42 demais agentes (`h=0`). No cenário de estresse, `sigma_i = 0.90 + h_i`.

## Detalhe de implementação crítico

A matriz de adjacência inclui **auto-influência**, isto é, `a_ii = 1` para todos os agentes. Os auto-laços são adicionados antes da ponderação hierárquica:

```text
A <- A + I
w_ij(kappa) = a_ij exp(kappa h_j) / sum_k a_ik exp(kappa h_k)
```

Sem esse detalhe, a concentração de influência publicada não é reproduzida.

## Valores de controle

| Métrica | Valor esperado |
|---|---:|
| Fração média de sinais corretos | 84.0247% |
| Menor fração correta observada | 63.33% |
| Sementes estruturais incorretas | 1.729 / 10.000 |
| `P(S)` | 17.29% |
| Peso estacionário do executivo | 52.6477% |
| Peso dos seis agentes superiores | 95.6359% |
| `n_eff = 1/sum(pi_i^2)` | 3.1408 |
| `P(H|S)`, beta=0.70, c=0.90 | 62.7530% |
| `P(H|S)`, beta=0.75, c=0.95 | 91.0931% |

## Estrutura

```text
research/dinamica-manada-organizacional/
├── README.md
├── REPRODUCIBILITY.md
├── CITATION.cff
├── LICENSE_NOTICE.md
├── environment/
│   └── python-requirements.txt
├── tools/
│   └── generate_reference_data.py
├── R/
│   ├── 00_config.R
│   ├── 01_reproduzir_resultados_baseline.R
│   ├── 02_reproduzir_tabela5.R
│   ├── 03_reproduzir_figuras.R
│   └── 04_simulacao_independente_R.R
├── run_all.R
├── data/
│   └── README.md
└── outputs/
    ├── expected_baseline_summary.csv
    └── expected_table5.csv
```

## Fluxo de reprodução

1. Gerar a realização estocástica de referência e as matrizes estruturais:

```bash
python tools/generate_reference_data.py
```

2. Executar a análise em R:

```bash
Rscript run_all.R
```

3. Comparar as saídas geradas com os arquivos de referência em `outputs/`.

## RNG e reprodução exata

A realização estocástica oficial foi reconstruída com `NumPy default_rng(20260816)`, cujo gerador é PCG64. Uma seed numérica não produz automaticamente a mesma sequência em R e Python. Por isso, o repositório separa:

- **geração exata dos dados de referência**, em Python, compatível com a realização validada;
- **análise e reprodução dos resultados**, em R;
- **simulação estatística independente em R**, para verificar o mecanismo sem exigir igualdade bit a bit.

Essa separação é deliberada e documenta a proveniência do experimento.

## Dados brutos e Zenodo

A tabela completa das 10.000 replicações deve permanecer arquivada no mesmo depósito Zenodo do preprint como material suplementar. O GitHub mantém o código, a especificação do processo gerador, os valores de controle e a automação de reprodução. Isso evita tratar o GitHub como repositório primário de dados científicos de maior volume.

O DOI do preprint/material suplementar deve ser inserido aqui e em `CITATION.cff` após o depósito definitivo.

## Limites atuais

Este repositório reproduz o núcleo Monte Carlo validado, a formação da semente incorreta, os quatro pontos da Tabela 5 e as Figuras 4 a 6 do cenário-base. Os módulos de Sobol, topologias alternativas e extensão não linear devem ser adicionados somente quando todas as escolhas de implementação estiverem integralmente especificadas e auditadas.
