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

## Parâmetros financeiros e conflitos normativos

Parâmetros normativos não serão escolhidos silenciosamente quando fontes públicas divergirem.

Na coleta de 06/10/2026 foram identificadas, entre outras, duas reproduções públicas distintas para limites da contribuição sobre remuneração fixa:

- cenário A: 1,5%, mínimo de R$ 63,00 e máximo de R$ 310,00;
- cenário B: 1,5%, mínimo de R$ 65,33 e máximo de R$ 326,61.

Enquanto o texto final primário da decisão do TST não for incorporado ao projeto, os dois conjuntos permanecem registrados como cenários de reconciliação documental, e não como parâmetros definitivos do artigo.

A estrutura de rateio de 70% para o sindicato local, 15% para federação e 15% restantes para confederação e central aparece de modo consistente nas fontes públicas consultadas. Algumas entidades detalham os 15% finais em 10% para confederação e 5% para central. Essa compatibilidade deve ser confirmada na fonte normativa primária antes da redação final.

## Fórmula de sensibilidade

Para universo elegível `E`, contribuição individual `c`, parcela local `s` e taxa hipotética de oposição `o`:

`repasse_potencial = E * c * s`

`repasse_com_oposicao = E * (1 - o) * c * s`

A taxa de oposição utilizada em cenários é hipotética até que haja dado público observado. Cenários não devem ser apresentados como previsão.

## Ausência de dados

Campos sem evidência pública suficiente permanecem ausentes. É vedado preencher lacunas usando informação obtida por acesso funcional, sistema corporativo, documento restrito, comunicação privada ou conhecimento não reproduzível por terceiros.

## Condição para uso no artigo

A tabela poderá sustentar resultados do artigo somente após:

1. reconciliação dos parâmetros normativos com fonte primária ou conjunto documental público suficientemente forte;
2. confirmação da âncora nacional de empregados em fonte pública primária ou justificativa explícita para manutenção como P3;
3. cobertura adequada das maiores bases sindicais;
4. registro de todas as fontes públicas e datas de acesso;
5. verificação de que os cálculos reproduzem exatamente os parâmetros e universos documentados;
6. apresentação separada de dados observados, intervalos, limites inferiores e estimativas modeladas.
