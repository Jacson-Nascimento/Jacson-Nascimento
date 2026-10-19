# Estrutura da tabela nacional por base sindical

## Objetivo

A tabela nacional é o núcleo empírico do estudo. Sua unidade de observação é a base territorial de representação sindical aplicável aos empregados da Caixa Econômica Federal em 2026.

A tabela não pressupõe que Unidade da Federação e base sindical sejam equivalentes. Quando uma UF contém múltiplas entidades, cada base deve ser tratada separadamente. Quando a entidade possui base estadual, essa condição deve ser documentada em fonte pública.

## Campos mínimos

Cada registro deve conter, sempre que publicamente disponível:

- identificador da base;
- UF;
- entidade sindical;
- delimitação territorial;
- universo mínimo, máximo ou pontual de empregados elegíveis;
- forma de obtenção do universo;
- nível de evidência;
- mecanismo de oposição ou restituição;
- início e fim da janela;
- canal utilizado;
- requisitos formais;
- fonte pública do universo;
- fonte pública do procedimento;
- status da coleta;
- cenários de contribuição e oposição.

## Regras para o universo de empregados

### Contagem direta

Quando a própria entidade publica o número de empregados aptos ou elegíveis, o valor é registrado como ponto observado, com nível P2.

### Reconstrução aritmética

Quando são publicados o número de participantes e a taxa exata de participação, o universo pode ser reconstruído por M1:

`universo_hat = participantes / taxa_participacao`

O arredondamento deve ser compatível com números inteiros e documentado.

### Intervalo

Quando a fonte informa que determinado número representa mais ou menos que certa proporção da base, deve-se registrar somente o intervalo matematicamente compatível. Esse intervalo não é intervalo de confiança.

### Limite inferior

Quando existe apenas a quantidade de votantes ou participantes, sem taxa de participação, esse número é somente limite inferior do universo. Ele não pode ser tratado como total de empregados.

### Sem denominador

Percentuais de aprovação, rejeição ou oposição sem contagem de participantes e sem taxa de participação não permitem reconstruir o universo. O valor permanece ausente.

## Classificação do mecanismo

A variável `mecanismo` distingue procedimentos institucionalmente diferentes:

- `prevent_discount`: manifestação feita antes do processamento do desconto, segundo a regra pública;
- `refund_local_share`: desconto ocorre e a entidade descreve devolução da parcela creditada ao sindicato local;
- `two_stage_prevent_refund`: existem janela preventiva e etapa posterior de restituição;
- `unknown`: a natureza do procedimento não foi suficientemente documentada.

Essas categorias são descritivas. Não implicam, por si, maior ou menor facilidade de exercício do direito.

## Componentes procedimentais

Os componentes são armazenados separadamente, sem produzir nesta fase um índice agregado de fricção:

- formulário eletrônico;
- e-mail;
- entrega presencial;
- correspondência com AR;
- exigência de documento manuscrito;
- assinatura digital ou gov.br;
- reconhecimento de firma;
- prazo disponível;
- quantidade de locais de entrega, quando publicada;
- necessidade de justificativa, quando aplicável.

Um eventual índice de custo procedimental somente poderá ser criado após regra de codificação previamente documentada e análise de sensibilidade. A mera soma de requisitos não será apresentada como medida causal.

## Evidência

- `P1`: fonte pública institucional primária;
- `P2`: publicação pública direta da entidade sindical ou representativa;
- `P3`: fonte pública secundária que reproduz informação institucional;
- `M1`: reconstrução aritmética baseada apenas em números públicos;
- `M2`: estimativa modelada que combina fontes públicas de períodos ou níveis territoriais diferentes.

Resultados derivados devem preservar a classificação da fonte que lhes deu origem e acrescentar a classificação metodológica correspondente.

## Parâmetros financeiros confirmados

A consulta pública ao processo `DCG-1000975-72.2026.5.00.0000` no PJe/TST localizou o acórdão da Seção Especializada em Dissídios Coletivos, julgado em 29/09/2026, documento `26092812223902200000207743324`.

Para a contribuição sobre remuneração fixa, a fonte P1 confirma:

- alíquota de 1,5%;
- mínimo de R$ 63,00;
- máximo de R$ 310,00;
- 70% destinados ao sindicato local;
- 15% à federação;
- 15% à confederação, sendo 10% retidos e 5% repassados à central sindical;
- direito de oposição ao desconto.

A publicação local de Campinas com R$ 65,33/R$ 326,61 permanece registrada somente como divergência documental de fonte P2 e não será utilizada como parâmetro normativo da sentença da CAIXA.

### Regra específica associada à PLR

O valor de 1,5% sobre PLR, sem mínimo e com teto de R$ 262,30 por pagamento, aparece em publicações sindicais, mas ainda não foi localizado em previsão primária incorporada ao projeto. Permanece P2 e não deve ser tratado como definitivo até reconciliação documental.

## Fórmula de sensibilidade

Para universo elegível `E`, contribuição individual `c`, parcela local `s` e taxa hipotética de oposição `o`:

`repasse_potencial = E * c * s`

`repasse_com_oposicao = E * (1 - o) * c * s`

Para a contribuição sobre remuneração fixa, os cálculos usam R$ 63,00 e R$ 310,00 como parâmetros normativos P1.

A taxa de oposição utilizada em cenários é hipotética até que haja dado público observado. Cenários não devem ser apresentados como previsão.

## Ausência de dados

Campos sem evidência pública suficiente permanecem ausentes. É vedado preencher lacunas usando informação obtida por acesso funcional, sistema corporativo, documento restrito, comunicação privada ou conhecimento não reproduzível por terceiros.

## Condição para uso no artigo

A tabela poderá sustentar resultados do artigo somente após:

1. classificação do nível de evidência de todos os parâmetros normativos usados em cada cálculo;
2. confirmação da âncora nacional de empregados em fonte pública primária ou justificativa explícita para manutenção como P3;
3. cobertura adequada das maiores bases sindicais;
4. registro de todas as fontes públicas e datas de acesso;
5. verificação de que os cálculos reproduzem exatamente os parâmetros e universos documentados;
6. apresentação separada de dados observados, intervalos, limites inferiores e estimativas modeladas.
