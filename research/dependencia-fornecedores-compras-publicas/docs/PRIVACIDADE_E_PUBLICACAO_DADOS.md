# Política de Privacidade e Publicação das Bases

## Escopo

Este documento define quais dados do projeto podem ser versionados no repositório público e quais devem permanecer apenas no armazenamento privado de pesquisa.

## Princípio

O fato de um dado estar disponível em fonte pública não implica necessidade de republicar identificadores pessoais em uma nova base derivada. O projeto aplicará minimização de dados e publicará somente os campos necessários para replicar os resultados científicos.

## GitHub público

Podem ser publicados:

- scripts de coleta, limpeza e análise;
- documentação metodológica;
- dicionários de variáveis;
- manifestos e checksums;
- resultados agregados;
- identificadores de órgãos e entidades públicas;
- identificadores de fornecedores pessoa jurídica quando necessários à replicação da rede empresarial;
- bases analíticas minimizadas com fornecedores PJ;
- tabelas de robustez agregadas que incluam outros tipos de fornecedor sem expor identificadores pessoais.

Não devem ser publicados:

- CPF de fornecedor pessoa física;
- nome de fornecedor pessoa física quando associado ao registro analítico individual;
- outros identificadores pessoais desnecessários à replicação;
- cópias integrais de respostas que contenham tais campos sem tratamento.

## Google Drive privado

O Drive privado pode preservar:

- pacotes brutos originais obtidos das fontes oficiais;
- versões integrais necessárias à auditoria da transformação;
- artefatos temporários de validação;
- arquivos com PF, desde que usados somente para fins metodológicos e análises controladas.

## Amostra principal

A rede empresarial principal poderá ser estimada sobre fornecedores pessoa jurídica, especialmente porque:

1. o objeto central é dependência de fornecedores empresariais;
2. a integração com os dados abertos do CNPJ exige pessoa jurídica;
3. no piloto sentinela de 2025, PJ representaram 11.968 de 12.799 instrumentos municipais válidos, aproximadamente 93,51%.

Fornecedores PF e PE poderão ser incorporados em testes de robustez agregados. A opção final deverá ser declarada explicitamente no artigo.

## Separação entre fonte e publicação derivada

A documentação do artigo indicará que o PNCP é a fonte original. O repositório derivado não pretende substituir nem reproduzir integralmente a fonte pública.

## Reprodutibilidade

Quando uma base pública derivada omitir registros ou identificadores por minimização, o script de coleta e tratamento deverá permitir a um pesquisador autorizado reproduzir a extração diretamente da fonte oficial, observando as regras jurídicas e éticas aplicáveis ao seu próprio tratamento de dados.

## Controle de versões

Toda base publicada deverá indicar:

- data de extração;
- período coberto;
- fonte e endpoint;
- versão do script;
- filtros aplicados;
- regra de tratamento de PF/PJ/PE;
- checksum quando aplicável.
