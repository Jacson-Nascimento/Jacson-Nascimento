# Registro Técnico 007 - Validação das Simulações de Choque Estrutural

## Objetivo

Verificar se o procedimento de remoção direcionada de fornecedores produz comportamento distinto da remoção aleatória antes de aplicar o método à base anual completa.

## Base diagnóstica

Foi utilizada a amostra sentinela de 2025, restrita a fornecedores pessoa jurídica e a 416 compradores institucionais com pelo menos 3 fornecedores e 5 instrumentos observados.

A rede continha 4.199 fornecedores PJ distintos. O teste utiliza as participações financeiras observadas na carteira de cada comprador.

A amostra não é probabilística e é fortemente influenciada por compras compartilhadas. Portanto, os resultados abaixo não representam estimativas nacionais.

## Estratégias

Foram comparadas:

1. remoção dos fornecedores com maior `Degree`;
2. remoção dos fornecedores com maior `Strength`;
3. 1.000 remoções aleatórias da mesma quantidade de fornecedores.

Foram testadas remoções de 1% e 5% dos fornecedores observados.

Para cada comprador:

`Loss_b(R) = soma das participações financeiras dos fornecedores removidos`

Foram medidos:

- perda média da carteira;
- proporção com perda >= 25%;
- proporção com perda >= 50%;
- proporção com qualquer perda.

## Remoção de 1%

Foram removidos 42 fornecedores.

### Degree direcionado

- perda média: 19,08%;
- compradores com perda >= 25%: 27,64%;
- compradores com perda >= 50%: 20,67%;
- compradores afetados: 42,07%.

### Strength direcionado

- perda média: 3,54%;
- perda >= 25%: 4,33%;
- perda >= 50%: 3,85%;
- compradores afetados: 4,57%.

### Remoção aleatória

Média de 1.000 simulações:

- perda média: 1,01%;
- perda >= 25%: 1,04%;
- perda >= 50%: 0,36%;
- compradores afetados: 13,86%.

Percentil 95 das simulações aleatórias:

- perda média: 1,94%;
- perda >= 25%: 2,16%;
- perda >= 50%: 0,96%.

## Remoção de 5%

Foram removidos 210 fornecedores.

### Degree direcionado

- perda média: 31,99%;
- perda >= 25%: 38,70%;
- perda >= 50%: 33,17%;
- compradores afetados: 59,86%.

### Strength direcionado

- perda média: 17,89%;
- perda >= 25%: 22,84%;
- perda >= 50%: 16,11%;
- compradores afetados: 45,67%.

### Remoção aleatória

Média de 1.000 simulações:

- perda média: 5,02%;
- perda >= 25%: 5,73%;
- perda >= 50%: 2,02%;
- compradores afetados: 46,59%.

Percentil 95 das simulações aleatórias:

- perda média: 6,87%;
- perda >= 25%: 8,41%;
- perda >= 50%: 3,37%.

## Interpretação metodológica

O teste demonstra que o código distingue choques direcionados de remoções aleatórias e que Degree e Strength capturam exposições diferentes.

No piloto, Degree gerou impacto muito maior que Strength, indicando que fornecedores conectados a muitos compradores podem ser estruturalmente relevantes mesmo quando não são os fornecedores de maior valor agregado da rede.

Esse resultado é coerente com a proposta de não reduzir vulnerabilidade estrutural à concentração monetária local.

## Cuidado substantivo

A magnitude observada não pode ser generalizada. A amostra sentinela é dominada por algumas UFs e por estruturas de compras compartilhadas. Um fornecedor de alto Degree pode aparecer em muitas unidades devido a mecanismos consorciados, o que pode ampliar artificialmente sua importância na rede sentinela.

## Decisão

A simulação de choque permanece no desenho do artigo. O teste substantivo deverá ser repetido sobre a rede anual completa e incluir, no mínimo:

- rede geral de fornecedores PJ;
- análise com e sem compras compartilhadas;
- remoção por Degree e Strength;
- 1.000 ou mais remoções aleatórias por cenário;
- intervalos empíricos da distribuição aleatória;
- limiares de perda de 25%, 50% e 75%;
- análise de sensibilidade para percentuais de remoção.
