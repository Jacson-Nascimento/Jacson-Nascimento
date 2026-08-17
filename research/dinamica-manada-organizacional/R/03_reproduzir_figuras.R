source(file.path("R", "00_config.R"))

agents <- read.csv(file.path(DATA_DIR, "agents_metadata.csv"), check.names = FALSE)
A <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_A.csv"))
W <- read_matrix_csv(file.path(DATA_DIR, "network_baseline_W.csv"))
raw <- read.csv(gzfile(file.path(DATA_DIR, "monte_carlo_10000_raw.csv.gz")), check.names = FALSE)
e_cols <- grep("^e_[0-9]{3}$", names(raw), value = TRUE)
E <- as.matrix(raw[, e_cols, drop = FALSE])

frac_correct <- rowMeans(sign(E) == sign(theta))
png(file.path(FIGURE_DIR, "figura4_distribuicao_maioria_informacional_R.png"), width = 1600, height = 900, res = 150)
hist(frac_correct, breaks = 30,
     main = "Distribuicao da maioria informacional no cenario-base",
     xlab = "Fracao de agentes com sinal correto",
     ylab = "Numero de replicacoes")
abline(v = mean(frac_correct), lty = 2, lwd = 2)
abline(v = 0.60, lty = 3, lwd = 2)
legend("topleft", legend = c(sprintf("Media = %.2f%%", 100*mean(frac_correct)), "Criterio de 60%"), lty = c(2,3), bty = "n")
dev.off()

h <- agents$h
kappas <- 0:5
neff <- numeric(length(kappas))
for (i in seq_along(kappas)) {
  mult <- exp(kappas[i]*h)
  Wk <- A * matrix(mult, nrow = N, ncol = N, byrow = TRUE)
  Wk <- Wk / rowSums(Wk)
  pik <- stationary_pi(Wk)
  neff[i] <- 1/sum(pik^2)
}
png(file.path(FIGURE_DIR, "figura5_tamanho_efetivo_fontes_R.png"), width = 1600, height = 900, res = 150)
plot(kappas, neff, type = "b", pch = 19,
     xlab = "Sensibilidade a hierarquia kappa",
     ylab = "Tamanho efetivo de fontes n_eff",
     main = "Concentracao estrutural e tamanho efetivo de fontes")
abline(h = N, lty = 3)
dev.off()

pi_calc <- stationary_pi(W)
S <- sign(as.vector(E %*% pi_calc)) != sign(theta)
betas <- seq(0.05, 0.75, by = 0.05)
cs <- seq(0, 0.95, by = 0.05)
Z <- matrix(NA_real_, nrow = length(cs), ncol = length(betas))
I_N <- diag(N)

for (ib in seq_along(betas)) {
  beta <- betas[ib]
  lambda <- 0.80 - beta
  for (ic in seq_along(cs)) {
    cpar <- cs[ic]
    H <- lambda*(1-cpar) * solve((lambda + beta)*I_N - (beta + lambda*cpar)*W)
    Y <- E %*% t(H)
    herd <- rowMeans(sign(Y) != sign(theta)) >= tau_herd
    Z[ic, ib] <- mean(herd[S])
  }
}

png(file.path(FIGURE_DIR, "figura6_fronteira_manada_R.png"), width = 1600, height = 1000, res = 150)
image(betas, cs, t(Z),
      xlab = "Influencia social beta",
      ylab = "Custo de discordancia c",
      main = "Fronteira de manada: P(H | S)")
contour(betas, cs, t(Z), add = TRUE)
dev.off()

write.csv(data.frame(kappa = kappas, n_eff = neff),
          file.path(OUTPUT_DIR, "reproduced_figure5_values_R.csv"),
          row.names = FALSE)
