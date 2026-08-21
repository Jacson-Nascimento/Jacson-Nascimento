# Auditoria inicial do acervo da dissertação

Data: 21/08/2026

Autor: Jacson Cruz do Nascimento

## 1. Escopo

Esta nota registra a primeira auditoria do material localizado no Google Drive para a dissertação sobre eleições e desempenho bancário. O objetivo é separar versões históricas, identificar a cadeia de dados e scripts efetivamente utilizada e preparar um pipeline reprodutível para artigo científico.

## 2. Versão textual de referência

Foi localizada a pasta `VERSÃO_FINAL_DISSERTAÇÃO`, contendo PDF e DOCX finais. A versão textual de referência é o arquivo:

`Dissertação - Impacto das Eleições Presidenciais na Lucratividade de Bancos Brasileiros - Versão Final - 2024-09-21.pdf`

Para o artigo, versões anteriores serão tratadas como histórico, não como fonte de resultados finais.

## 3. Bases candidatas finais

Foram recuperadas três bases sucessivas da etapa final do projeto:

| Arquivo | Modificação | Linhas | Bancos | Trimestres | Duplicidade banco-data | NA | SHA-256 |
|---|---|---:|---:|---:|---:|---:|---|
| `dataset_290624_11.csv` | 09/07/2024 | 3.072 | 32 | 96 | 0 | 0 | `8f2a06bae81e80a58fe1acadc38fe7982594ca3a489e22cd64ef4bb40d4388e2` |
| `dataset_290624_12.csv` | 20/07/2024 | 3.072 | 32 | 96 | 0 | 0 | `3b45c30d2352f04c3b1c8b070d91678f41964f95e683e615fcf72449f7220a5d` |
| `dataset_290624_13.csv` | 22/07/2024 | 3.072 | 32 | 96 | 0 | 0 | `058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f` |

As três bases possuem exatamente as mesmas chaves `Instituição` e `Data`, o mesmo conjunto de 16 variáveis e o mesmo painel balanceado, de março de 2000 a dezembro de 2023.

## 4. Diferenças entre as versões

A comparação célula a célula mostrou:

- V11 -> V12: apenas `taxa_selic_` foi alterada, em todas as 3.072 observações.
- V12 -> V13: apenas `Taxa_IPCA` foi alterada, em todas as 3.072 observações.
- V11 -> V13: todas as demais variáveis, inclusive ROA, ROE, dummies eleitorais, tipo de controle e indicadores bancários, permanecem idênticas.

### 4.1 IPCA

Na V13, o IPCA foi convertido de percentual para proporção decimal. Exemplo: `0,97` passa a `0,0097`. Trata-se de mudança linear de escala. Ela altera numericamente o coeficiente estimado do IPCA, mas não altera a informação econômica da série nem a estatística t quando a única mudança é a unidade de medida.

### 4.2 Selic

A origem da mudança V11 -> V12 foi localizada. O arquivo final de apoio é:

`TB_selic_4390_acum_mes_trim.xlsx`

Ele utiliza a série 4390, **Taxa de juros - Selic acumulada no mês - % a.m.**, converte cada taxa mensal para decimal e calcula a taxa trimestral por composição:

```text
TaxaTrimestre = (1 + r_mes1) * (1 + r_mes2) * (1 + r_mes3) - 1
```

Exemplo documentado no arquivo para 3T2000:

```text
(1 + 0,0131) * (1 + 0,0141) * (1 + 0,0122) - 1
= 0,039918803462...
```

Esse valor aparece na V12/V13. Portanto, a V12 corrige a operacionalização da Selic para uma taxa trimestral composta compatível com a frequência do painel. A V11 usava outra representação da Selic.

Com isso, a proveniência das duas diferenças materiais entre V11, V12 e V13 está substancialmente esclarecida:

- V12: correção da Selic para taxa trimestral composta;
- V13: padronização do IPCA para proporção decimal.

## 5. Scripts finais localizados

Na pasta `Ajustes p banca defesa 080624/scripts_R` foram localizados, entre outros:

- `if_ols_estatico_2.R`
- `if_ols_dinamico_2.R`
- `if_ols_estatico.R`
- `if_ols_dinamico.R`
- scripts de estatística descritiva
- scripts de testes de raiz unitária
- `.Rhistory` com execução registrada em agosto de 2024

O `.Rhistory` confirma que os scripts `_2` foram efetivamente executados na etapa final de trabalho.

## 6. Achado principal da auditoria

Há uma inconsistência objetiva de versão da base:

- `if_ols_estatico_2.R` lê `dataset_290624_11.csv`.
- `if_ols_dinamico_2.R` lê `dataset_290624_13.csv`.

O arquivo `if_ols_estatico.R`, modificado em 06/08/2024, também aponta para V11.

Portanto, os modelos estático e dinâmico arquivados não partem exatamente da mesma versão das variáveis macroeconômicas.

Isso não significa, por si só, que os resultados centrais estejam errados. Entretanto, impede considerar o pipeline original plenamente reprodutível sem nova execução padronizada.

## 7. Observações sobre o desenho original

### 7.1 Painel balanceado

