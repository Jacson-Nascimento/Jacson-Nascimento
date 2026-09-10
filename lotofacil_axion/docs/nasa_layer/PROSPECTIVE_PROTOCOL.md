# AXION - Protocolo Prospectivo a partir do Concurso 3780

**Versão:** 1.0  
**Data de registro:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Início prospectivo:** concurso 3780

## 1. Motivo

Os experimentos da NASA Signal Analysis Layer produziram alguns sinais descritivos no histórico anterior ao concurso 3436, principalmente dispersão de frequências. Entretanto, esses sinais e o AXION 0.3 não demonstraram vantagem estatisticamente suficiente no holdout genuíno dos concursos 3436 a 3779.

A partir deste ponto, o projeto prioriza evidência prospectiva. As regras avaliadas devem ser registradas antes do resultado do concurso alvo e não podem ser alteradas retrospectivamente.

## 2. Endpoint primário

O endpoint primário é o número de acertos de um único jogo de 15 dezenas.

Sob sorteio uniforme 15/25, qualquer jogo pré-declarado de 15 dezenas possui sobreposição esperada igual a 9 dezenas. Esse valor é o benchmark principal.

## 3. Estratégias pré-registradas

Serão acompanhadas quatro estratégias:

1. `axion_top_game`: jogo principal produzido pelo AXION antes do concurso;
2. `fixed_pre3436_top15`: 15 dezenas de maior frequência acumulada, congeladas no concurso 3435;
3. `rolling1000_top15`: 15 dezenas de maior frequência nos 1.000 concursos imediatamente anteriores ao alvo;
4. `deterministic_random_control`: jogo uniforme de controle determinado por hash do número do concurso e pelo salt público `AXION-PROSPECTIVE-CONTROL-v1`.

O controle determinístico existe para que o benchmark aleatório seja reproduzível e não possa ser escolhido depois do resultado.

## 4. Horizontes bloqueados

As análises inferenciais serão revisadas somente após completar:

- 25 concursos;
- 50 concursos;
- 100 concursos;
- 250 concursos.

Resultados intermediários podem ser armazenados no ledger, mas não serão usados para promover, abandonar ou recalibrar uma estratégia antes do próximo horizonte bloqueado.

## 5. Regras de governança

1. Cada jogo deve ser registrado antes de o resultado do concurso alvo estar disponível.
2. Manifests antigos não serão reescritos pelo pipeline.
3. O histórico será reconstruído a partir dos manifests preservados, não de regras recalculadas retroativamente.
4. Comparações múltiplas entre as quatro estratégias terão correção Benjamini-Hochberg em cada horizonte bloqueado.
5. Nenhum resultado será convertido automaticamente em regra de aposta.
6. Alterações metodológicas futuras deverão criar nova versão do protocolo e novo marco prospectivo.
7. Resultados negativos e inconclusivos serão preservados.

## 6. Primeiro registro

O primeiro manifest prospectivo foi criado para o concurso **3780**, depois de observado o concurso 3779 e antes de qualquer resultado do concurso 3780 constar na base do projeto.

As quatro estratégias foram congeladas no arquivo:

`results/nasa_layer/prospective_registry/baseline_manifest_3780.json`

O status inicial registra zero concursos avaliados e próximo horizonte bloqueado de 25 concursos.

## 7. Critério de interpretação

O objetivo não é procurar significância a qualquer custo. O resultado relevante será a consistência fora da amostra.

Uma estratégia somente poderá ser considerada candidata a investigação adicional se:

- superar o benchmark justo no horizonte bloqueado;
- sobreviver ao controle de multiplicidade;
- apresentar direção consistente em horizontes posteriores;
- não depender de seleção retrospectiva de janelas, dezenas ou parâmetros;
- apresentar ganho material, e não apenas significância estatística marginal.

Até que esses requisitos sejam satisfeitos, a hipótese operacional permanece: **não há vantagem preditiva demonstrada**.
