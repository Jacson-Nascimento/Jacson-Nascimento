# AXION - Addendum Metodológico do Registro Prospectivo

**Versão do mecanismo:** 1.1  
**Data:** 10/09/2026  
**Autor:** Jacson Cruz do Nascimento  
**Protocolo-base:** axion-prospective-v1  
**Marco prospectivo preservado:** concurso 3780

## 1. Motivo da atualização

A versão 1.0 do protocolo prospectivo foi registrada antes do concurso 3780 e antes de qualquer observação prospectiva. O status do ledger permanecia em zero concursos avaliados. Isso permite aperfeiçoar o mecanismo de inferência e de controle de integridade sem utilizar informação do resultado-alvo.

O manifest do concurso 3780 permanece imutável. A atualização atua no mecanismo que reconstruirá o ledger, avaliará os horizontes bloqueados e criará manifests futuros.

## 2. Alterações principais

### 2.1 Teste exato no lugar da aproximação normal

O número de acertos de qualquer jogo de 15 dezenas, definido antes do sorteio, segue sob o modelo justo:

`X ~ Hypergeometric(N=25, K=15, n=15)`

com esperança igual a 9 e variância igual a 1,5.

Nos horizontes de 25, 50, 100 e 250 concursos, a distribuição da soma dos acertos passa a ser calculada pela convolução exata da distribuição hipergeométrica, em vez da aproximação normal anteriormente prevista.

Para cada estratégia é calculado o p-valor unilateral exato da soma de acertos observada ou superior. Os quatro testes pré-registrados são corrigidos por Benjamini-Hochberg dentro de cada horizonte bloqueado.

### 2.2 Comparação com controle aleatório

As diferenças entre cada estratégia e o controle aleatório determinístico continuarão sendo registradas em cada horizonte como estatística descritiva: diferença média de acertos, soma das diferenças e contagem de vitórias, empates e derrotas.

Nesta versão não é atribuído p-valor pareado a essas diferenças. O AXION e algumas estratégias são adaptativos e podem alterar seus jogos com base no histórico anterior. Tratar toda a sequência de sobreposições entre dois jogos adaptativos como fixa para uma convolução pareada poderia introduzir uma hipótese de independência não demonstrada.

### 2.3 Criação fail-closed de manifests futuros

Um novo manifest prospectivo somente será criado quando existir um `prediction_<concurso>_manifest.json` válido para o concurso imediatamente seguinte ao último resultado observado.

O mecanismo verifica o campo `next_contest`, o campo `last_observed_contest`, a existência de exatamente 15 dezenas únicas entre 1 e 25 e o SHA-256 do manifest AXION que originou o jogo.

Se o resultado histórico for atualizado antes da previsão AXION seguinte, o pipeline registra o estado como pendente e não cria um manifest incompleto. Quando a previsão válida for adicionada, o workflow poderá criar o manifest completo.

## 3. Controles adicionais de integridade

O mecanismo 1.1 passa a validar a continuidade dos números de concurso, duplicidades e a integridade das 15 dezenas de cada sorteio.

Também passa a produzir `manifest_index.csv`, `CHECKSUMS.sha256`, `manifest_sha256` em cada linha do ledger e `registry_engine_version` no status e nos novos manifests.

O workflow possui verificação específica para impedir a reescrita de manifests já versionados e arquiva as saídas como artifact do GitHub Actions.

## 4. Regra de interpretação

A atualização 1.1 não muda a hipótese operacional do projeto. O benchmark justo continua sendo 9 acertos em média por jogo de 15 dezenas e nenhuma estratégia é considerada superior antes de sobreviver aos horizontes prospectivos bloqueados.

A primeira análise inferencial permanece no horizonte de 25 concursos. Resultados entre os marcos são armazenados, mas não autorizam recalibração retroativa nem promoção de uma estratégia.

## 5. Governança de versão

O protocolo-base permanece `axion-prospective-v1`. O mecanismo computacional de registro e avaliação passa a ser identificado como `registry_engine_version = 1.1`.

O manifest já criado para o concurso 3780 não será alterado para inserir esse novo campo. Sua ausência será interpretada no índice como mecanismo 1.0. Essa decisão preserva a imutabilidade do primeiro registro.

Novos aperfeiçoamentos inferenciais depois de observado o concurso 3780 deverão ser avaliados com maior restrição. Qualquer alteração que mude endpoint, estratégias, horizontes ou critérios de decisão exigirá nova versão formal do protocolo, sem reescrever os registros já existentes.
