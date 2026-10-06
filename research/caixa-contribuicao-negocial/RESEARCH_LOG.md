# Research log

## 2026-10-06 - abertura do projeto

### Escopo definido

Objetivo inicial: estimar a distribuição dos empregados da CAIXA por UF e por base sindical e calcular a ordem de grandeza da contribuição negocial decorrente do dissídio coletivo de 2026.

Regra vinculante: somente dados públicos. Informações internas da CAIXA ou obtidas por acesso funcional estão excluídas, ainda que possam confirmar um dado público.

### Decisão 1 - separar dado observado de estimativa

Foi adotada classificação A-D de evidência.

Motivo: as fontes públicas disponíveis misturam quantitativos diretamente divulgados, percentuais de assembleias, proxies históricas e lacunas. Sem classificação, uma tabela única produziria falsa aparência de precisão.

### Decisão 2 - não tratar 92.596 como estoque oficial de 2017

O quadro de representação do 33º CONECEF soma 92.596 empregados por UF. O Relatório de Sustentabilidade CAIXA 2017 informa 87.654 empregados no fechamento de 2017.

Diferença: 4.942 empregados, aproximadamente 5,64% do total oficial de fechamento.

Tratamento: a tabela do CONECEF é usada somente como proxy dos pesos territoriais históricos e recebe evidência C.

### Decisão 3 - reconciliar a proxy estadual ao total contemporâneo

Foi escolhido o total público de 84.136 empregados em junho de 2026 para a primeira modelagem.

Os pesos históricos são aplicados a esse total e arredondados pelo método de maiores restos. A soma das 27 UFs deve permanecer exatamente 84.136.

### Decisão 4 - retirar a contribuição média pontual da conclusão principal

Uma versão preliminar da análise utilizava contribuição média estimada a partir de remuneração média agregada.

Esse caminho foi descartado como estimativa central porque a cláusula incide sobre uma base remuneratória específica e possui piso e teto. A remuneração média contábil da empresa não identifica a distribuição da base individual da cláusula.

Novo tratamento: apresentar intervalo normativo entre R$ 63 e R$ 310 por empregado, com análise de cenários adicionais apenas quando explicitamente identificados.

### Decisão 5 - separar sentença da CAIXA e referência da CCT

Foram localizadas fontes públicas com valores distintos:

- cenário atribuído à sentença do dissídio: piso R$ 63,00 e teto R$ 310,00;
- referência divulgada da CCT: piso R$ 62,46 e teto R$ 312,25.

Os cenários permanecem separados. O dissídio da CAIXA é a referência principal do estudo.

### Decisão 6 - não converter UF em sindicato automaticamente

O quantitativo estimado para uma UF não será atribuído ao principal sindicato daquele estado.

Exemplo: a proxy estadual do DF não será tratada como quantitativo observado do Sindicato dos Bancários de Brasília sem fonte pública específica da base sindical.

### Bases com denominador público incorporadas nesta rodada

- São Paulo, Osasco e Região: aproximadamente 11.000.
- SBBA/Bahia: 1.881 aptos.
- Irecê e Região: 58 aptos.
- Juiz de Fora e Região: 516 aptos.
- Londrina e Região: 457 aptos.
- Patos de Minas e Região: 132 aptos.
- Criciúma e Região: 206 reconstruídos a partir da própria publicação, com inconsistência textual registrada.
- Campina Grande e Região: aproximadamente 198 reconstruídos de 180 votantes e 90,91% de participação.
- Pelotas e Região: aproximadamente 230 empregados atuando na base, segundo fonte pública secundária.

### Evidências mantidas como não resolvidas

- Brasília: percentual de votação conhecido, denominador não publicado na fonte localizada.
- Rio de Janeiro: 2.711 participantes representaram mais de 78% da base, mas a taxa exata não foi divulgada e não há denominador pontual defensável.
- Belo Horizonte e Região: percentual de votação conhecido, denominador não localizado.
- Curitiba e Região: assembleia localizada, denominador não localizado.
- Porto Alegre e Região: resultado localizado em fontes nacionais, denominador não localizado.
- Pernambuco: resultado percentual localizado, denominador não localizado.
- Goiás: edital localizado, denominador não localizado.
- FEEB-PR: percentuais agregados de nove sindicatos, sem contagem de votos ou aptos.
- Joinville: 266 participantes publicados, mas sem total de aptos.

### Resultado nacional provisório da contribuição salarial

Com 84.136 empregados e limites de R$ 63 e R$ 310:

- contribuição bruta mínima teórica: R$ 5.300.568,00;
- contribuição bruta máxima teórica: R$ 26.082.160,00;
- 70% destinados aos sindicatos: R$ 3.710.397,60 a R$ 18.257.512,00.

Esses valores não incorporam oposição e não são apresentados como receita efetiva.

### Próximos controles

1. ampliar denominadores públicos por base sindical;
2. validar o total de junho de 2026 em fonte primária, se disponível;
3. executar testes automatizados e comparar os CSVs processados com a rotina;
4. produzir análise de sensibilidade com total de 2025;
5. estimar cobertura da amostra de bases A/B sobre o quadro nacional;
6. somente depois discutir desenho e redação do artigo.