Os scripts filtram instituições com o número máximo de observações e chegam a 32 bancos com 96 trimestres. Como as bases V11-V13 já possuem 3.072 observações, esse filtro é redundante nessas versões, mas funciona como verificação adicional.

### 7.2 Tipo de controle em efeitos fixos

`dummy_tp` representa característica invariável do banco no período. Em um modelo within com efeito fixo individual, seu efeito principal é absorvido pelo efeito fixo do banco. Interações entre `dummy_tp` e variáveis que mudam no tempo continuam potencialmente identificáveis.

### 7.3 Modelo dinâmico

O script dinâmico inclui `ROA_lag` ou `ROE_lag` em um modelo within. Esse desenho pode apresentar viés de Nickell. Com T=96 o problema é menor que em painéis curtos, mas deve ser tratado explicitamente em um artigo. Uma eventual alternativa GMM precisa ser avaliada com cautela porque N=32 e T=96 não é o ambiente típico em que Arellano-Bond é mais confortável.

### 7.4 Erros-padrão

Os scripts utilizam `vcovHC(..., type = "HC1")`. Para o artigo será necessário documentar claramente o agrupamento e avaliar erros-padrão apropriados para dependência dentro do banco e choques temporais comuns.

## 8. Implicação econométrica para o novo artigo

As dummies de eleição geral e municipal variam apenas no tempo. Por isso, um modelo com efeitos fixos completos de trimestre absorve o efeito principal dessas dummies.

Isso torna frágil interpretar o coeficiente agregado de `dummy_EG` ou `dummy_EM` como efeito eleitoral causal, porque ele pode capturar outros choques nacionais coincidentes com os períodos eleitorais.

Uma estratégia mais defensável é explorar a heterogeneidade entre bancos públicos e privados:

`Election_t × Public_i`

Com efeitos fixos de banco e de trimestre, o componente eleitoral agregado é absorvido, mas a interação permanece identificável. A pergunta passa a ser se bancos públicos mudam seu desempenho de forma diferente dos privados em períodos eleitorais, controlando choques comuns a todos os bancos.

## 9. Reconstrução preliminar dos resultados

Foi feita uma reconstrução independente em Python para verificar a sensibilidade das conclusões antes da reprodução exata em R.

### 9.1 Especificação original aproximada, efeitos fixos de banco

O coeficiente de eleição geral no modelo estático de ROA fica próximo de `0,02838` nas três bases. A estimativa com V12/V13 reproduz, até as casas exibidas, o coeficiente `2,837812e-02` registrado na versão final da dissertação.

Esse ponto cria uma nova pista de proveniência: embora o script estático arquivado aponte para V11, a tabela publicada parece ter sido produzida após a correção macroeconômica ou a partir de uma execução intermediária compatível com V12/V13. A conclusão deve ser confirmada por reprodução em R antes de ser tratada como definitiva.

Nas reconstruções preliminares:

- eleição geral permanece positiva e significativa para ROA na especificação original;
- eleição municipal não apresenta resultado equivalente;
- ROE não apresenta o mesmo padrão consistente;
- as interações simples entre banco público e eleição geral/municipal não se mostram estatisticamente fortes.

### 9.2 Two-way fixed effects, teste de desenho do novo artigo

Foi testado um baseline com efeitos fixos de banco e de trimestre, controles bancários e interações `Public x Eleição Geral` e `Public x Eleição Municipal`, com erros agrupados por banco.

Resultado preliminar:

| Outcome | Interação | Coeficiente | p-valor aproximado |
|---|---|---:|---:|
| ROA | Público x Eleição Geral | -0,00146 | 0,235 |
| ROA | Público x Eleição Municipal | 0,00113 | 0,302 |
| ROE | Público x Eleição Geral | -0,00546 | 0,560 |
| ROE | Público x Eleição Municipal | 0,00429 | 0,575 |

Portanto, a hipótese inicialmente considerada para o novo paper, de uma heterogeneidade simples público x privado nos anos eleitorais, **não recebe apoio preliminar** nessa especificação.

Esse resultado é útil porque evita construir o artigo em torno de uma hipótese que os dados, neste primeiro teste, não sustentam. O desenho do paper deve permanecer aberto até a reprodução completa e o event study.

## 10. Decisão provisória sobre a base

A V13 passa a ser a **candidata preferencial** para a base canônica porque incorpora:

1. Selic trimestral composta a partir da série mensal 4390;
2. IPCA em proporção decimal;
3. o mesmo painel e as mesmas variáveis bancárias das versões anteriores.

Ainda não será declarada definitiva antes de:

1. reproduzir os modelos estático e dinâmico com V11, V12 e V13;
2. comparar coeficientes, erros-padrão e p-valores;
3. reconciliar os outputs com as tabelas da dissertação;
4. identificar a origem do erro de duplicação dos apêndices H/I;
5. definir um script único de preparação da base.

## 11. Próximas entregas

- reprodução exata em R das tabelas principais;
- matriz final de reconciliação `tabela publicada x script x base`;
- base canônica com dicionário de dados;
- script único de preparação;
- event study para investigar timing e pré-tendências;
- teste de alternativas de artigo caso a heterogeneidade público x privado permaneça nula;
- documentação para eventual depósito em Zenodo.
