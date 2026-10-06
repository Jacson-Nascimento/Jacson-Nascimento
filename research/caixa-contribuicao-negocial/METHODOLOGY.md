# Metodologia

## 1. Pergunta de pesquisa

Qual é a ordem de grandeza da contribuição negocial potencial associada aos empregados da Caixa Econômica Federal em 2026 e como esse potencial pode ser distribuído territorialmente entre UFs e, quando houver evidência pública suficiente, entre bases sindicais?

O estudo não pretende identificar descontos individuais nem estimar receita efetiva de uma entidade a partir de informação não pública.

## 2. Universo informacional

Somente dados públicos são admissíveis. Cada observação deve possuir referência no `data/source_register.csv`.

São excluídos, por desenho:

- dados de sistemas internos da CAIXA;
- relatórios ou consultas de acesso restrito;
- conhecimento funcional não publicado;
- planilhas internas, listas de lotação e dados individualizados;
- informações obtidas informalmente sem fonte pública verificável.

Se uma informação conhecida por outra via também estiver publicada, apenas a versão pública e sua fonte pública podem ser usadas.

## 3. Classificação da evidência

### A - observação pública direta

A fonte publica o quantitativo correspondente à variável e à base territorial analisada. Exemplo: 516 empregados aptos na base do SINTRAF Juiz de Fora.

Uma observação pode ser A e ainda ser aproximada. Exemplo: uma entidade declarar publicamente que possui "cerca de 11 mil" empregados da CAIXA em sua base. Nesse caso `evidence_grade=A` e `is_approximate=true`.

### B - reconstrução matemática

A fonte não publica diretamente o denominador, mas fornece elementos suficientes para reconstruí-lo sem hipótese distributiva adicional. Exemplo: 180 votantes correspondendo a 90,91% de participação implica aproximadamente 198 aptos.

### C - proxy/modelagem

O quantitativo depende de hipótese territorial ou estabilidade de estrutura histórica. Exemplo: estimar empregados por UF em junho de 2026 aplicando os pesos estaduais do quadro de representação do 33º CONECEF ao total nacional de 84.136.

### D - não estimado

Há informação insuficiente para produzir valor quantitativo defensável. A ausência permanece explícita.

## 4. Total nacional de referência

O total utilizado na modelagem inicial é:

`N_2026_06 = 84.136`

A fonte pública usada nesta etapa é secundária e atribui o número ao balanço semestral da CAIXA. Por isso o denominador é B, embora seja consistente com a série pública de 84.394 empregados no fim de 2025 e 84.363 em março de 2026.

O valor oficial de 2025, 84.394, funciona como controle de consistência.

## 5. Estrutura estadual histórica

O 33º CONECEF publicou uma tabela de quantitativos por UF usada para definir delegados na proporção de um delegado para cada 300 empregados. A soma da coluna é 92.596.

Entretanto, o Relatório de Sustentabilidade CAIXA 2017 registra 87.654 empregados no fechamento daquele exercício. A diferença é material, 4.942 pessoas ou aproximadamente 5,64% do total oficial de fechamento.

Assim, a tabela do CONECEF não é tratada como estoque oficial em 31/12/2017. Ela é apenas uma proxy da distribuição territorial usada pelo movimento sindical naquele período.

Para cada UF `i`, calcula-se o peso histórico:

`w_i = H_i / soma(H)`

onde `H_i` é o denominador publicado pelo CONECEF.

A cota teórica para junho de 2026 é:

`q_i = w_i * 84.136`

Como empregados são contagens inteiras, as cotas são reconciliadas pelo método de maiores restos:

1. atribuir `floor(q_i)` a cada UF;
2. calcular a diferença entre 84.136 e a soma das partes inteiras;
3. distribuir as unidades restantes às UFs com maiores partes decimais;
4. usar ordem alfabética da UF apenas como critério determinístico de desempate.

A soma final deve ser exatamente 84.136.

Esses valores recebem evidência C.

## 6. Bases sindicais

O objetivo preferencial é obter o número de empregados da CAIXA aptos a participar das assembleias específicas de 2026 em cada base sindical.

A razão é prática: o cadastro de aptos utilizado em assembleias específicas tende a se aproximar do universo territorial de empregados abrangidos pela entidade no momento da Campanha Nacional.

A regra de precedência é:

1. denominador público contemporâneo da própria base sindical;
2. reconstrução matemática a partir de votação contemporânea;
3. outros quantitativos públicos contemporâneos, com limitação explicitada;
4. proxy estadual somente para análise por UF, não para preencher automaticamente sindicato específico.

