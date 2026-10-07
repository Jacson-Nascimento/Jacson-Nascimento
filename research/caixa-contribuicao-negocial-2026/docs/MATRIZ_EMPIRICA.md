# Matriz empírica nacional

Posição da coleta: 07/10/2026.

Este documento resume o estado da coleta pública por base sindical. A matriz operacional completa permanece fora do repositório público de perfil, em conformidade com a política de dados do projeto.

## Regra de inclusão

Cada linha territorial é classificada por:

- base sindical e UF;
- universo elegível, quando publicado ou reconstruível;
- tipo de evidência;
- mecanismo de oposição ou restituição;
- janela temporal;
- canal utilizado;
- requisitos formais;
- fonte pública;
- possibilidade de cálculo financeiro.

Não se preenche denominador por aproximação demográfica, quantidade de municípios ou quantidade de agências.

## Cobertura em 07/10/2026

- 25 bases territoriais cadastradas;
- 21 bases com procedimento público de oposição/restituição localizado total ou parcialmente;
- 8 bases com universo pontual defensável;
- 3 bases com intervalo ou limite inferior;
- 7 grandes bases ainda sem denominador público: Brasília, Belo Horizonte, Pernambuco, Goiás, Campinas, Curitiba e Porto Alegre.

## Bases com denominador pontual

| Base | Universo | Classificação | Observação |
|---|---:|---|---|
| São Paulo, Osasco e região | cerca de 11.000 | P2 | contagem pública aproximada de trabalhadores habilitados às assembleias |
| Bahia, SBBA | 1.881 | P2 | aptos publicados |
| Juiz de Fora e região | 516 | P2 | aptos publicados |
| Londrina e região | 457 | P2 | aptos publicados |
| Pelotas e região | 227 | P2+M1 | 164 votantes e 72,25% de participação; reconstrução aritmética |
| Campina Grande e região | 198 | P2+M1 | 180 votantes e 90,91% de participação |
| Patos de Minas e região | 132 | P2 | aptos publicados |
| Criciúma e região | 206 | P2+M1 | 161 votos e 78,16% de participação |

### Checagem de Pelotas

A publicação sindical informa 72,25% de participação e distribuição de 58,54%, 39,02% e 2,44% dos votos. Esses percentuais são reproduzidos exatamente por 96, 64 e 4 votos, totalizando 164 votantes. A relação 164/227 corresponde a 72,2467%, que arredonda para 72,25%.

Uma reportagem local, citando o sindicato, informa aproximadamente 230 trabalhadores na base. Esse número é usado apenas como validação externa de ordem de grandeza, não como denominador da assembleia.

## Bases com intervalo ou limite inferior

| Base | Informação utilizável | Tratamento |
|---|---|---|
| Rio de Janeiro | 2.711 participantes representam mais de 78% da base | intervalo de aptos, não ponto |
| Espírito Santo | 1.352 participantes | limite inferior |
| Joinville e região | 266 participantes | limite inferior |

## Grandes bases ainda sem denominador

As páginas públicas localizadas para Brasília, Belo Horizonte, Pernambuco, Goiás, Campinas e Curitiba informam procedimento, percentuais de votação ou ambos, mas não número absoluto de aptos ou taxa de participação que permita reconstrução defensável. Porto Alegre continua pendente de fonte pública específica com denominador e procedimento claramente atribuível à base.

Nesses casos, a matriz mantém o universo como `NA`.

## Procedimentos de oposição e restituição

A coleta já demonstra heterogeneidade institucional:

- formulário eletrônico: São Paulo, Brasília, Espírito Santo, Sergipe;
- e-mail: Pernambuco, Campo Grande, Goiás, Santa Cruz do Sul;
- presencial: Rio de Janeiro, Campinas;
- combinação presencial/e-mail: Juiz de Fora, Pelotas, Uberaba, Petrópolis;
- presencial/AR: Ceará e Belo Horizonte;
- WhatsApp com envio de formulário: Criciúma;
- mecanismos de restituição da parcela local: Bahia, Belo Horizonte e outras bases identificadas;
- mecanismos em duas etapas, oposição preventiva e restituição posterior: Joinville e Uberaba.

Essas diferenças serão tratadas como atributos procedimentais observados. Não serão interpretadas como prova de maior ou menor restrição sem evidência empírica adicional.

## Resultados de assembleias usados para denominadores

Os resultados de votação são usados apenas quando fornecem contagem de aptos, votantes ou taxa de participação.

Exemplos:

- Bahia: 1.881 aptos e 1.854 votantes;
- Juiz de Fora: 516 aptos e 427 votantes;
- Londrina: 457 aptos e participação de 81,84%;
- Espírito Santo: 1.352 votantes;
- Pelotas: participação de 72,25% com percentuais de voto que permitem reconstrução;
- Campina Grande: 180 votos e participação de 90,91%;
- Patos de Minas: 132 aptos e 99 votantes.

Percentuais isolados, como os publicados em Belo Horizonte, Pernambuco, Campinas e Curitiba, não são convertidos em quantidade de empregados.

## Parâmetros financeiros

A consulta pública ao acórdão do TST no processo `DCG-1000975-72.2026.5.00.0000` confirma para a contribuição sobre remuneração fixa:

- alíquota de 1,5%;
- mínimo individual de R$ 63,00;
- máximo individual de R$ 310,00;
- 70% destinados ao sindicato da base;
- direito de oposição.

A regra específica de contribuição sobre PLR, incluindo o teto de R$ 262,30 reproduzido por fontes sindicais, permanece separada até confirmação primária específica.

## Uso no artigo

A tabela nacional será a base dos resultados empíricos. Cada valor deverá ser apresentado como:

1. observado diretamente;
2. reconstruído aritmeticamente;
3. intervalo ou limite;
4. modelado;
5. não estimado.

O artigo não transformará ausência de informação em estimativa pontual e não equiparará oposição pré-desconto, restituição posterior da parcela local e devolução automática a sindicalizados.
