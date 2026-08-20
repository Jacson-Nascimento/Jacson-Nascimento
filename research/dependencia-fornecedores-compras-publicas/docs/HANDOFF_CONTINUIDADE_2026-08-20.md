# HANDOFF DE CONTINUIDADE — DEPENDÊNCIA ESTRUTURAL DE FORNECEDORES NAS COMPRAS PÚBLICAS

**Atualizado em:** 20/08/2026  
**Repositório:** `Jacson-Nascimento/Jacson-Nascimento`  
**Diretório do projeto:** `research/dependencia-fornecedores-compras-publicas`

> **REGRA DE CONTINUIDADE:** este arquivo é a fonte de verdade para retomar o projeto em outro diálogo. Antes de alterar metodologia, métricas, chaves, scripts, recorte temporal ou interpretação, ler este handoff e os arquivos aqui referenciados. Não reinventar decisões já validadas.

---

# 1. EXISTEM DUAS TRILHAS E ELAS NÃO DEVEM SER MISTURADAS

## Trilha A — Artigo 1 / primeiro semestre de 2025

Esta é a prioridade do próximo diálogo.

**Branch:** `research/artigo-primeiro-semestre-2025`  
**PR:** **#62 — Atualiza artigo semestral de dependência estrutural para v0.2 robusta**  
**Arquivo editorial principal:** `paper/ARTIGO_PRIMEIRO_SEMESTRE_2025_V0_2.md`  
**Regras editoriais:** `paper/README_V0_2.md`  
**Plano editorial:** `paper/PLANO_EDITORIAL_ARTIGO_SEMESTRAL_E_ANUAL.md`

### Recorte empírico congelado do Artigo 1

- instrumentos **assinados em 2025**;
- observados nas publicações do PNCP entre **01/01/2025 e 30/06/2025**;
- julho em diante NÃO altera retrospectivamente os resultados semestrais;
- publicações tardias de 2026 pertencem à extensão anual, não ao fechamento do Artigo 1.

O novo diálogo deve continuar a **revisão científica, editorial e de publicação do Artigo 1**, usando exclusivamente o recorte semestral acima.

## Trilha B — Extensão anual de 2025

Objetivo: completar instrumentos assinados de **01/01/2025 a 31/12/2025**, coletados pela data de publicação do PNCP, com captura tardia em 2026.

Janeiro–julho já estão consolidados no `main`.

Julho em diante NÃO pertence ao manuscrito semestral. Serve para a futura extensão anual.

---

# 2. TÍTULO E PERGUNTA DO ARTIGO 1

## Título atual em português

**Dependência Estrutural de Fornecedores nas Compras Públicas Municipais: Concentração de Carteira, Exposição em Rede e Vulnerabilidade a Choques Coletivos**

## Título em inglês

**Structural Supplier Dependency in Municipal Public Procurement: Portfolio Concentration, Network Exposure, and Vulnerability to Collective Shocks**

## Pergunta central

> Em que medida a concentração local da carteira captura — ou deixa de capturar — a exposição dos compradores públicos a fornecedores globalmente centrais, e quão persistente e relevante é essa exposição quando conjuntos centrais de fornecedores são removidos da rede observada?

A contribuição deve permanecer **incremental e conservadora**. Não reivindicar novidade no uso isolado de HHI, redes bipartidas, centralidade, recorrência ou simulações de remoção.

Contribuição combinada:

1. concentração monetária da carteira institucional;
2. contraste concentração por valor × concentração por frequência;
3. exposição do comprador à centralidade global de seus fornecedores;
4. choques coletivos direcionados comparados a contrafactuais aleatórios;
5. persistência longitudinal do sinal;
6. integração com controles fiscais municipais;
7. pipeline reproduzível e auditável.

---

# 3. FONTES DE DADOS

## PNCP

Endpoint principal já validado:

`https://pncp.gov.br/api/consulta/v1/contratos`

A coleta é feita por **data de publicação**, mas a classificação econômica usa **data de assinatura**.

Campos estruturais confirmados:

