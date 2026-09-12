# Artigo complementar: concentração de influência e reversão da maioria informacional

Autor: Jacson Cruz do Nascimento  
Projeto-base: Dinâmica de Manada Organizacional  
DOI de referência: 10.5281/zenodo.21985858  
Status: análise complementar replicável, versão de trabalho 0.1

## Objetivo

Este diretório contém as análises do segundo artigo derivado da mesma realização computacional do preprint Dinâmica de Manada Organizacional. O foco não é repetir a demonstração de efeito manada. A pergunta complementar é como uma maioria nominalmente correta pode produzir um agregado estrutural incorreto quando a influência é concentrada, e em que medida a intensidade dessa semente errada antecipa sua propagação posterior.

## Delimitação metodológica

A análise usa somente componentes integralmente reproduzíveis do pacote publicado:

- 10.000 vetores de sinais individuais;
- metadados dos 60 agentes;
- matriz de adjacência A;
- matriz de influência W do cenário-base;
- quatro cenários de propagação arquivados e regeneráveis;
- processo gerador documentado com NumPy/PCG64 e seed 20260816.

Não são tratados como novos resultados deste artigo os módulos de Sobol, topologias alternativas e extensão não linear que não integram o núcleo exato de replicação do pacote v1.1.

## Principais achados de controle

- fração média de sinais corretos: 84,0247%;
- menor maioria correta observada: 63,33%;
- sementes estruturais incorretas: 1.729/10.000, ou 17,29%;
- peso estacionário do executivo: 52,6477%;
- peso dos seis agentes superiores: 95,6359%;
- tamanho efetivo de fontes: 3,1408;
- P(S | executivo errado): 55,8347%;
- P(S | executivo correto): 0,5735%;
- P(executivo errado | S): 97,6865%;
- AUC da margem da semente para manada em beta=0,70 e c=0,90: 0,9933;
- AUC da margem da semente para manada em beta=0,75 e c=0,95: 0,9984.

## Estrutura

- tools/analyze_reversal.py: análise principal e geração de figuras;
- outputs/expected/: valores de controle versionados;
- outputs/generated/: saídas locais reproduzidas;
- figures/generated/: figuras locais;
- manuscript/ARTIGO_COMPLEMENTAR_v0_1.md: manuscrito;
- REPRODUCIBILITY.md: protocolo de replicação;
- CHECKSUMS.sha256: hashes dos artefatos textuais versionados.

## Reprodução

A partir de research/dinamica-manada-organizacional:

1. instalar environment/python-requirements.txt;
2. executar tools/generate_reference_data.py;
3. instalar second-paper/environment/python-requirements.txt;
4. executar second-paper/tools/analyze_reversal.py --validate.

O script regenera as tabelas, produz três figuras e compara os resultados com os controles versionados.

## Interpretação

Os percentuais descrevem o comportamento interno de um experimento computacional. Eles não estimam prevalência de conformidade, silêncio organizacional ou efeito manada em equipes reais. O cenário-base foi intencionalmente configurado com associação negativa entre posição hierárquica e precisão dos sinais para testar uma condição de estresse.
