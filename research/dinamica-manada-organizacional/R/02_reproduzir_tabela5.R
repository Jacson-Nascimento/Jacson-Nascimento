source(file.path("R", "00_config.R"))

W <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_W.csv"))
raw <- read.csv(gzfile(file.path(DATA_DIR, "monte_carlo_10000_raw.csv.gz")), check.names = FALSE)
e_cols <- grep("^e_[0-9]{3}$", names(raw), value = TRUE)
E <- as.matrix(raw[, e_cols, drop = FALSE])

pi_calc <- stationary_pi(W)
S <- sign(as.vector(E %*% pi_calc)) != sign(theta)
nS <- sum(S)

scenarios <- data.frame(
  beta = c(0.30, 0.50, 0.70, 0.75),
  cpar = c(0.30, 0.60, 0.90, 0.95)
)

res <- vector("list", nrow(scenarios))
I_N <- diag(N)

for (r in seq_len(nrow(scenarios))) {
  beta <- scenarios$beta[r]
  cpar <- scenarios$cpar[r]
  lambda <- 0.80 - beta

  H <- lambda*(1-cpar) *
    solve((lambda + beta)*I_N - (beta + lambda*cpar)*W)

  Y <- E %*% t(H)
  frac_wrong <- rowMeans(sign(Y) != sign(theta))
  herd <- frac_wrong >= tau_herd

  x <- sum(herd[S])
  ci <- wilson_interval(x, nS)

  res[[r]] <- data.frame(
    beta = beta,
    c = cpar,
    lambda = lambda,
    conditional_n_seed_wrong = nS,
    herd_count_given_seed_wrong = x,
    P_H_given_S = x/nS,
    wilson_low_95 = ci["lower"],
    wilson_high_95 = ci["upper"],
    P_H_given_not_S = mean(herd[!S]),
    P_H_total = mean(herd)
  )
}

tab5 <- do.call(rbind, res)
rownames(tab5) <- NULL
write.csv(tab5, file.path(OUTPUT_DIR, "reproduced_table5_R.csv"), row.names = FALSE)
print(tab5, digits = 12)