- `numeroControlePNCP` — chave do instrumento;
- `numeroControlePNCPCompra` — vínculo com a contratação;
- `orgaoEntidade.cnpj` — comprador institucional principal;
- `unidadeOrgao.codigoIbge` — município da unidade;
- `niFornecedor` — identificador do fornecedor;
- `tipoPessoa`;
- `valorInicial`;
- `valorGlobal`;
- `dataAssinatura`;
- `dataPublicacaoPncp`;
- `numeroRetificacao`;
- `tipoContrato.nome`;
- `categoriaProcesso.nome`.

## SICONFI / DCA

Usado para controles fiscais municipais.

Integração por `cod_ibge`.

Variáveis principais:

- população;
- despesa empenhada;
- despesa empenhada per capita.

A cobertura na coorte semestral final é aproximadamente **99,18%**.

## IBGE

Usado para universo territorial e mapeamento UF/região.

Universo municipal estrito adotado: **5.569 municípios**.

O endpoint de localidades retorna 5.571 registros; para o denominador municipal estrito foram excluídos:

- Distrito Federal;
- Distrito Estadual de Fernando de Noronha.

Presença territorial deve ser chamada de **presença/continuidade observacional**, nunca de “completude de reporte”.

---

# 4. CHAVES E UNIDADES — DECISÕES CONGELADAS

## Chave do instrumento

`numeroControlePNCP`

### NÃO deduplicar por `numeroControlePNCPCompra`

Uma mesma contratação pode gerar vários instrumentos e vários fornecedores. Deduplicar pela compra destruiria informação econômica válida.

## Comprador

O nó comprador principal é o **CNPJ institucional do órgão/entidade contratante**.

Não redefinir o comprador como município.

Motivo: consórcios e instituições multi-municipais podem gerar instrumentos em várias unidades/municípios.

## Município

É dimensão territorial e chave de integração com SICONFI/IBGE, não o nó comprador principal.

## Compra compartilhada / origem externa

Indicador já utilizado:

`origem_externa = orgao_cnpj != orgao_compra_cnpj`

A robustez mostrou que **Strength** é bastante estável à exclusão de origem externa. Degree é mais sensível.

---

# 5. GOVERNANÇA, PRIVACIDADE E PUBLICAÇÃO DE DADOS

O repositório é público.

Regra vigente:

- base pública identificada no GitHub: fornecedores **PJ**;
- PF/PE permanecem apenas em diagnósticos agregados e/ou cópia privada;
- não republicar CPF e nome de fornecedor pessoa física no GitHub;
- identificadores tratados como texto;
- preservar hashes SHA-256 dos arquivos mensais e partições;
- não deduplicar silenciosamente.

---

# 6. DEFINIÇÃO ECONÔMICA — NÃO CHAMAR DE “MERCADO”

Os testes de itens mostraram que os campos de classificação do PNCP não possuem granularidade uniforme suficiente para sustentar uma definição confiável de mercado relevante.

Portanto, a métrica principal é:

**concentração da carteira de fornecedores do comprador**,

não concentração de mercado.

Não interpretar a categoria ampla `Compras` como mercado econômico.

---

# 7. MÉTRICAS PRINCIPAIS

Para comprador `b`, fornecedor `s` e janela `t`:

`V_bst` = valor agregado da relação comprador–fornecedor.

`V_bt = sum_s V_bst`

`q_bst = V_bst / V_bt`

## HHI monetário da carteira

`PortfolioHHI_bt = sum_s q_bst^2`

## HHI normalizado

`HHI_norm = (HHI - 1/N) / (1 - 1/N)` para `N > 1`.

O HHI normalizado é obrigatório como complemento porque o HHI bruto depende mecanicamente do número de fornecedores.

## CR1

Maior participação monetária individual.

## CR4

Soma das quatro maiores participações.

## Número efetivo de fornecedores

`N_eff = 1 / HHI`

## CountHHI

Concentração pela frequência de instrumentos, não pelo valor.

A divergência `PortfolioHHI > CountHHI` é resultado central.

---

# 8. REDE E EXPOSIÇÃO ESTRUTURAL

