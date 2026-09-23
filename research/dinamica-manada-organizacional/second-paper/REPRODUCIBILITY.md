# Protocolo de replicação do artigo complementar - v0.2

## Dependência do estudo-base

O segundo artigo reutiliza, por desenho, os 10.000 vetores de evidência do DOI 10.5281/zenodo.21985858. A versão 0.2 acrescenta resultados analíticos e verificações estruturais que não dependem de uma nova amostra humana ou de alteração dos dados publicados.

## Etapas

1. Gerar a realização oficial com `tools/generate_reference_data.py` na raiz do estudo-base.
2. Executar `second-paper/tools/analyze_reversal.py --validate`.
3. Comparar automaticamente as tabelas produzidas em `outputs/generated/` com `outputs/expected/`.
4. Gerar as figuras em `figures/generated/`.
5. Verificar as saídas analíticas, o conjunto de 500 redes, as 1.000 permutações de papéis e a sensibilidade do corte de manada.

## Processo analítico adicional

Sob:

`e_i = theta + epsilon_i`, com `epsilon_i ~ N(0, sigma_i^2)` independentes,

o agregado estrutural `Z = pi'e` é normal com:

- média = `theta`;
- variância = `sum_i pi_i^2 sigma_i^2`.

Assim:

`P(S=1) = Phi(-|theta| / sqrt(sum_i pi_i^2 sigma_i^2))`.

Essa expressão é usada como controle independente da realização Monte Carlo para a formação da semente.

## Critérios de aceitação principais

A reprodução deve retornar:

- 1.729 sementes estruturais incorretas na realização-base;
- P(S) Monte Carlo = 0,172900000000;
- P(S) analítica em kappa=5 = 0,170122439385;
- desvio-padrão do agregado estrutural em kappa=5 = 1,048568082889;
- n_eff(kappa=5) = 3,140783586954;
- peso do executivo em kappa=5 = 0,526477382521;
- peso Top 6 em kappa=5 = 0,956359480167.

### Curva analítica por kappa

- kappa=2: P(S) exata = 0,002926157268;
- kappa=3: 0,044831140654;
- kappa=4: 0,112750227977;
- kappa=5: 0,170122439385.

### Robustez em 500 novas redes

Com papéis fixos e seeds 20260912 a 20261411:

- P(S) média = 0,174563481365;
- mediana = 0,174170357066;
- percentil 2,5% = 0,169331637898;
- percentil 97,5% = 0,184307997885;
- n_eff médio = 3,041224628923;
- peso médio do executivo = 0,538984384769.

### Robustez de posição hierárquica

Com 1.000 permutações, RNG `default_rng(20260912)`, movendo conjuntamente `h` e `sigma`:

- P(S) média = 0,223499855301;
- mediana = 0,223659436304;
- percentil 2,5% = 0,206174192357;
- percentil 97,5% = 0,238971056382;
- n_eff médio = 2,070675404944;
- peso médio do executivo = 0,686464076434.

### Sensibilidade ao limiar de manada

Para beta=0,70 e c=0,90:

- tau=0,70: P(H|S)=0,654713707345;
- tau=0,80: 0,627530364372;
- tau=0,90: 0,596298438404.

Para beta=0,75 e c=0,95:

- tau=0,70: P(H|S)=0,919028340081;
- tau=0,80: 0,910931174089;
- tau=0,90: 0,901677270098.

Diferenças superiores a 1e-9 nos controles principais devem ser tratadas como falha de reprodução, salvo tolerância específica documentada no script.

## Automação

O workflow `.github/workflows/reproduce-herd-dynamics-second-paper.yml`:

1. regenera a realização-base;
2. instala as dependências do segundo artigo;
3. executa `analyze_reversal.py --validate`;
4. publica tabelas e figuras geradas como artefato do workflow.

Após a revisão v0.2, os seguintes checks concluíram com sucesso no mesmo commit:

- Reproduce herd dynamics second paper;
- Reproduce herd dynamics baseline;
- public-data-guard.

## Limite inferencial

O protocolo demonstra reprodução computacional. Não demonstra validade externa. A solução analítica depende do processo gerador gaussiano independente. As novas redes permanecem dentro da família Watts-Strogatz especificada. As permutações de papéis são testes estruturais, não modelo empírico de alocação de cargos. A análise é secundária, exploratória e não pré-registrada.
