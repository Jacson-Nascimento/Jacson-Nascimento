# Registro Técnico 003 - Resultados do Piloto PNCP 2025

## 1. Objetivo

Documentar os resultados do piloto sentinela do PNCP realizado em 12 datas distribuídas ao longo de 2025, registrar as fragilidades identificadas e formalizar as decisões metodológicas antes da coleta anual.

Este registro é de diagnóstico de dados. Os indicadores de concentração calculados na amostra sentinela não são resultados substantivos do artigo.

## 2. Desenho do piloto

Foram selecionadas 12 quartas-feiras, aproximadamente uma por mês:

- 15/01/2025
- 12/02/2025
- 12/03/2025
- 16/04/2025
- 14/05/2025
- 11/06/2025
- 16/07/2025
- 13/08/2025
- 10/09/2025
- 15/10/2025
- 12/11/2025
- 10/12/2025

Em cada data foram coletadas todas as páginas retornadas pelo endpoint público de contratos e empenhos do PNCP.

O filtro diagnóstico principal reteve registros que satisfaziam simultaneamente:

- esfera municipal;
- Poder Executivo;
- código IBGE da unidade informado;
- fornecedor identificado;
- valor inicial positivo;
- instrumento de despesa.

## 3. Volume observado

A coleta retornou:

- 104.141 instrumentos no universo bruto das 12 datas;
- 12.799 instrumentos municipais válidos após o filtro diagnóstico;
- 12.799 identificadores de instrumento distintos;
- 3.951 identificadores de contratação distintos;
- 5.242 fornecedores distintos;
- 705 municípios de localização das unidades executoras;
- 25 UFs na amostra municipal;
- 1.279 CNPJs distintos de órgãos/entidades nos instrumentos municipais.

Esses números medem o piloto, não o universo anual.

## 4. Completude dos campos essenciais

Nas 104.141 linhas brutas das 12 datas, o diagnóstico por data encontrou:

- 0% de fornecedor ausente;
- 0% de código IBGE ausente;
- proporção de valor inicial nulo ou não positivo entre aproximadamente 0,94% e 3,01%, dependendo da data.

A qualidade sintática das chaves essenciais é, portanto, favorável para a construção do banco. Essa constatação não prova completude institucional ou temporal do PNCP.

## 5. Atraso entre assinatura e publicação

Nos 12.799 instrumentos municipais válidos:

- mediana: 2 dias;
- percentil 75: 20 dias;
- percentil 90: 91 dias;
- percentil 95: 197 dias;
- percentil 99: aproximadamente 365 dias;
- máximo: 862 dias.

Foram observados 128 registros com atraso superior a 365 dias, aproximadamente 1% da amostra válida.

Também foram identificados 5 registros com atraso negativo, isto é, a data de assinatura informada é posterior à data de publicação. Os casos observados incluem Adamantina/SP, Curuçá/PA e Afogados da Ingazeira/PE.

### Decisão

Será criada a variável de qualidade:

`flag_lag_negativo = 1[data_assinatura > data_publicacao]`

Registros com atraso negativo serão preservados na base bruta e excluídos ou tratados separadamente nas análises que dependam da ordem temporal das datas.

O longo rabo direito do atraso confirma que a coleta de contratos assinados em 2025 não pode terminar em 31/12/2025. Será necessária coleta suplementar de publicações de 2026 e posterior filtro pelo ano de assinatura.

## 6. Ano de assinatura dentro das publicações de 2025

Entre os registros municipais válidos das 12 datas:

- assinatura em 2023: 34;
- assinatura em 2024: 638;
- assinatura em 2025: 12.126;
- assinatura em 2026: 1.

Isso confirma que data de publicação e período econômico não são intercambiáveis.

### Regra

A API será percorrida por data de publicação, mas o painel econômico será classificado pela data de assinatura.

## 7. Tipos de instrumento

Distribuição observada:

- Outros: 6.070;
- Contrato, termo inicial: 4.029;
- Empenho: 2.662;
- Termo de Adesão: 26;
- Carta Contrato: 8;
- Comodato: 3;
- Concessão: 1.

