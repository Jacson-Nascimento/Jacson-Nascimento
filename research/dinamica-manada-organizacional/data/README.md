# Dados científicos

Os arquivos de maior volume não são versionados diretamente neste repositório. Eles podem ser gerados deterministicamente por `../tools/generate_reference_data.py` e estão arquivados no registro Zenodo da versão 1.3 do preprint.

- Registro: https://zenodo.org/records/21985858
- DOI: https://doi.org/10.5281/zenodo.21985858
- Data de publicação: 2026-08-17

Arquivos gerados localmente:

- `agents_metadata.csv`
- `network_baseline_A.csv`
- `network_baseline_W.csv`
- `monte_carlo_10000_raw.csv.gz`
- `monte_carlo_10000_outcomes.csv.gz`

A tabela `monte_carlo_10000_raw.csv.gz` contém 10.000 linhas de replicação e os 60 sinais individuais `e_i`, além das métricas de maioria informacional e semente estrutural.

## Conteúdo científico arquivado

O depósito Zenodo inclui, entre outros artefatos:

1. preprint v1.3;
2. tabela bruta das 10.000 replicações;
3. tabela de desfechos derivados;
4. matrizes e metadados estruturais no pacote suplementar;
5. scripts R;
6. gerador de referência;
7. arquivo de checksums SHA-256;
8. README e dicionário de dados.

## Política de integridade

O Zenodo é o registro persistente e citável da versão publicada. O GitHub mantém o código e a automação de reprodução em desenvolvimento. Para reproduzir ou auditar os resultados publicados, utilize o DOI `10.5281/zenodo.21985858` como referência canônica dos artefatos depositados.
