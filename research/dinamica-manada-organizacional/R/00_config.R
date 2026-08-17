options(stringsAsFactors = FALSE, scipen = 999)

ROOT <- normalizePath(".")
DATA_DIR <- file.path(ROOT, "data")
OUTPUT_DIR <- file.path(ROOT, "outputs", "generated")
FIGURE_DIR <- file.path(ROOT, "figures", "generated")
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGURE_DIR, showWarnings = FALSE, recursive = TRUE)

N <- 60L
theta <- -1
rho <- 0.20
kappa_baseline <- 5
seed_documentada <- 20260816L
n_rep <- 10000L
tau_herd <- 0.80

read_matrix_csv <- function(path) {
  x <- read.csv(path, check.names = FALSE)
  as.matrix(x[, -1, drop = FALSE])
}

stationary_pi <- function(W) {
  ee <- eigen(t(W))
  j <- which.min(abs(ee$values - 1))
  p <- Re(ee$vectors[, j])
  if (sum(p) < 0) p <- -p
  p / sum(p)
}

wilson_interval <- function(x, n, conf.level = 0.95) {
  z <- qnorm(1 - (1-conf.level)/2)
  phat <- x/n
  den <- 1 + z^2/n
  center <- (phat + z^2/(2*n))/den
  half <- z * sqrt(phat*(1-phat)/n + z^2/(4*n^2))/den
  c(lower = max(0, center-half), upper = min(1, center+half))
}
