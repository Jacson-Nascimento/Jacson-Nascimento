# Dados científicos

Os arquivos de grande volume não são versionados diretamente neste repositório. Eles são gerados deterministicamente por `../tools/generate_reference_data.py` e devem ser arquivados no depósito Zenodo do preprint.

Arquivos gerados localmente:

- `agents_metadata.csv`
- `network_baseline_A.csv`
- `network_baseline_W.csv`
- `monte_carlo_10000_raw.csv.gz`
- `monte_carlo_10000_outcomes.csv.gz`

A tabela `monte_carlo_10000_raw.csv.gz` contém 10.000 linhas de replicação e os 60 sinais individuais `e_i`, além das métricas de maioria informacional e semente estrutural.

## Política de integridade

Para uma release científica, o depósito Zenodo deve incluir:

1. tabela bruta das 10.000 replicações;
2. tabela de desfechos derivados;
3. matrizes `A` e `W`;
4. metadados dos agentes;
5. scripts R;
6. gerador de referência;
7. arquivo de checksums SHA-256;
8. README e dicionário de dados.

O DOI e os hashes do depósito definitivo devem ser registrados no README principal após a publicação.
