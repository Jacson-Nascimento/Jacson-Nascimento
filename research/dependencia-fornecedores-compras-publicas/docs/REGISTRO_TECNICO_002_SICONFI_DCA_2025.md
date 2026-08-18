# Registro Técnico 002 - SICONFI / DCA 2025

## Objetivo

Definir o uso da Declaração de Contas Anuais do SICONFI como fonte fiscal municipal complementar ao PNCP.

## Situação da base em agosto de 2026

A documentação oficial do SICONFI para o exercício de 2026 informa que a DCA desse ciclo se refere às contas anuais do exercício de 2025. As instruções de preenchimento da DCA 2025 foram publicadas em fevereiro de 2026.

Isso permite integrar dados fiscais de 2025 aos contratos assinados em 2025, respeitada a cobertura de municípios que homologaram suas contas no SICONFI.

## Fonte

- API SICONFI: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/
- Endpoint DCA: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca
- Documentação: https://apidatalake.tesouro.gov.br/docs/siconfi/
- Documentação oficial DCA 2025: https://www.siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=46903

## Anexos prioritários

### DCA-Anexo I-D

Demonstrativo de Despesas Orçamentárias por Natureza.

Uso previsto:
- despesa orçamentária total;
- despesas empenhadas;
- despesas liquidadas;
- despesas pagas;
- despesas correntes;
- despesas de capital;
- investimentos, quando identificáveis de forma consistente.

### DCA-Anexo I-E

Demonstrativo de Despesas Orçamentárias por Função.

Uso previsto:
- composição funcional da despesa;
- controles para saúde, educação, administração e outras funções relevantes;
- análises de heterogeneidade por categoria de contratação.

## Parâmetros de consulta

O endpoint DCA utiliza, entre outros:
- `an_exercicio`: exercício das contas;
- `id_ente`: código do ente, compatível com o código IBGE;
- `no_anexo`: anexo específico, por exemplo `DCA-Anexo I-D`.

## Chave de integração

A integração com o PNCP será realizada por código IBGE municipal:

`PNCP.unidadeOrgao.codigoIbge = SICONFI.id_ente`

A correspondência será auditada antes do merge definitivo.

## Variáveis derivadas previstas

### Intensidade das contratações

`ProcurementIntensity_bt = ValorContratadoPNCP_bt / DespesaTotalSICONFI_bt`

A razão será usada principalmente como controle de escala e diagnóstico de consistência. Valores extremos não serão interpretados automaticamente como erro, pois PNCP e DCA medem objetos contábeis distintos.

### Contratações per capita

`ProcurementPC_bt = ValorContratadoPNCP_bt / Populacao_bt`

### Despesa per capita

`DespesaPC_bt = DespesaTotalSICONFI_bt / Populacao_bt`

## Riscos metodológicos

1. Nem todos os entes necessariamente possuem DCA homologada no momento da extração.
2. Valor contratado no PNCP não equivale a despesa empenhada, liquidada ou paga na DCA.
3. Contratos plurianuais podem gerar valor inicial superior à execução orçamentária do exercício.
4. A DCA é anual, enquanto a contratação possui data específica.
5. Retificações do SICONFI podem alterar os valores após uma extração inicial.

## Controles

- registrar data da coleta;
- preservar resposta bruta ou base extraída;
- verificar cobertura municipal;
- registrar anexo e coluna fiscal utilizada;
- não comparar diretamente valores sem documentar a natureza contábil;
- executar análise de sensibilidade com variáveis fiscais alternativas quando apropriado.

## Decisão

SICONFI/DCA 2025 permanece aprovado como base complementar principal do artigo. Sua integração ocorrerá depois da validação da cobertura PNCP 2025, para evitar construir controles fiscais antes de definir a amostra contratual final.