A elevada presença de `Outros` e `Empenho` impede somar todos os registros sem classificação prévia.

### Decisão

Antes do cálculo anual serão criados estratos por tipo de instrumento. As métricas principais terão ao menos:

1. todos os instrumentos elegíveis;
2. contratos, termo inicial;
3. empenhos e instrumentos equivalentes em análise de sensibilidade.

A regra final de agregação será determinada após inspeção das duplicidades econômicas e das relações entre contratação e instrumento.

## 8. Multiplicidade de instrumentos por contratação

Nas 3.951 contratações observadas:

- mediana de instrumentos por contratação: 1;
- percentil 75: 1;
- percentil 90: 3;
- percentil 95: 6;
- percentil 99: aproximadamente 39,5;
- máximo: 1.350 instrumentos vinculados à mesma contratação.

Além disso:

- 22,12% das contratações possuíam mais de um instrumento na amostra sentinela;
- 16,40% possuíam mais de um fornecedor;
- o máximo observado foi de 114 fornecedores vinculados a uma contratação.

### Consequência

`numeroControlePncpCompra` não é chave de deduplicação.

A chave do instrumento continua sendo `numeroControlePNCP`. A contratação de origem é uma relação hierárquica que precisa ser preservada.

## 9. Caso extremo e compras compartilhadas

A contratação `12075748000132-1-000133/2024` apresentou 1.350 instrumentos na amostra sentinela, 45 fornecedores e instrumentos associados a dezenas de unidades municipais.

O CNPJ 12.075.748/0001-32 corresponde ao CINCATARINA, consórcio público intermunicipal de Santa Catarina. O caso demonstra que uma contratação centralizada pode gerar instrumentos executados por diversos entes ou unidades.

Esse fenômeno é economicamente legítimo e não deve ser tratado como duplicidade automática.

## 10. Correção da definição de comprador

O piloto mostrou que a localização municipal da unidade executora e a identidade institucional do comprador não são a mesma dimensão.

### Estrutura do PNCP

O instrumento contém um CNPJ de órgão/entidade e uma unidade executora localizada em município específico. A contratação de origem também possui CNPJ próprio em seu número de controle.

### Evidência do piloto

Foram identificados 1.279 CNPJs de órgãos/entidades em 705 municípios de localização.

Em 42,13% dos municípios observados havia mais de um CNPJ contratante. O número de instituições por município teve:

- mediana: 1;
- percentil 75: 2;
- máximo: 25.

Consequentemente, agregar diretamente todos os instrumentos de um município mistura secretarias, fundos, autarquias e outras entidades com decisões de compra potencialmente distintas.

### Decisão metodológica

A unidade compradora principal passa a ser:

`buyer_id = orgao_cnpj`

A rede principal será:

`orgao_cnpj × fornecedor × mercado × ano`

O município será dimensão territorial e fonte de variáveis de controle.

Uma análise municipal agregada poderá ser apresentada como extensão, mas não substituirá a análise institucional.

## 11. CNPJ do contrato versus CNPJ da contratação de origem

A partir dos números de controle foi possível distinguir:

- CNPJ da entidade do instrumento;
- CNPJ da contratação de origem.

Em 6.630 dos 12.799 instrumentos municipais válidos, 51,80%, os dois identificadores eram diferentes.

O percentual é fortemente influenciado por mecanismos de compra compartilhada e pela composição geográfica da amostra sentinela. Em Santa Catarina, por exemplo, a diferença apareceu em parcela muito elevada dos registros devido à presença de estruturas consorciadas.

### Nova variável exploratória

`origem_externa = 1[orgao_cnpj_contrato != orgao_cnpj_compra]`

Também será testada:

`SharedProcurementShare_bct = Valor de instrumentos com origem externa / Valor total do comprador-mercado-ano`

Essa variável poderá controlar o uso de compras compartilhadas. Não será interpretada como fragilidade por si só.

## 12. Categorias do PNCP

Nos registros municipais válidos:

- Compras: 9.636;
- Serviços: 2.285;
- Serviços de Saúde: 577;
- Cessão: 67;
- Obras: 64;
- Serviços de Engenharia: 56;
- Locação de Imóveis: 50;
- Informática, TIC: 46;
- Mão de Obra: 15;
- Internacional: 2;
- Alienação: 1.

