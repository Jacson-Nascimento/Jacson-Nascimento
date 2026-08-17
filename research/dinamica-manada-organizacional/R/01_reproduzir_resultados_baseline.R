source(file.path("R", "00_config.R"))

agents <- read.csv(file.path(DATA_DIR, "agents_metadata.csv"), check.names = FALSE)
A <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_A.csv"))
W <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_W.csv"))
raw <- read.csv(gzfile(file.path(DATA_DIR, "monte_carlo_10000_raw.csv.gz")), check.names = FALSE)

stopifnot(nrow(agents) == N, nrow(W) == N, ncol(W) == N)
stopifnot(max(abs(rowSums(W) - 1)) < 1e-10)
stopifnot(all(diag(A) == 1))

pi_calc <- stationary_pi(W)
neff_calc <- 1/sum(pi_calc^2)

e_cols <- grep("^e_[0-9]{3}$", names(raw), value = TRUE)
E <- as.matrix(raw[, e_cols, drop = FALSE])

frac_correct_calc <- rowMeans(sign(E) == sign(theta))
seed_agg_calc <- as.vector(E %*% pi_calc)
seed_wrong_calc <- sign(seed_agg_calc) != sign(theta)

summary_out <- data.frame(
  metric = c(
    "mean_fraction_correct",
    "minimum_fraction_correct",
    "wrong_seed_count",
    "wrong_seed_probability",
    "executive_stationary_weight",
    "top6_stationary_weight",
    "effective_number_sources"
  ),
  value = c(
    mean(frac_correct_calc),
    min(frac_correct_calc),
    sum(seed_wrong_calc),
    mean(seed_wrong_calc),
    pi_calc[1],
    sum(pi_calc[1:6]),
    neff_calc
  )
)

write.csv(summary_out,
          file.path(OUTPUT_DIR, "reproduced_baseline_summary_R.csv"),
          row.names = FALSE)

print(summary_out, digits = 12)
