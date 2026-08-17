source(file.path("R", "01_reproduzir_resultados_baseline.R"))
source(file.path("R", "02_reproduzir_tabela5.R"))
source(file.path("R", "03_reproduzir_figuras.R"))
source(file.path("R", "04_simulacao_independente_R.R"))

sink(file.path("outputs", "generated", "sessionInfo_R.txt"))
sessionInfo()
sink()

cat("\nPipeline concluido. Resultados em outputs/generated e figures/generated.\n")