Portanto, o total estimado de empregados de uma UF não é distribuído entre seus sindicatos por população, PIB, agências, número de municípios ou qualquer outra variável sem validação empírica pública.

## 7. Evidências incompletas

Algumas publicações divulgam apenas percentuais ou número de participantes.

Exemplos:

- Brasília: 58,68% dos participantes rejeitaram a proposta, mas a fonte não informa participantes nem aptos. Evidência D para denominador.
- Rio de Janeiro: 2.711 participantes equivaleram a mais de 78% da base. Isso fornece uma restrição, mas não um denominador exato. Evidência D para valor pontual.
- FEEB-PR: percentuais agregados de nove bases foram divulgados sem número de votos ou aptos. Evidência D para denominador.
- Joinville: 266 participantes foram divulgados, mas sem total de aptos. O valor não é usado como denominador de arrecadação.

A regra é não converter essas informações em número exato de empregados.

## 8. Regra da contribuição negocial

O cenário principal da remuneração fixa utiliza os parâmetros publicamente divulgados para a sentença normativa do dissídio da CAIXA em 2026:

- alíquota: 1,5%;
- piso individual: R$ 63,00;
- teto individual: R$ 310,00;
- sindicato da base: 70%;
- federação: 15%;
- confederação: 10%;
- central: 5%.

A referência de CCT com piso de R$ 62,46 e teto de R$ 312,25 fica em cenário separado. Ela não é fundida com o cenário principal.

## 9. Por que não usar contribuição média pontual

A contribuição individual depende da base remuneratória definida na cláusula e é truncada entre piso e teto.

Sem microdados públicos ou uma distribuição pública da base remuneratória compatível com a cláusula, a média da remuneração contábil da empresa não identifica a média da contribuição. Usá-la como ponto estimado introduziria hipótese forte e pouco verificável.

O resultado principal é, portanto, um intervalo normativo.

Para `N` empregados:

`Bruto_min = N * 63`

`Bruto_max = N * 310`

`Sindicato_min = Bruto_min * 0,70`

`Sindicato_max = Bruto_max * 0,70`

Para 84.136 empregados:

- bruto mínimo: R$ 5.300.568,00;
- bruto máximo: R$ 26.082.160,00;
- parcela sindical mínima: R$ 3.710.397,60;
- parcela sindical máxima: R$ 18.257.512,00.

Esses são limites teóricos antes de oposição, devolução, compensação ou qualquer outra particularidade operacional.

## 10. PLR

A incidência sobre PLR é analisada em bloco separado. O teto divulgado é R$ 262,30 por pagamento.

Não se presume que todos os empregados atinjam esse teto e o valor não é somado automaticamente ao cenário salarial. Eventuais cenários de PLR devem declarar:

- número de pagamentos considerados;
- proporção de empregados atingindo o teto, se houver;
- tratamento das oposições;
- fonte normativa utilizada.

## 11. Oposição

A arrecadação potencial deve ser diferenciada da arrecadação após oposição.

Em uma análise de sensibilidade simples, para taxa de oposição `o`:

`Valor_pos_oposicao = Valor_potencial * (1 - o)`

Essa operação pressupõe, apenas para sensibilidade, que a oposição seja proporcional ao valor potencial. Não é uma estimativa observada de comportamento individual.

## 12. Reprodutibilidade

A rotina `src/estimate.py` implementa os cálculos básicos. Os dados de entrada ficam em `data/raw/`, os resultados em `data/processed/` e as fontes em `data/source_register.csv`.

Qualquer revisão de fonte deve preservar histórico no Git e atualizar o `RESEARCH_LOG.md`.

## 13. Validações obrigatórias antes do artigo

Antes de redigir a versão acadêmica, devem ser verificados:

1. soma dos 27 quantitativos históricos do CONECEF;
2. reconciliação das estimativas estaduais a 84.136;
3. consistência entre cada `source_id` e o registro de fontes;
4. ausência de base sindical estimada sem evidência A ou B, salvo quando explicitamente apresentada como proxy C;
5. sensibilidade aos totais nacionais de 2025 e junho de 2026;
6. sensibilidade aos limites normativos do dissídio e da CCT;
7. impacto de diferentes taxas de oposição;
8. separação entre ativos e aposentados quando a fonte eleitoral misturar os grupos;
9. distinção entre quantitativo de votantes e quantitativo de aptos;
10. linguagem do artigo para não converter potencial de desconto em receita efetiva.
