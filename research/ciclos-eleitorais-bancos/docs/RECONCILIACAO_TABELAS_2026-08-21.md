# Reconciliação das tabelas da dissertação com as bases V11, V12 e V13

Data: 21/08/2026

Status: auditoria de reprodutibilidade concluída para as estimações principais dos Apêndices D a K.

## 1. Objetivo

Identificar qual versão da base gerou efetivamente as tabelas publicadas na versão final da dissertação e localizar inconsistências de transcrição, amostra e definição de variáveis.

Fonte textual de referência:

`Dissertação - Impacto das Eleições Presidenciais na Lucratividade de Bancos Brasileiros - Versão Final - 2024-09-21.pdf`

Bases comparadas:

- V11: `dataset_290624_11.csv`
- V12: `dataset_290624_12.csv`
- V13: `dataset_290624_13.csv`

A reprodução foi feita por transformação within por banco e matriz de covariância equivalente a `vcovHC(..., type = "HC1")` do `plm`, com agrupamento por banco. Os graus de liberdade foram calculados como `N - n_bancos - k`.

## 2. Resultado central da reconciliação

Os Apêndices D, E, F, G, J e K são reproduzidos pela **V13** até o limite de arredondamento exibido no PDF.

| Apêndice | Modelo publicado | Resultado da auditoria |
|---|---|---|
| D | ROA estático, 2000-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |
| E | ROE estático, 2000-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |
| F | ROA dinâmico, 2000-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |
| G | ROE dinâmico, 2000-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |
| H | ROA estático, 2012-2023 | **não contém ROA; é cópia do ROE** |
| I | ROE estático, 2012-2023 | V13 reproduz corretamente o ROE |
| J | ROA dinâmico, 2012-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |
| K | ROE dinâmico, 2012-2023 | V13 reproduz coeficientes, erros-padrão, t e p-valores |

Portanto, a base que efetivamente sustenta as tabelas finais é a V13, embora os scripts estáticos arquivados ainda apontem para V11.

## 3. Evidência de que a tabela estática final veio da V13

No Apêndice D, o coeficiente publicado de `dummy_EG` para ROA é:

`2.837812e-02`

A reprodução fornece:

- V11: `0.0283695865`
- V12: `0.0283781177`
- V13: `0.0283781177`

Esse coeficiente isolado não distingue V12 de V13. Entretanto, o coeficiente publicado do IPCA é:

`1.275683e-02`

A reprodução fornece:

- V12: `0.0001275683`
- V13: `0.0127568313`

Logo, o conjunto completo da tabela identifica inequivocamente a V13 como base final.

O mesmo padrão ocorre nos demais modelos: V12 e V13 diferem apenas pela escala do IPCA, e os coeficientes publicados do IPCA estão na escala da V13.

## 4. Apêndice H é uma duplicação do ROE

O Apêndice H está rotulado como:

`Modelo Estático - ROA - 2012-2023`

O Apêndice I está rotulado como:

`Modelo Estático - ROE - 2012-2023`

Os dois apêndices apresentam valores idênticos em todas as linhas, inclusive:

- coeficientes;
- erros-padrão;
- estatísticas t;
- p-valores;
- Total Sum of Squares;
- Residual Sum of Squares;
- R²;
- R² ajustado;
- estatística F.

A reprodução mostrou que esses valores são exatamente os do **ROE estático de 2012-2023 com V13**.

Exemplos:

- `deg = 0.0728247002`
- `dpcdl:dtc = -3.321536788`
- `spread:dtc = 1.090554552`
- `R² = 0.1541424`
- `Total Sum of Squares = 7.938726`

Portanto, o erro não é econométrico. É um erro de montagem/transcrição do documento: o output de ROE foi inserido também no Apêndice H.

O verdadeiro output estático de ROA para 2012-2023 foi reconstruído e está salvo em:

`results/auditoria/modelo_estatico_roa_2012_2023_corrigido.csv`

## 5. Número de observações dos modelos dinâmicos

Os scripts criam `N` antes de gerar a defasagem da variável dependente e antes de executar `na.omit()`.

Por isso, os cabeçalhos e tabelas informam incorretamente:

