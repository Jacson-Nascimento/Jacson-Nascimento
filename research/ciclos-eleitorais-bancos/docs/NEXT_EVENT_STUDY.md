# Especificação prévia do event study

## Objetivo

Testar se existe dinâmica de ROA ao redor das eleições gerais além da sazonalidade trimestral comum.

## Eventos

Eleições gerais de 2002, 2006, 2010, 2014, 2018 e 2022.

`k=0` será o trimestre efetivo da eleição, T4.

Janela inicial:

`k=-4,-3,-2,-1,0,+1,+2,+3,+4`

Referência:

`k=-1`.

## Especificações mínimas

1. série setorial média por trimestre, com sazonalidade de trimestre do ano e tendência;
2. painel bancário com efeitos fixos de banco, sazonalidade de trimestre do ano e controles bancários;
3. modelo sem interações eleitorais como benchmark interpretável;
4. versão interagida apenas como comparação com a dissertação, reportando efeitos marginais.

## Inferência

- Newey-West/HAC na série agregada;
- cluster por trimestre e/ou Driscoll-Kraay no painel, conforme especificação;
- leave-one-election-out dos perfis;
- bandas de confiança e teste conjunto dos coeficientes pré-eleição.

## Limitação de identificação

Como o evento eleitoral é nacional e ocorre simultaneamente para todos os bancos, não existe grupo contemporâneo não tratado. O event study será interpretado como padrão temporal associativo, não como estimador causal clássico.

## Critérios pré-definidos

Um padrão só será tratado como evidência eleitoral relevante se:

1. não for explicado apenas pela sazonalidade de T4;
2. apresentar dinâmica temporal coerente ao redor de `k=0`;
3. não depender de um único ciclo;
4. sobreviver a inferência compatível com poucos eventos temporais;
5. tiver magnitude economicamente relevante.
