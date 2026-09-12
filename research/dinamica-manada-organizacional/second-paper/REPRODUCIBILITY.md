# Protocolo de replicação do artigo complementar

## Dependência do estudo-base

O segundo artigo não possui uma nova realização estocástica. Ele reutiliza, por desenho, os 10.000 vetores de evidência do DOI 10.5281/zenodo.21985858.

## Etapas

1. Gerar a realização oficial com tools/generate_reference_data.py na raiz do estudo-base.
2. Executar second-paper/tools/analyze_reversal.py --validate.
3. Comparar automaticamente as tabelas produzidas em outputs/generated/ com outputs/expected/.
4. Gerar as três figuras em figures/generated/.

## Critérios de aceitação

A reprodução deve retornar, entre outros controles:

- 1.729 sementes estruturais incorretas;
- P(S)=0,1729;
- P(S|executivo errado)=0,558347107438;
- P(S|executivo correto)=0,005734767025;
- n_eff(kappa=5)=3,140783586954;
- 39, 461, 1.133 e 1.729 sementes erradas em kappa=2,3,4,5;
- AUC da margem de 0,993305092023 e 0,998445681303 nos dois cenários de propagação.

Diferenças superiores a 1e-9 nas tabelas principais devem ser tratadas como falha de reprodução.

## Limite inferencial

O teste garante reprodução computacional, não validade externa. Os coeficientes e probabilidades não representam estimativas de organizações reais.
