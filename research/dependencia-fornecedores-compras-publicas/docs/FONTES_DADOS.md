# Fontes de Dados e Evidências Técnicas

## PNCP

Portal de Dados Abertos:
https://www.gov.br/pncp/pt-br/acesso-a-informacao/dados-abertos

Manual de Integração:
https://pncp.gov.br/manual/pt-br/latest/

Consulta de contratos utilizada na validação:
https://pncp.gov.br/api/consulta/v1/contratos?dataFinal=20230102&dataInicial=20230102&pagina=1

Na consulta de validação de 02/01/2023, a API retornou 182 registros em uma página. Foram observados os campos necessários para identificar contratação, instrumento, fornecedor, órgão, município, categoria, valores, assinatura, publicação e retificação.

## SICONFI / Tesouro Nacional

API de Dados Abertos:
https://www.tesourotransparente.gov.br/consultas/consultas-siconfi/siconfi-api-de-dados-abertos

A API é pública, sem necessidade de identificação do usuário, retorna JSON e informa paginação padrão de até 5.000 itens.

## IBGE

Bases previstas:
- estimativas populacionais municipais;
- PIB dos municípios, com uso defasado quando necessário;
- códigos municipais para integração.

## Receita Federal / CNPJ

Uso previsto como enriquecimento cadastral de fornecedores. CNPJ e identificadores de fornecedores devem ser mantidos como texto, não como tipo numérico.

## Política de reprodutibilidade

Sempre registrar:
- URL ou endpoint;
- parâmetros da consulta;
- data da extração;
- hash ou identificação da versão quando aplicável;
- arquivo bruto preservado;
- script que originou a base tratada;
- critérios de exclusão e transformação.