### Fragilidade

A categoria `Compras` representa mais de três quartos da amostra e é ampla demais para definir um mercado econômico relevante. Medicamentos, alimentos, material de expediente e veículos não devem competir no mesmo HHI.

### Decisão

`categoriaProcesso` será mantida como classificação de primeiro nível, mas a definição final de mercado deverá utilizar informação mais granular dos itens da contratação quando tecnicamente viável.

O artigo não apresentará HHI de uma categoria excessivamente ampla como se fosse concentração de mercado.

## 13. Composição geográfica da amostra sentinela

A amostra é fortemente desigual:

- Santa Catarina: 6.425 instrumentos, 50,20%;
- Goiás: 2.410, 18,83%;
- São Paulo: 1.539, 12,02%.

A predominância catarinense é associada, em parte, a publicações de compras compartilhadas e em lote.

### Consequência

A amostra de 12 datas é inadequada para estimar a concentração média do Brasil.

Ela é aprovada como teste de API, estrutura, completude e engenharia de dados, mas rejeitada como amostra para inferência econômica.

## 14. Presença nas datas sentinela não é cobertura anual

Dos 705 municípios observados:

- 265 apareceram em apenas uma das 12 datas;
- 209 apareceram em 2 ou 3 datas;
- 86 apareceram em 4 ou 5;
- 88 apareceram em 6 a 8;
- 47 apareceram em 9 a 11;
- 10 apareceram nas 12 datas.

Esse resultado não significa que os demais municípios tenham baixa cobertura do PNCP. Um ente não é obrigado a publicar contratos exatamente nas datas escolhidas.

### Correção conceitual

A variável antes chamada de `coverage_sentinela` passa a ser interpretada apenas como `presenca_sentinela`.

Cobertura anual só será avaliada depois da coleta integral, usando meses ou trimestres com registros, quantidade de instrumentos e comparações com fontes auxiliares.

## 15. Indicadores de concentração calculados no piloto

O pipeline calculou HHI, CR1, CR4, número efetivo de fornecedores, entropia e métricas de exposição de rede sem erro computacional.

Os valores produzidos na amostra sentinela não serão utilizados como evidência do artigo porque:

1. as datas não formam uma amostra probabilística;
2. a composição é dominada por alguns mecanismos de publicação em lote;
3. o comprador inicialmente foi agregado por município;
4. a categoria `Compras` é excessivamente ampla;
5. não há garantia de cobertura anual para cada mercado.

Os arquivos permanecem versionados exclusivamente para auditoria do pipeline.

## 16. Decisão sobre a viabilidade do PNCP

### Resultado

**Aprovado para continuidade, com reespecificação metodológica.**

O PNCP demonstrou:

- volume suficiente;
- campos essenciais disponíveis;
- identificação consistente do fornecedor;
- identificação institucional do comprador;
- vínculo entre instrumento e contratação;
- valores e datas utilizáveis;
- informação suficiente para construir redes comprador-fornecedor.

As principais dificuldades são conceituais e de engenharia de dados, não ausência de dados.

## 17. Próxima coleta

A extração principal será particionada e reiniciável.

### Etapa A

Coletar todas as publicações de 2025, em partições mensais, preservando checkpoints e manifesto de coleta.

### Etapa B

Coletar publicações de 2026 até a data de corte do estudo e reter instrumentos cuja assinatura ocorreu em 2025.

### Etapa C

Classificar instrumentos, retificações, órgãos, unidades e compras compartilhadas.

### Etapa D

Recuperar itens das contratações para refinar a definição de mercado.

### Etapa E

Somente após o banco anual limpo calcular concentração, redes, persistência e choques estruturais.

## 18. Regra de interpretação

Nenhuma medida de concentração, centralidade, compra compartilhada ou persistência será tratada isoladamente como evidência de fraude, direcionamento, favorecimento ou interrupção de serviço.

O objetivo é mensurar estrutura e exposição, com aplicação potencial à priorização de auditoria e análise de risco.
