# Registro Técnico 004 - Validação Empírica do SICONFI / DCA 2025

## Objetivo

Validar, com consultas reais, se a DCA 2025 do SICONFI pode fornecer controles fiscais anuais compatíveis com a chave territorial usada no projeto PNCP.

## Municípios testados

- São Paulo/SP - código IBGE 3550308
- Florianópolis/SC - código IBGE 4205407
- Goiânia/GO - código IBGE 5208707

## Anexos consultados

- DCA-Anexo I-D - Despesas Orçamentárias por Natureza
- DCA-Anexo I-E - Despesas Orçamentárias por Função

## Resultado operacional

Foram executadas 6 consultas, duas para cada município.

- consultas bem-sucedidas: 6
- consultas com erro: 0
- consultas vazias: 0
- registros coletados: 2.144

Distribuição:

| Município | Anexo | Registros |
|---|---|---:|
| São Paulo | I-D | 422 |
| São Paulo | I-E | 545 |
| Florianópolis | I-D | 341 |
| Florianópolis | I-E | 310 |
| Goiânia | I-D | 279 |
| Goiânia | I-E | 247 |

## Estrutura observada

O retorno possui 14 colunas:

- `exercicio`
- `instituicao`
- `cod_ibge`
- `uf`
- `anexo`
- `rotulo`
- `coluna`
- `cod_conta`
- `conta`
- `valor`
- `populacao`
- `_municipio_consulta`
- `_anexo_consulta`
- `_exercicio_consulta`

## Evidência de variáveis fiscais utilizáveis

No DCA-Anexo I-D de São Paulo foram observadas, entre outras, as linhas:

- Total Geral da Despesa - Despesas Empenhadas: aproximadamente R$ 123,57 bilhões;
- Total Geral da Despesa - Despesas Liquidadas: aproximadamente R$ 117,01 bilhões;
- Total Geral da Despesa - Despesas Pagas: aproximadamente R$ 116,80 bilhões;
- Despesas Correntes - Despesas Empenhadas: aproximadamente R$ 108,88 bilhões.

O retorno também trouxe população de 12.200.180 para o município nessa base.

Esses valores servem somente para validar estrutura e escala. Não são ainda resultados do artigo.

## Chave de integração

A chave observada é `cod_ibge`, compatível com o código municipal utilizado pelo PNCP/IBGE.

A integração territorial proposta permanece:

`PNCP.municipio_ibge = SICONFI.cod_ibge`

A análise principal de concentração, contudo, usa o CNPJ institucional do comprador. O SICONFI entra como controle municipal do ambiente fiscal em que a instituição está inserida.

## Variáveis candidatas

### Despesa total empenhada

Selecionar:

- `anexo = DCA-Anexo I-D`
- `cod_conta = TotalDespesas`
- `coluna = Despesas Empenhadas`

### Despesa total liquidada

- `cod_conta = TotalDespesas`
- `coluna = Despesas Liquidadas`

### Despesa total paga

- `cod_conta = TotalDespesas`
- `coluna = Despesas Pagas`

### Despesas correntes

Selecionar a conta agregada de despesas correntes e a coluna fiscal de interesse.

### Despesas de capital e investimentos

Serão extraídas de contas específicas depois de validar os códigos de conta em uma amostra maior.

## Intensidade de contratação

Uma medida candidata é:

`ProcurementIntensity_bt = ValorContratadoPNCP_bt / DespesaEmpenhadaSICONFI_bt`

A interpretação exige cautela: valor contratado e despesa empenhada são conceitos distintos, contratos podem ser plurianuais e o instrumento pode ter vigência além do exercício.

Essa razão será utilizada como controle de escala e teste de consistência, não como identidade contábil.

## Decisão

**SICONFI/DCA 2025 aprovado para integração ao artigo.**

O teste confirmou:

1. disponibilidade da DCA do mesmo exercício de 2025;
2. consulta por código IBGE;
3. retorno não vazio nos três municípios testados;
4. estrutura de contas e colunas adequada para extrair despesa empenhada, liquidada e paga;
5. viabilidade de coleta automatizada.

## Próxima etapa

A coleta completa do SICONFI será condicionada à amostra final de municípios do PNCP. Não será baixada antecipadamente para todos os entes. Isso reduz processamento e evita integrar controles fiscais de observações posteriormente excluídas.

O artefato do teste foi preservado no Drive privado e o script de coleta está versionado no repositório.