Rede bipartida comprador–fornecedor, ponderada por valor.

## Degree global

Número de compradores distintos ligados ao fornecedor.

## Strength global

Valor total das relações do fornecedor na rede.

## Especificação principal

**Strength global** = principal para vulnerabilidade/choques.

**Degree global** = complementar/robustez.

Motivo: Strength mostrou maior robustez a compras compartilhadas/origem externa.

## Exposição estrutural do comprador

Média ponderada da centralidade global dos fornecedores pela participação monetária deles na carteira do comprador.

## Exposição estrutural oculta

Comprador com HHI local abaixo do quartil superior e exposição Strength acima do quartil superior.

Usar como **sinal de screening**, não como índice proprietário nem rótulo permanente.

---

# 9. SIMULAÇÕES DE CHOQUE

Remover da rede:

- 1% dos fornecedores;
- 5%;
- 10%.

Comparar:

- remoção direcionada por Strength global — principal;
- Degree global — complementar;
- 1.000 remoções aleatórias de mesmo tamanho;
- semente fixa `20260818`.

Para conjunto removido `R`:

`Loss_b(R) = sum_{s in R} q_bs`

Limiares monitorados:

- 25%;
- 50%;
- 75%.

Termos adequados:

- vulnerabilidade estrutural;
- exposição estrutural.

Não dizer que a simulação representa falência, sanção ou interrupção real. É uma simulação estática da carteira observada.

---

# 10. ELEGIBILIDADE E ROBUSTEZ

Amostra principal:

- pelo menos 3 fornecedores;
- pelo menos 5 instrumentos.

Robustez:

- 3/5;
- 5/10;
- 5/20;
- 10/20.

Não tratar 3/5 como parâmetro “natural”. O nível absoluto do HHI varia com o tamanho mínimo da carteira; a divergência valor–frequência e a exposição oculta são muito mais estáveis.

---

# 11. RESULTADOS CONGELADOS DO ARTIGO 1 — JAN–JUN/2025

## Recorte

- publicações PNCP: **01/01/2025 a 30/06/2025**;
- instrumentos economicamente considerados: assinados em 2025;
- base pública identificada: fornecedores PJ.

## Números reportados na v0.2

- **105.582 instrumentos PJ** na base semestral;
- **98.438 assinados em 2025**;
- métricas para **2.349 compradores institucionais**;
- amostra principal: **1.347 compradores elegíveis**;
- rede global: aproximadamente **20.367 fornecedores**.

## Resultados principais

- HHI monetário mediano: **0,2365**;
- HHI normalizado mediano: **0,1563**;
- número efetivo mediano de fornecedores: **4,23**;
- concentração por valor > concentração por frequência em **98,14%** dos compradores;
- Spearman HHI normalizado × exposição Strength global: **0,4081**;
- exposição estrutural oculta: **13,14%**;
- remoção direcionada dos 10% fornecedores de maior Strength: **48,26%** dos compradores com perda ≥50% da carteira;
- remoção aleatória equivalente: **4,08%**;
- retenção no quartil superior da exposição Strength de maio para junho: **90,76%**;
- cobertura de despesa empenhada PNCP–SICONFI: **99,18%**.

**Esses números ficam congelados no Artigo 1.**

Segundo semestre não deve substituí-los.

---

# 12. ACHADOS INTERPRETATIVOS JÁ VALIDADOS

1. **Diversificação nominal não equivale a diversificação econômica.**
2. **Concentração local e exposição estrutural são dimensões diferentes.**
3. **A vulnerabilidade é coletiva, não dominada por um único “superfornecedor”.**
4. **Strength global é a medida principal de choque.**
5. **O ranking de exposição é temporalmente persistente.**
6. **Entrada de novos fornecedores explica grande parte da queda do HHI bruto.**
7. **Novos elegíveis tendem a entrar mais concentrados que incumbentes.**
8. **Lags negativos são raros e não alteram materialmente os resultados.**
9. **`valorInicial` permanece principal; `valorGlobal` é robustez.**
10. **Empenhos afetam mais frequência que valor e não dirigem os resultados monetários.**
11. **Compras compartilhadas não explicam o resultado principal por Strength.**

