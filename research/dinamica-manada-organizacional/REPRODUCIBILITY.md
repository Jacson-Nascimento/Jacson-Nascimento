# Protocolo de replicabilidade

## Registro científico de referência

A versão publicada deste protocolo e dos artefatos associados integra o depósito Zenodo do preprint v1.3:

- Registro: https://zenodo.org/records/21985858
- DOI: https://doi.org/10.5281/zenodo.21985858
- Publicação: 17 de agosto de 2026

## Objetivo

Este protocolo define o procedimento mínimo para reproduzir o experimento-base do preprint e verificar os números publicados sem depender de inferências sobre a implementação.

## Processo gerador de dados

Para cada agente `i`:

```text
s_i = theta + epsilon_i
epsilon_i ~ Normal(0, sigma_i^2)
q_i = 1/sigma_i^2
```

No cenário de estresse:

```text
sigma_i = 0.90 + h_i
```

A evidência utilizada na implementação-base é `e_i = s_i`.

## Rede e hierarquia

A rede inicial é Watts-Strogatz com 60 nós, 6 vizinhos iniciais e probabilidade de reconexão 0.12. Após a geração da rede, são incluídos auto-laços:

```text
a_ii = 1
```

A matriz de influência é construída por:

```text
w_ij(kappa) = a_ij exp(kappa h_j) / sum_k a_ik exp(kappa h_k)
```

No cenário-base, `kappa = 5`.

## Distribuição estacionária

O vetor `pi` satisfaz:

```text
pi' W = pi'
sum_i pi_i = 1
```

A semente estrutural incorreta é definida por:

```text
S = 1[ sign(pi'e) != sign(theta) ]
```

## Solução estacionária

Para cada combinação de `beta` e `c`, define-se `lambda = 0.80 - beta`. A manifestação pública estacionária é calculada diretamente por:

```text
y* = lambda(1-c) [(lambda+beta)I - (beta+lambda*c)W]^-1 e
```

O evento de manada usa corte de 80%:

```text
H_0.80 = 1[ mean(sign(y_i*) != sign(theta)) >= 0.80 ]
```

## Quatro pontos de controle da Tabela 5

| beta | c | P(H|S) esperado | P(H) esperado |
|---:|---:|---:|---:|
| 0.30 | 0.30 | 0.0000% | 0.0000% |
| 0.50 | 0.60 | 0.0000% | 0.0000% |
| 0.70 | 0.90 | 62.7530% | 10.85% |
| 0.75 | 0.95 | 91.0931% | 15.75% |

Entre as 1.729 replicações com semente incorreta, os dois últimos pontos produzem respectivamente 1.085 e 1.575 eventos de manada.

## Critérios de aceitação

Uma reprodução é classificada como exata quando:

1. gera 10.000 replicações;
2. produz 1.729 sementes incorretas;
3. obtém fração média correta de aproximadamente 0.8402466667;
4. obtém peso estacionário do executivo de aproximadamente 0.5264773825;
5. obtém peso acumulado dos seis agentes superiores de aproximadamente 0.9563594802;
6. obtém `n_eff` de aproximadamente 3.140783587;
7. reproduz as contagens condicionais 1.085 e 1.575 nos dois pontos extremos da Tabela 5.

Diferenças pequenas de impressão decimal são aceitáveis. Diferenças nas contagens inteiras indicam que a rede, os auto-laços, o RNG, a ordem dos agentes ou a sequência dos sorteios não coincidem com a realização de referência.

## Independência entre softwares

A seed `20260816` é um identificador de inicialização, não uma garantia de sequência universal. NumPy/PCG64 e o RNG padrão do R geram sequências diferentes. A reprodução estatística independente em R deve ser comparada em termos de distribuição e probabilidades, não linha a linha.

## Integridade científica

Os percentuais simulados demonstram comportamento interno do modelo sob condições especificadas. Eles não devem ser interpretados como prevalência empírica de comportamento de manada em organizações ou equipes de auditoria.
