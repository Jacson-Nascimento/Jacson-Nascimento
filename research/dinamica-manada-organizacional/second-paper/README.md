# Artigo complementar: concentração de influência e reversão da maioria informacional

Autor: Jacson Cruz do Nascimento  
Projeto-base: Dinâmica de Manada Organizacional  
DOI de referência: 10.5281/zenodo.21985858  
Status: análise secundária teórico-computacional, versão de trabalho 0.2

## Objetivo

Este diretório contém as análises do segundo artigo derivado da mesma realização computacional do preprint Dinâmica de Manada Organizacional. O foco não é reivindicar como novo o resultado geral de que concentração de influência pode prejudicar a sabedoria coletiva. Essa relação já aparece na literatura de aprendizagem em redes. A contribuição específica é decompor como uma maioria nominalmente correta pode ser revertida dentro do arcabouço organizacional hierárquico do estudo-base, calcular analiticamente a probabilidade dessa reversão e investigar como a intensidade da semente errada se relaciona com sua amplificação posterior.

## Status epistemológico

A análise é secundária, exploratória e não pré-registrada. Os 10.000 vetores de sinais e a rede de referência foram definidos no estudo-base. A versão 0.2 acrescenta verificações posteriores de robustez, explicitamente identificadas como tais.

## Núcleo reproduzível

A análise utiliza:

- 10.000 vetores de sinais individuais do depósito publicado;
- metadados dos 60 agentes;
- matriz de adjacência A;
- matriz de influência W do cenário-base;
- processo gerador documentado com NumPy/PCG64 e seed 20260816;
- probabilidade analítica de semente incorreta sob sinais gaussianos independentes;
- 500 novas redes Watts-Strogatz para robustez estrutural;
- 1.000 permutações dos papéis hierárquicos na rede publicada;
- sensibilidade do critério de manada entre 70% e 90%.

Não são tratados como novos resultados deste artigo os módulos de Sobol, topologias alternativas e extensão não linear do manuscrito-base quando não integram o núcleo exato do pacote de replicação v1.1.

## Principais controles da versão 0.2

- fração média de sinais corretos: 84,0247%;
- menor maioria correta observada: 63,33%;
- sementes estruturais incorretas na realização-base: 1.729/10.000 = 17,29%;
- probabilidade analítica de semente incorreta no cenário-base: 17,0122%;
- peso estacionário do executivo: 52,6477%;
- peso dos seis agentes superiores: 95,6359%;
- tamanho efetivo de fontes: 3,1408;
- média de P(S) em 500 novas redes: 17,4563%;
- intervalo estrutural empírico 2,5%-97,5% nas 500 redes: 16,9332%-18,4308%;
- média de P(S) em 1.000 permutações dos papéis: 22,3500%;
- intervalo estrutural empírico nas permutações: 20,6174%-23,8971%;
- P(H|S) no cenário beta=0,70/c=0,90 permanece entre 59,63% e 65,47% para cortes de manada entre 90% e 70%;
- P(H|S) no cenário beta=0,75/c=0,95 permanece entre 90,17% e 91,90% no mesmo intervalo de cortes.

AUC e regressão logística permanecem apenas como diagnósticos suplementares do mecanismo, não como evidência de validação preditiva.

## Estrutura

- tools/analyze_reversal.py: análise principal, robustez e geração de figuras;
- outputs/expected/: valores de controle versionados;
- outputs/generated/: saídas locais reproduzidas;
- figures/generated/: figuras locais;
- manuscript/ARTIGO_COMPLEMENTAR_v0_1.md: versão histórica inicial;
- manuscript/ARTIGO_COMPLEMENTAR_v0_2.md: versão revisada após parecer técnico-acadêmico;
- ACADEMIC_REVIEW_v0_1.md: parecer interno e tratamento das fragilidades;
- REPRODUCIBILITY.md: protocolo de replicação.

O arquivo CHECKSUMS.sha256 registra o conjunto histórico da versão 0.1. A versão 0.2 será acompanhada por um novo conjunto de hashes no pacote suplementar de publicação, preservando o histórico anterior.

## Reprodução

A partir de research/dinamica-manada-organizacional:

1. instalar environment/python-requirements.txt;
2. executar tools/generate_reference_data.py;
3. instalar second-paper/environment/python-requirements.txt;
4. executar second-paper/tools/analyze_reversal.py --validate.

O workflow `Reproduce herd dynamics second paper` executa a mesma sequência no GitHub Actions. A versão 0.2 foi validada juntamente com o pipeline-base e o controle de dados públicos.

## Interpretação

Os resultados descrevem propriedades do experimento computacional e do processo gerador especificado. Eles não estimam prevalência de conformidade, silêncio organizacional ou efeito manada em equipes reais. O cenário-base associa deliberadamente maior hierarquia a maior ruído para testar uma condição de estresse. Hierarquia, por si só, não é interpretada como fonte automática de erro.