---

# 13. MODELOS ASSOCIATIVOS PNCP–SICONFI

Natureza: **associativa/descritiva, não causal**.

Especificação vigente:

- resposta principal: HHI normalizado;
- controles externos: log população + log despesa empenhada per capita;
- controles de carteira: log número de fornecedores + log instrumentos por fornecedor;
- efeitos de macrorregião;
- erros-padrão agrupados por município;
- fractional logit como robustez funcional.

A parametrização inicial com população e despesa total causou multicolinearidade forte e foi substituída por população + despesa per capita.

Após reparametrização, VIFs ficaram baixos, aproximadamente 1,1–1,6.

Padrões semestrais:

- população → HHI normalizado: positiva e persistente;
- número de fornecedores → HHI normalizado: negativa e muito persistente;
- despesa per capita: não robusta;
- recorrência → HHI: frágil/inconsistente;
- recorrência → exposição Strength: positiva e consistentemente significativa.

Não transformar significância isolada em narrativa causal.

---

# 14. PRESENÇA TERRITORIAL

A PR **#54 foi concluída e incorporada ao `main`**.

Universo estrito: **5.569 municípios**.

Até junho:

- municípios observados ao menos uma vez: **1.031**;
- presença observacional ao menos uma vez: aproximadamente **18,51%**;
- 708 municípios observados em pelo menos metade dos seis meses;
- 300 observados em todos os seis meses.

Não chamar a coorte semestral de “representativa de todos os municípios brasileiros”.

Formulação adequada:

**compradores municipais observados no PNCP na janela analisada**.

Ausência de município em um mês não prova falha de reporte.

---

# 15. ARTIGO 1 — ESTADO EDITORIAL ATUAL

## PR atual

**#62 — Atualiza artigo semestral de dependência estrutural para v0.2 robusta**

Branch:

`research/artigo-primeiro-semestre-2025`

Referência editorial:

`research/dependencia-fornecedores-compras-publicas/paper/ARTIGO_PRIMEIRO_SEMESTRE_2025_V0_2.md`

Arquivo auxiliar:

`paper/README_V0_2.md`

Plano editorial:

`paper/PLANO_EDITORIAL_ARTIGO_SEMESTRAL_E_ANUAL.md`

A v0.2 já contém:

- resumo;
- abstract;
- introdução;
- fundamentação teórica;
- organização industrial;
- procurement;
- redes e robustez;
- metodologia;
- resultados;
- robustez e verificações de qualidade;
- contribuição;
- limitações;
- agenda de pesquisas futuras;
- referências;
- versão diagramada Word/Google Docs com **6 tabelas e 5 figuras/gráficos**.

Regras editoriais:

- primeira ocorrência de sigla: nome por extenso + sigla;
- siglas centrais também expandidas no abstract;
- contribuição formulada de maneira conservadora;
- HHI definido como concentração de carteira, não mercado;
- ausência de causalidade explicitada;
- choque explicitamente estático/estrutural;
- resultados semestrais separados da extensão anual.

Literatura mainstream incorporada:

- Bandiera, Prat & Valletti — AER, 2009;
- Decarolis — AEJ: Applied Economics, 2014;
- Lewis-Faupel et al. — AEJ: Economic Policy, 2016;
- Coviello, Guglielmo & Spagnolo — Management Science, 2018;
- Bosio et al. — AER, 2022.

Referências teóricas canônicas de apoio:

- Tirole;
- Laffont & Tirole;
- Dimitri, Piga & Spagnolo;
- Jackson;
- Newman;
- Freeman;
- Albert, Jeong & Barabási.

---

# 16. SCRIPTS CENTRAIS — NÃO REINVENTAR

Diretório:

`research/dependencia-fornecedores-compras-publicas/scripts/`

## Coleta PNCP

`coletar_pncp_periodo.py`

## Consolidação mensal

`consolidar_mes_pncp_2025.py`

Valida:

- unicidade de `id_contrato`;
- datas parseáveis;
- janela semiaberta do mês;
- hashes;
- ausência de deduplicação silenciosa.

