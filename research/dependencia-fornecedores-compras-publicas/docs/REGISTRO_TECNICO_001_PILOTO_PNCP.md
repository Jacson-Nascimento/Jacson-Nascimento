# Registro Técnico 001 - Piloto PNCP

## Objetivo

Validar a estrutura mínima necessária para construir relações comprador-fornecedor e testar o pipeline de concentração antes da coleta nacional.

## Fonte verificada

Endpoint público de contratos do PNCP:

`https://pncp.gov.br/api/consulta/v1/contratos`

Consulta de referência inspecionada: contratos publicados em 02/01/2023. A resposta informou 182 registros e uma página.

## Campos confirmados

- `numeroControlePncpCompra`
- `numeroControlePNCP`
- `niFornecedor`
- `nomeRazaoSocialFornecedor`
- `tipoPessoa`
- `orgaoEntidade.cnpj`
- `orgaoEntidade.esferaId`
- `orgaoEntidade.poderId`
- `categoriaProcesso.nome`
- `unidadeOrgao.codigoIbge`
- `unidadeOrgao.municipioNome`
- `unidadeOrgao.ufSigla`
- `valorInicial`
- `valorGlobal`
- `dataAssinatura`
- `dataPublicacaoPncp`
- `numeroRetificacao`
- `tipoContrato.nome`

## Evidência estrutural relevante

A microamostra registra uma mesma contratação (`numeroControlePncpCompra`) associada a vários instrumentos e fornecedores. Portanto, deduplicar a base apenas pelo identificador da compra destruiria informação econômica válida.

Na microamostra de 12 instrumentos:

- 12 contratos/instrumentos únicos;
- 7 identificadores de compra únicos;
- 3 das 7 compras aparecem com mais de um instrumento na amostra parcial;
- o máximo observado na microamostra foi de 4 instrumentos associados ao mesmo identificador de compra;
- 11 fornecedores distintos;
- 6 municípios de localização das unidades administrativas;
- atraso mediano entre assinatura e publicação de 3 dias.

Esses números servem exclusivamente para validação de estrutura e código. A microamostra é parcial, federal e não representa um mercado anual.

## Teste das métricas

O pipeline calculou, sem erro, HHI, CR1, CR4, número efetivo de fornecedores e entropia para os grupos presentes na microamostra. Os resultados estão em `results/microamostra_validacao_metricas.csv`.

Os valores de concentração não devem ser interpretados substantivamente porque a microamostra contém apenas os primeiros registros observados em uma resposta de API e não a totalidade anual de cada mercado municipal.

## Implicações para a coleta principal

1. Unidade econômica principal: município x categoria x ano.
2. Chave do instrumento: `numeroControlePNCP`.
3. Chave de ligação com a contratação: `numeroControlePncpCompra`.
4. Fornecedor: `niFornecedor`, tratado como texto.
5. Coleta por data de publicação, classificação econômica por data de assinatura.
6. Verificar duplicidade de `numeroControlePNCP` e comportamento de retificações antes da agregação.
7. Separar tipos de instrumento antes de somar valores.
8. Medir cobertura temporal por município antes de qualquer comparação entre anos.

## Próxima etapa

Executar a coleta piloto de 2025 em datas distribuídas ao longo do ano, medir completude e cobertura municipal, e então decidir a janela definitiva de coleta 2024-2025, incluindo publicações posteriores referentes a contratos assinados nesses exercícios.
