# CAIXA Contribuição Negocial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir uma base pública, auditável e reprodutível para estimar empregados da CAIXA por UF e por base sindical e calcular intervalos de contribuição negocial de 2026.

**Architecture:** O projeto separa fontes brutas, registro de proveniência, transformações reprodutíveis e resultados processados. Quantitativos diretamente publicados por sindicatos prevalecem sobre proxies; lacunas permanecem explícitas em vez de receber rateios arbitrários.

**Tech Stack:** CSV, Markdown, Python 3 padrão, unittest.

**Spec:** `research/caixa-contribuicao-negocial/SPEC.md`

## Global Constraints

- Usar exclusivamente dados públicos com fonte demonstrável.
- Nunca usar informações internas da CAIXA ou obtidas por acesso funcional.
- Registrar origem, fórmula, hipótese, nível de evidência e limitações de toda estimativa.
- Preservar divergências entre fontes em vez de escolher silenciosamente uma delas.
- Não distribuir resíduos estaduais entre bases sindicais sem regra pública defensável.

## Review Focus

- A soma do rateio estadual deve ser exatamente igual ao total nacional de 84.136.
- A tabela histórica do CONECEF não pode ser rotulada como quadro corrente de 2017 ou 2026.
- Limites da contribuição precisam permanecer cenários separados quando as fontes normativas divergem.
- Bases A/B não podem ser substituídas por proxies C sem sinalização.
- Ausência de dado deve permanecer ausente, não virar zero nem estimativa arbitrária.

---

### Task 1: Registro de fontes e dados brutos

**Files:**
- Create: `research/caixa-contribuicao-negocial/data/source_register.csv`
- Create: `research/caixa-contribuicao-negocial/data/raw/national_totals.csv`
- Create: `research/caixa-contribuicao-negocial/data/raw/uf_conecef_2017.csv`
- Create: `research/caixa-contribuicao-negocial/data/raw/base_counts_2026.csv`
- Create: `research/caixa-contribuicao-negocial/data/raw/contribution_rules.csv`

**Interfaces:**
- Consumes: fontes públicas verificadas.
- Produces: tabelas brutas com `source_id` para as transformações posteriores.

- [ ] Registrar cada fonte pública com URL, data, uso e limitação.
- [ ] Registrar totais nacionais de 2024, 2025 e junho de 2026, distinguindo fonte primária e secundária.
- [ ] Registrar os 27 quantitativos do quadro de representação do 33º CONECEF, totalizando 92.596.
- [ ] Registrar apenas bases sindicais de 2026 cujo denominador esteja publicamente verificável.
- [ ] Registrar separadamente parâmetros do dissídio e referências de CCT/PLR quando divergirem.

### Task 2: Testes das transformações

**Files:**
- Create: `research/caixa-contribuicao-negocial/tests/test_estimates.py`

**Interfaces:**
- Consumes: dados brutos da Task 1.
- Produces: testes para rateio por maiores restos, intervalos de contribuição e preservação de ausências.

- [ ] Escrever teste que exija soma estadual igual a 84.136.
- [ ] Escrever teste que exija total histórico igual a 92.596.
- [ ] Escrever teste dos limites por empregado: R$ 63 a R$ 310 e 70% ao sindicato.
- [ ] Escrever teste para não preencher bases D sem denominador público.
- [ ] Executar os testes antes do código e confirmar falha por ausência da implementação.

### Task 3: Transformações reprodutíveis

**Files:**
- Create: `research/caixa-contribuicao-negocial/src/estimate.py`
- Create: `research/caixa-contribuicao-negocial/data/processed/uf_estimate_2026.csv`
- Create: `research/caixa-contribuicao-negocial/data/processed/base_estimate_2026.csv`

**Interfaces:**
- Consumes: CSVs brutos da Task 1.
- Produces: estimativas estaduais reconciliadas e intervalos para bases com denominador verificável.

- [ ] Implementar método de maiores restos para preservar o total nacional.
- [ ] Calcular pesos históricos sem tratá-los como observações correntes.
- [ ] Calcular intervalos bruto e parcela sindical para remuneração fixa.
- [ ] Manter bases sem denominador público fora da estimativa pontual.
- [ ] Executar testes e confirmar aprovação.

### Task 4: Documentação e auditoria

**Files:**
- Create: `research/caixa-contribuicao-negocial/README.md`
- Create: `research/caixa-contribuicao-negocial/METHODOLOGY.md`
- Create: `research/caixa-contribuicao-negocial/RESEARCH_LOG.md`

**Interfaces:**
- Consumes: dados, regras e resultados anteriores.
- Produces: documentação suficiente para reprodução e futura redação do artigo.

- [ ] Documentar fontes, níveis A-D, fórmulas e conflitos encontrados.
- [ ] Explicar a divergência entre 92.596 do quadro do CONECEF e outros totais históricos publicados para a CAIXA.
- [ ] Listar bases prioritárias ainda sem denominador público: Brasília, Belo Horizonte, Porto Alegre, Curitiba, Recife, Goiânia e outras.
- [ ] Registrar que o artigo só será redigido após validação quantitativa e análise de sensibilidade.
- [ ] Verificar que nenhum arquivo menciona fonte interna ou dado obtido por acesso funcional como evidência.