## Acumulador global

`analisar_acumulado_2025_global.py`

Calcula:

- PortfolioHHI;
- HHI normalizado;
- CountHHI;
- CR1/CR4;
- N_eff;
- rede global;
- Strength/Degree;
- exposição estrutural;
- choques direcionados/aleatórios;
- sensibilidade de elegibilidade.

## Diagnóstico longitudinal genérico

`diagnosticos_longitudinais_generico.py`

Usar parâmetros de mês inicial/final. Não criar script novo para cada par de meses.

## Modelos PNCP–SICONFI genéricos

`modelos_associativos_pncp_siconfi_generico.py`

Usar `--month` e `--compare-month`.

## SICONFI / DCA

`coletar_siconfi_dca.py`

A integração fiscal mensal foi generalizada pelas PRs **#57/#58**. Reutilizar cache e consultar somente municípios novos.

## Cobertura territorial

`diagnostico_cobertura_territorial_pncp.py`

Universo estrito: 5.569 municípios.

Scripts históricos específicos de meses devem ser preservados para auditoria, mas não são o padrão operacional atual.

---

# 17. EXTENSÃO ANUAL — ESTADO ATUAL EM 20/08/2026

## Janeiro–julho

Consolidado e incorporado ao `main`.

Fechamento jan–jul:

- **128.444 instrumentos PJ** acumulados;
- **120.609 assinados em 2025**;
- **2.517 compradores** com métricas;
- **1.500 compradores elegíveis 3/5**;
- **24.160 fornecedores** na rede global;
- HHI mediano **0,2346**;
- HHI normalizado **0,1546**;
- exposição estrutural oculta **14,13%**;
- choque Strength 10%: **47,73%** severos contra **3,96%** aleatório médio.

Esses números são da extensão anual e NÃO entram no artigo semestral v0.2.

## Rotina agosto–dezembro

Há duas camadas já estruturadas:

### Rotina genérica incorporada ao main

PR **#55 — Generaliza coleta e tratamento PNCP para agosto–dezembro de 2025** — **MERGED**.

### Integração fiscal/modelos genéricos

PR **#57** — SICONFI/modelos mensais genéricos — **MERGED**.

PR **#58** — integração SICONFI até julho — **MERGED**.

### Diagnóstico territorial mensal

PR **#59** — inclui diagnóstico territorial na rotina mensal — **MERGED**.

### PR operacional adicional

PR **#60 — Cria rotina genérica PNCP para agosto-dezembro de 2025**

Branch:

`research/pncp-restante-2025-rotina`

Estado em 20/08/2026: **aberta, draft, mergeável**.

Não reinventar outra rotina; partir dela ou do workflow genérico já incorporado ao `main`.

---

# 18. AGOSTO — ESTADO EXATO EM 20/08/2026

PR de execução:

**#56 — Coleta PNCP agosto de 2025 pela rotina mensal genérica**

Branch:

`research/pncp-2025-08`

Checkpoints atualmente confirmados/commitados:

| Janela | PJ |
|---|---:|
| 01–04/08 | 1.833 |
| 05–08/08 | 3.581 |
| 09–12/08 | 2.066 |
| 13–16/08 | 3.245 |
| 17–20/08 | 2.580 |

Total PJ 01–20/08: **13.305**.

O bloco 17–20/08 está confirmado na branch; qualquer registro anterior dizendo que esse bloco havia falhado está **superado**.

Não coletar datas futuras como se fossem completas. Em 20/08/2026, o próximo bloco 21–24/08 só deve ser consolidado quando a janela correspondente estiver disponível.

---

# 19. GOOGLE DRIVE

Pasta do projeto:

**ARTIGO - Dependencia de Fornecedores e Compras Publicas**

Estrutura:

- `01_Dados`
- `02_Scripts`
- `03_Documentacao_Tecnica`
- `04_Resultados`
- `05_Artigo`
- `06_Referencias`

Regra:

- GitHub: código, bases públicas minimizadas, resultados reproduzíveis e documentação técnica versionável;
- Drive: documentação, versões editoriais, arquivos de suporte, cópias privadas e materiais de trabalho.

---

# 20. O QUE FAZER NO NOVO DIÁLOGO — PRIORIDADE ARTIGO 1

O próximo diálogo deve começar pela **Trilha A / Artigo 1**, salvo ordem expressa em contrário.

Sequência recomendada:

1. abrir este handoff integralmente;
2. abrir a PR #62;
3. ler integralmente `ARTIGO_PRIMEIRO_SEMESTRE_2025_V0_2.md`;
4. ler `README_V0_2.md`;
5. ler `PLANO_EDITORIAL_ARTIGO_SEMESTRAL_E_ANUAL.md`;
6. revisar criticamente a v0.2 como artigo científico independente;
7. verificar coerência entre resumo, tabelas, figuras, resultados, metodologia e limitações;
8. revisar referências e links/DOIs;
9. revisar siglas;
10. checar se todos os números do texto vêm exclusivamente do recorte jan–jun;
11. impedir contaminação por julho/agosto;
12. definir ajustes para v0.3 ou versão de preprint;
13. quando aprovado, preparar pacote Word/PDF/Zenodo e divulgação.

---

# 21. PROIBIÇÕES DE CONTINUIDADE

No novo diálogo, NÃO:

- redefinir comprador como município;
- deduplicar por `numeroControlePNCPCompra`;
- chamar HHI de concentração de mercado;
- substituir Strength por Degree como principal sem novo teste;
- inventar índice composto sem necessidade;
- interpretar simulação como falência real;
- alegar causalidade nos modelos associativos;
- publicar CPF/nome de fornecedor PF no GitHub;
- alterar o recorte semestral com dados de julho–dezembro;
- usar baixa presença territorial como prova automática de descumprimento do PNCP;
- criar scripts mensais duplicados quando já existe módulo genérico.

---

# 22. PROMPT OPERACIONAL PARA O PRÓXIMO CHAT

Copiar e colar integralmente:

> CONTINUE O PROJETO “DEPENDÊNCIA ESTRUTURAL DE FORNECEDORES NAS COMPRAS PÚBLICAS”.
>
> Primeiro, abra e leia integralmente no GitHub:
>
> `research/dependencia-fornecedores-compras-publicas/docs/HANDOFF_CONTINUIDADE_2026-08-20.md`
>
> Repositório: `Jacson-Nascimento/Jacson-Nascimento`.
>
> Esse arquivo é a fonte de verdade para a continuidade. Não reinvente metodologia, métricas, chaves, scripts, recorte temporal ou decisões já validadas.
>
> PRIORIDADE DESTE NOVO DIÁLOGO: continuar o **Artigo 1 — primeiro semestre de 2025**, atualmente na PR #62, branch `research/artigo-primeiro-semestre-2025`, arquivo `research/dependencia-fornecedores-compras-publicas/paper/ARTIGO_PRIMEIRO_SEMESTRE_2025_V0_2.md`.
>
> O recorte do Artigo 1 é CONGELADO: instrumentos assinados em 2025 e observados nas publicações PNCP de 01/01/2025 a 30/06/2025. Julho em diante pertence à extensão anual e não deve alterar os resultados do manuscrito semestral.
>
> Abra também `paper/README_V0_2.md` e `paper/PLANO_EDITORIAL_ARTIGO_SEMESTRAL_E_ANUAL.md`.
>
> Depois faça uma revisão crítica completa da v0.2 e continue a produção editorial/científica a partir do ponto exato documentado. Salve alterações técnicas no GitHub e materiais editoriais/de suporte na pasta dedicada do Google Drive. Não peça que eu repita contexto já registrado no handoff.

---

# 23. PRINCÍPIO FINAL

**Artigo semestral = evidência congelada até 30/06/2025.**  
**Extensão anual = julho–dezembro + captura tardia em 2026.**

A arquitetura empírica é a mesma, mas os dois produtos têm objetivos editoriais e recortes temporais distintos. Preservar essa separação é requisito de validade e reprodutibilidade.