- 2000-2023: `N = 3072`
- 2012-2023: `N = 1536`

A amostra efetivamente usada nas regressões dinâmicas é:

- 2000-2023: **3040 observações**, 32 bancos x 95 trimestres úteis;
- 2012-2023: **1504 observações**, 32 bancos x 47 trimestres úteis.

Os próprios graus de liberdade publicados confirmam isso:

- período completo: `2986 = 3040 - 32 - 22`;
- período 2012-2023: `1450 = 1504 - 32 - 22`.

Assim, os coeficientes dinâmicos estão reproduzidos, mas a linha `Observations` das Tabelas 8 e 9 e os cabeçalhos dos Apêndices F, G, J e K foram preenchidos com a contagem pré-defasagem.

## 6. Nova inconsistência identificada no ROA

Foi recuperada a base anterior `dataset_2024_3.csv`, utilizada na fase inicial do projeto. Para 2.852 observações banco-trimestre comuns entre essa base e a V13, cobrindo 31 bancos de 2000 a 2022, verificou-se exatamente:

`ROA_V13 = 1 + ROA_antigo`

Erro numérico máximo observado nessa identidade: aproximadamente `4,44e-16`.

Ao mesmo tempo:

`ROE_V13 = ROE_antigo`

sem diferença nas observações comuns.

A dissertação define conceitualmente ROA como:

`Lucro Líquido / Ativo Total`

mas a estatística descritiva da versão final apresenta média de ROA próxima de `1,0049`, compatível com a transformação `1 + ROA`, não com o indicador definido no texto.

### Consequência econométrica

A soma de uma constante igual a 1 ao ROA **não altera** os coeficientes dos modelos within de efeitos fixos, porque a transformação within remove constantes específicas do nível da variável. O mesmo vale para o modelo com `ROA_lag`, pois o deslocamento constante também desaparece após a transformação within.

Portanto:

- os coeficientes reproduzidos não são invalidados por esse deslocamento;
- as estatísticas descritivas de nível do ROA ficam incorretamente apresentadas;
- a interpretação literal da variável como `Lucro Líquido / Ativo Total` exige retirar o `+1`;
- o novo artigo deverá usar `ROA_limpo = ROA_V13 - 1`.

Para preservar rastreabilidade, a base V13 deve ser mantida como **base arquivística de reprodução**, enquanto uma base canônica limpa será derivada por script.

## 7. Erro de interpretação de notação científica

No texto da dissertação, o coeficiente `2,837812e-02` é descrito em passagem narrativa como `2,8378`.

O valor correto é:

`0,02837812`

Se ROA for expresso como proporção, a interpretação aproximada é uma diferença de **2,84 pontos percentuais**, condicionada à validade da especificação. Não é um aumento de `2,8378` unidades de ROA.

## 8. Interações e interpretação

A interação `dpcdl:dtc` representa:

`Despesa de Provisão sobre Ativos x Tipo de Controle`

Ela não inclui uma dummy eleitoral. Assim, trechos narrativos que descrevem esse coeficiente como efeito sobre bancos públicos `durante períodos eleitorais` adicionam uma condição que não está presente no termo estimado.

O mesmo cuidado será aplicado a todas as interações no novo artigo: nenhuma interpretação será ampliada além das variáveis efetivamente presentes no termo econométrico.

## 9. Decisão de versionamento

A partir desta auditoria serão mantidas duas referências distintas:

### V13 arquivística

Usada exclusivamente para reproduzir a dissertação exatamente como publicada.

SHA-256:

`058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f`

### Base canônica limpa do artigo

Será derivada da V13 por script, inicialmente com:

- `ROA = ROA_V13 - 1`;
- Selic trimestral composta mantida;
- IPCA em proporção decimal mantido;
- preservação de uma coluna `ROA_arquivistico` para auditoria;
- validação das demais fórmulas contábeis antes das novas estimações.

## 10. Próxima etapa

1. construir a base canônica limpa;
2. gerar dicionário de dados e validações de domínio;
3. revisar as demais fórmulas contábeis contra bases anteriores e rubricas de origem;
4. executar event study com data eleitoral trimestral;
5. executar inferência temporal e placebos;
6. somente então decidir a pergunta definitiva do paper.
