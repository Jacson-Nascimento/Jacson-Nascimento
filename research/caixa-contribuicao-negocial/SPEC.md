# Especificação do projeto

## Objetivo

Estimar, com dados exclusivamente públicos e metodologia reprodutível, a distribuição territorial dos empregados da Caixa Econômica Federal e a ordem de grandeza da contribuição negocial potencial por base sindical no Brasil, com foco na Campanha Nacional dos Bancários de 2026 e no dissídio coletivo da CAIXA.

## Regra de dados públicos

Este projeto utiliza exclusivamente informações publicamente acessíveis. É vedado incorporar:

- dados internos da CAIXA;
- informações obtidas por acesso funcional, sistemas corporativos ou comunicação restrita;
- listas de empregados, lotações ou remunerações não publicadas;
- qualquer informação cuja publicidade não possa ser demonstrada por URL ou documento público.

Se um dado conhecido por outra via também estiver publicado, somente a versão pública, com sua fonte pública, poderá ser usada.

## Rastreabilidade obrigatória

Todo número utilizado deve ser classificado como observado, inferido ou estimado e possuir, quando aplicável:

1. fonte pública;
2. URL;
3. data da fonte;
4. data de acesso;
5. variável medida;
6. fórmula ou transformação;
7. hipótese adotada;
8. nível de evidência;
9. limitação conhecida.

## Níveis de evidência

- A: quantitativo publicado diretamente para a variável e base territorial analisada.
- B: quantitativo reconstruído matematicamente a partir de informações públicas suficientes, sem hipótese distributiva adicional.
- C: estimativa baseada em proxy territorial, estrutura histórica ou rateio explicitamente documentado.
- D: informação insuficiente para estimativa quantitativa. A base permanece sem valor estimado até haver critério público defensável.

## Padrões metodológicos

- Não atribuir empregados a sindicato apenas por população, número de municípios ou quantidade de agências sem justificativa empírica pública.
- Não tratar a tabela do 33º CONECEF como quadro corrente de empregados. Ela será usada apenas como proxy histórica de estrutura territorial.
- A soma das estimativas por UF deve reconciliar exatamente com o total nacional escolhido, usando método de maiores restos quando necessário.
- Bases sindicais com quantitativo público de aptos em assembleias da CAIXA em 2026 prevalecem sobre proxies estaduais.
- Resíduos de uma UF não serão arbitrariamente rateados entre sindicatos sem fonte pública ou regra empírica documentada.
- Divergências entre fontes serão preservadas no registro de fontes e discutidas, não apagadas.

## Contribuição negocial

O projeto separará cenários normativos quando houver divergência entre valores divulgados para a sentença do TST, ACT e CCT. O cenário principal para a remuneração fixa utilizará os parâmetros publicamente atribuídos ao dissídio da CAIXA: alíquota de 1,5%, mínimo de R$ 63 e máximo de R$ 310, com 70% destinados ao sindicato de base, 15% à federação, 10% à confederação e 5% à central.

Enquanto não houver distribuição pública da base remuneratória individual compatível com a cláusula, não será adotado um valor médio pontual como se fosse observado. Serão reportados intervalos mínimo e máximo por empregado e cenários adicionais claramente identificados.

A incidência sobre PLR será apresentada separadamente e somente com parâmetros cuja fonte pública esteja identificada, sem misturar automaticamente regra de CCT com regra de sentença normativa.

## Produto final

O repositório deverá permitir:

- auditoria das fontes e transformações;
- reprodução das estimativas;
- análise de sensibilidade;
- identificação clara do que é observado e do que é modelado;
- posterior redação de artigo acadêmico com as limitações explicitadas.
