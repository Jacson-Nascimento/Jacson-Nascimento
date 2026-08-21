# Scripts originais localizados no Google Drive

Este diretório documenta a proveniência dos scripts da dissertação. As cópias originais serão incorporadas após a reconciliação da base canônica, preservando nomes e conteúdo sem edição.

## Scripts finais prioritários

| Arquivo | Google Drive ID | Modificação | Base lida no código |
|---|---|---|---|
| `if_ols_estatico_2.R` | `1U9fZqI0aowzs1vIRMcdZP-Nj-Q9VJrDo` | 22/07/2024 | `dataset_290624_11.csv` |
| `if_ols_dinamico_2.R` | `12zdrE_1f5QQAz01_Hp0an0jhcNLnIufG` | 22/07/2024 | `dataset_290624_13.csv` |
| `if_ols_dinamico.R` | `18nT5aMJgMkU8cSh_IxL_zDrnsiv7lMn0` | 11/07/2024 | a verificar |
| `if_ols_estatico.R` | `1r-e_YpgHBmEqbU2nPWTaBUc_MgNmiRxb` | 06/08/2024 | a verificar |
| `.Rhistory` | `116WGx51EyTUrpvnPfwPylTVFhKAJKawA` | 06/08/2024 | confirma execução dos scripts finais |

## Estrutura do modelo estático `_2`

- painel de 32 bancos e 96 trimestres;
- efeitos fixos individuais, `plm(..., model = "within")`;
- ROA e ROE como dependentes;
- variáveis bancárias, dummies eleitorais e interações;
- `vcovHC(..., type = "HC1")` para erros-padrão;
- testes IPS e LLC aplicados aos resíduos.

## Estrutura do modelo dinâmico `_2`

Replica a especificação estática e acrescenta:

- `ROA_lag` no modelo ROA;
- `ROE_lag` no modelo ROE;
- remoção das primeiras observações de cada painel após a defasagem.

## Observação

Os scripts originais contêm caminhos absolutos do Windows. A reconstrução do artigo não utilizará caminhos locais. Todos os caminhos serão relativos à raiz do repositório e todas as entradas serão identificadas por versão e hash.
