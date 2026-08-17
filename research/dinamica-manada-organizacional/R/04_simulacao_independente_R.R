source(file.path("R", "00_config.R"))

agents <- read.csv(file.path(DATA_DIR, "agents_metadata.csv"), check.names = FALSE)
W <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_W.csv"))
pi_calc <- stationary_pi(W)

set.seed(seed_documentada)
E_new <- matrix(NA_real_, nrow = n_rep, ncol = N)
for (j in seq_len(N)) {
  E_new[, j] <- theta + rnorm(n_rep, mean = 0, sd = agents$sigma[j])
}

frac_correct <- rowMeans(sign(E_new) == sign(theta))
S <- sign(as.vector(E_new %*% pi_calc)) != sign(theta)

out <- data.frame(
  metric = c("mean_fraction_correct", "minimum_fraction_correct", "wrong_seed_count", "wrong_seed_probability"),
  value = c(mean(frac_correct), min(frac_correct), sum(S), mean(S))
)

write.csv(out, file.path(OUTPUT_DIR, "independent_R_monte_carlo_summary.csv"), row.names = FALSE)
print(out, digits = 12)
cat("\nEsta simulacao usa o RNG do R e nao deve coincidir linha a linha com a realizacao PCG64/NumPy.\n")
