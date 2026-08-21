# Auditoria das bases finais da dissertação
# Autor: Jacson Cruz do Nascimento
# Projeto: ciclos-eleitorais-bancos
# Data inicial: 21/08/2026

required <- c("dplyr", "readr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) {
  stop("Pacotes ausentes: ", paste(missing, collapse = ", "))
}

library(dplyr)
library(readr)

root <- normalizePath(file.path(getwd()), winslash = "/", mustWork = FALSE)

# Ajuste se o script for executado fora da raiz do projeto.
data_dir <- file.path(root, "research", "ciclos-eleitorais-bancos", "data", "raw")
results_dir <- file.path(root, "research", "ciclos-eleitorais-bancos", "results", "auditoria_base")
dir.create(results_dir, recursive = TRUE, showWarnings = FALSE)

files <- c(
  v11 = "dataset_290624_11.csv",
  v12 = "dataset_290624_12.csv",
  v13 = "dataset_290624_13.csv"
)

paths <- file.path(data_dir, files)
if (!all(file.exists(paths))) {
  stop(
    "Arquivos não encontrados em data/raw. Esperados: ",
    paste(files, collapse = ", ")
  )
}

read_version <- function(path) {
  read_csv(path, show_col_types = FALSE) |>
    mutate(Data = as.Date(Data)) |>
    arrange(`Instituição`, Data)
}

bases <- lapply(paths, read_version)

key_cols <- c("Instituição", "Data")
expected_cols <- c(
  "Data", "Instituição", "dummy_tp", "ROA", "ROE", "IND_EFICIENCIA",
  "Indice_individamento", "Spread Bancário", "PC", "PCC", "dummy_EG",
  "dummy_EM", "Taxa_IPCA", "taxa_selic_", "MCAT", "Desp_Provisao_At"
)

summarise_base <- function(df, version) {
  tibble(
    versao = version,
    n_linhas = nrow(df),
    n_colunas = ncol(df),
    n_bancos = n_distinct(df$`Instituição`),
    n_trimestres = n_distinct(df$Data),
    data_inicial = min(df$Data),
    data_final = max(df$Data),
    duplicidades_banco_data = sum(duplicated(df[key_cols])),
    total_na = sum(is.na(df))
  )
}

summary_tbl <- bind_rows(
  Map(summarise_base, bases, names(bases))
)

write_csv(summary_tbl, file.path(results_dir, "resumo_versoes.csv"))
print(summary_tbl)

for (nm in names(bases)) {
  if (!identical(names(bases[[nm]]), expected_cols)) {
    warning("Colunas inesperadas em ", nm)
  }
}

compare_keys <- function(a, b, name_a, name_b) {
  same <- identical(a[key_cols], b[key_cols])
  tibble(comparacao = paste(name_a, name_b, sep = "_vs_"), mesmas_chaves = same)
}

keys_tbl <- bind_rows(
  compare_keys(bases$v11, bases$v12, "v11", "v12"),
  compare_keys(bases$v12, bases$v13, "v12", "v13"),
  compare_keys(bases$v11, bases$v13, "v11", "v13")
)
write_csv(keys_tbl, file.path(results_dir, "comparacao_chaves.csv"))

numeric_equal <- function(x, y, tol = 1e-12) {
  both_na <- is.na(x) & is.na(y)
  same <- abs(x - y) <= tol
  same[is.na(same)] <- FALSE
  same | both_na
}

compare_values <- function(a, b, name_a, name_b) {
  cols <- setdiff(intersect(names(a), names(b)), key_cols)
  bind_rows(lapply(cols, function(col) {
    x <- a[[col]]
    y <- b[[col]]

    if (is.numeric(x) && is.numeric(y)) {
      eq <- numeric_equal(x, y)
    } else {
      eq <- as.character(x) == as.character(y)
      eq[is.na(eq)] <- FALSE
    }

    tibble(
      comparacao = paste(name_a, name_b, sep = "_vs_"),
      variavel = col,
      n_diferencas = sum(!eq)
    )
  }))
}

diffs_tbl <- bind_rows(
  compare_values(bases$v11, bases$v12, "v11", "v12"),
  compare_values(bases$v12, bases$v13, "v12", "v13"),
  compare_values(bases$v11, bases$v13, "v11", "v13")
) |>
  filter(n_diferencas > 0)

write_csv(diffs_tbl, file.path(results_dir, "diferencas_por_variavel.csv"))
print(diffs_tbl)

# Diagnóstico específico das variáveis que mudaram.
macro_diag <- bind_rows(
  lapply(names(bases), function(nm) {
    df <- bases[[nm]]
    tibble(
      versao = nm,
      ipca_min = min(df$Taxa_IPCA),
      ipca_max = max(df$Taxa_IPCA),
      ipca_media = mean(df$Taxa_IPCA),
      selic_min = min(df$taxa_selic_),
      selic_max = max(df$taxa_selic_),
      selic_media = mean(df$taxa_selic_)
    )
  })
)

write_csv(macro_diag, file.path(results_dir, "diagnostico_macro.csv"))

cat("\nAuditoria concluída. Saídas em:\n", results_dir, "\n")
