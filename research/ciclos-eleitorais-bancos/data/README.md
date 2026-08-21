# Dados

Este diretório será usado para a base canônica do artigo e arquivos auxiliares de reprodutibilidade.

## Situação atual

Os arquivos brutos recuperados do Google Drive ainda **não foram incorporados ao GitHub**. A prioridade inicial é fechar a proveniência e evitar publicar como definitiva uma versão que depois precise ser substituída.

## Bases finais em auditoria

| Versão | Arquivo | Google Drive ID | SHA-256 | Situação |
|---|---|---|---|---|
| V11 | `dataset_290624_11.csv` | `1yexH75tm4SpoRlruhu1uamP5X_bVHg8j` | `8f2a06bae81e80a58fe1acadc38fe7982594ca3a489e22cd64ef4bb40d4388e2` | usada pelo script estático `_2` |
| V12 | `dataset_290624_12.csv` | `1UB8W7KLldtbqEGQEZqo6DZIkf9Hi6HBr` | `3b45c30d2352f04c3b1c8b070d91678f41964f95e683e615fcf72449f7220a5d` | correção intermediária |
| V13 | `dataset_290624_13.csv` | `1kxTXsGYjc5W49Tw7SorIOyRVS9gWFWMp` | `058d0af9323925a8e82a0c532f247649ad72ffbf8a9968d6f8002eb387e4965f` | usada pelo script dinâmico `_2`; candidata canônica |

Todas possuem:

- 3.072 observações;
- 32 instituições;
- 96 trimestres;
- período de 1T2000 a 4T2023;
- nenhuma duplicidade na chave `Instituição + Data`;
- nenhum valor ausente.

## Colunas comuns

```text
Data
Instituição
dummy_tp
ROA
ROE
IND_EFICIENCIA
Indice_individamento
Spread Bancário
PC
PCC
dummy_EG
dummy_EM
Taxa_IPCA
taxa_selic_
MCAT
Desp_Provisao_At
```

## Política para o artigo

1. Nunca editar manualmente a base canônica.
2. Toda transformação deve ocorrer por script.
3. A base analítica final deve ser gerada a partir de uma fonte identificada por hash.
4. Resultados devem registrar a versão da base e o commit do código.
5. Arquivos com dados públicos podem ser versionados após a auditoria, desde que tamanho e licença permitam.
6. A versão histórica da dissertação deve permanecer preservada e separada da base reconstruída para o artigo.
