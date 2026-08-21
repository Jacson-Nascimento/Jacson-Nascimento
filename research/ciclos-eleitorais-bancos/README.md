# Ciclos Eleitorais e Desempenho Bancário no Brasil

Projeto de continuidade da dissertação de mestrado de Jacson Cruz do Nascimento, com foco em reconstrução reprodutível da base empírica, auditoria dos scripts originais e desenvolvimento de artigo científico derivado.

## Origem

Dissertação: **Impacto das Eleições no Desempenho de Bancos Brasileiros**.

Período empírico final documentado: **1T2000 a 4T2023**.

Painel final documentado: **32 instituições x 96 trimestres = 3.072 observações**.

Fontes principais: Banco Central do Brasil, TSE e séries macroeconômicas utilizadas na dissertação.

## Objetivo desta etapa

Antes de escrever o artigo, o projeto fará uma auditoria de reprodutibilidade para responder quatro perguntas:

1. Qual versão da base gerou cada resultado da dissertação?
2. Quais scripts foram efetivamente executados para os modelos estático e dinâmico?
3. Os resultados podem ser reproduzidos sem depender de caminhos locais, arquivos temporários ou transcrições manuais?
4. Qual desenho empírico é defensável para um artigo de periódico?

## Regra de trabalho

Os coeficientes publicados na dissertação serão tratados como **resultados históricos a reproduzir**, e não como resultados a reutilizar automaticamente. O artigo será estimado novamente a partir de uma base canônica validada e scripts versionados.

## Estrutura

```text
research/ciclos-eleitorais-bancos/
├── README.md
├── data/
│   └── README.md
├── docs/
│   ├── AUDITORIA_ACERVO_DRIVE_2026-08-21.md
│   └── HANDOFF_CONTINUIDADE_2026-08-21.md
├── paper/
│   └── PLANO_ARTIGO.md
└── scripts/
    └── auditoria/
        └── 01_validar_versoes_base.R
```

## Hipótese de artigo prioritária

A linha mais defensável, sujeita à auditoria empírica, é avaliar **heterogeneidade do efeito eleitoral entre bancos públicos e privados**, em vez de atribuir diretamente à eleição um efeito agregado sobre toda a rentabilidade bancária.

A razão econométrica é importante: dummies eleitorais variam apenas no tempo e são comuns a todos os bancos. Com efeitos fixos completos de trimestre, o efeito agregado da eleição é absorvido. Já a interação entre eleição e tipo de controle pode ser identificada com efeitos fixos de banco e de tempo, permitindo controlar choques macroeconômicos comuns.

## Estado em 21/08/2026

- acervo principal localizado no Google Drive;
- versão final da dissertação localizada;
- bases `dataset_290624_11.csv`, `dataset_290624_12.csv` e `dataset_290624_13.csv` recuperadas para auditoria;
- scripts finais estático e dinâmico localizados;
- inconsistência de versão da base entre os dois scripts identificada;
- auditoria e reconstrução em andamento.
