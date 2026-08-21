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

No IPCA, a V13 corresponde a uma mudança de escala de percentual para proporção decimal. Exemplo: `0,97` passa a `0,0097`. Logo, a transformação é linear e afeta a escala do coeficiente, não o conteúdo informacional da série.

Na Selic, a V12/V13 apresenta uma transformação mais substantiva em relação à V11. A correlação entre as duas séries é muito alta, mas não perfeita, aproximadamente 0,9916. A transformação deve ser documentada a partir do script ou da fonte original antes de definir a base canônica.

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

Portanto, os modelos estático e dinâmico documentados na dissertação não partem exatamente da mesma versão das variáveis macroeconômicas.

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

## 9. Decisão provisória

Nenhuma das três bases será ainda declarada como base definitiva do artigo.

A V13 é a candidata natural por ser a versão mais recente e conter as correções de escala já incorporadas, mas a decisão só será fechada após:

1. localizar a origem e regra de transformação da Selic;
2. reproduzir os modelos estático e dinâmico com V11, V12 e V13;
3. comparar os coeficientes eleitorais e interações;
4. reconciliar os outputs com as tabelas da dissertação;
5. definir um script único de preparação da base.

## 10. Próximas entregas

- matriz de diferenças V11/V12/V13;
- reprodução independente das tabelas principais;
- base canônica com dicionário de dados;
- script único de preparação;
- modelo baseline do artigo;
- event study de heterogeneidade público x privado;
- documentação para eventual depósito em Zenodo.
