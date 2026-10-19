# Parecer técnico-acadêmico interno - v0.1

Data da revisão: 12 de setembro de 2026  
Objeto: artigo complementar "Concentração de influência e reversão da maioria informacional"  
Natureza: revisão crítica pré-Zenodo, com foco em novidade, validade interna, robustez e risco de objeções de pareceristas.

## Síntese

O artigo tem pergunta própria e pode ser defendido como estudo complementar, mas a v0.1 ainda apresentava duas fragilidades de primeira ordem: posicionava como contribuição um mecanismo geral já bem estabelecido na literatura de aprendizagem em redes e dependia excessivamente de uma única rede e de uma única realização Monte Carlo. A revisão v0.2 corrige ambos os pontos.

## Achados do parecer e tratamento

### 1. Sobreposição com literatura de wisdom of crowds - MAIOR

Golub e Jackson (2010) demonstram que aprendizagem eficiente em redes DeGroot depende de a influência do agente mais influente desaparecer em sociedades grandes. Becker, Brackbill e Centola (2017) mostram experimentalmente que centralização pode deslocar o julgamento coletivo em direção a indivíduos centrais. Tian, Wang e Bullo (2023) formalizam que a relação entre poder social e acurácia determina se influência melhora ou prejudica a sabedoria coletiva.

**Risco:** reivindicação excessiva de novidade.

**Correção:** a contribuição é reposicionada como aplicação e decomposição específica dentro do modelo organizacional: reversão de maioria correta, decomposição por posição hierárquica, relação entre concentração e precisão heterogênea, e intensidade da semente como medida de vulnerabilidade.

### 2. Dependência de uma única realização Monte Carlo - MAIOR

A v0.1 reportava 17,29% como resultado central de uma realização de 10.000 réplicas.

**Correção:** derivação fechada. Sob sinais gaussianos independentes, Z=pi'e é normal com média theta e variância V_pi = soma_i pi_i^2 sigma_i^2. Portanto:

P(S=1) = Phi(-|theta| / sqrt(V_pi)).

No cenário-base, a probabilidade exata é 17,0122%, contra 17,29% na realização publicada. O valor exato está dentro do IC95% de Wilson da estimativa Monte Carlo, 16,56%-18,04%.

### 3. Dependência da rede específica - MAIOR

**Correção:** 500 novas redes Watts-Strogatz, mantendo os papéis hierárquicos. A probabilidade exata média de semente errada foi 17,4563%, mediana 17,4170%, com intervalo estrutural empírico de 2,5%-97,5% igual a 16,9332%-18,4308%. Assim, o resultado-base não depende de uma rede excepcional.

### 4. Dependência da posição do executivo e gestores na rede - MAIOR

**Correção:** 1.000 permutações determinísticas dos papéis hierárquicos na rede publicada, movendo conjuntamente h e sigma. A probabilidade exata média de semente errada foi 22,3500%, mediana 22,3659%, intervalo estrutural 20,6174%-23,8971%. O arranjo publicado, 17,01% em probabilidade exata, é menos adverso do que todas as 1.000 posições sorteadas, o que afasta a hipótese de escolha acidentalmente extrema da posição do executivo.

### 5. Corte de 80% para definir manada - MODERADA

**Correção:** análise de sensibilidade para tau entre 0,70 e 0,90. No cenário beta=0,70/c=0,90, P(H|S) varia de 65,47% a 59,63%. No cenário beta=0,75/c=0,95, varia de 91,90% a 90,17%. A interpretação não depende materialmente do corte de 80%.

### 6. AUC e regressão logística com aparência de validação preditiva - MODERADA

A margem da semente e o evento de manada são produzidos pelo mesmo sistema matemático. Uma AUC elevada é informativa sobre ordenação interna, mas não constitui validação preditiva.

**Correção:** AUC e regressão logística são rebaixadas a diagnósticos suplementares. Não sustentam a contribuição principal nem aparecem como evidência de validade externa.

### 7. Natureza pós-hoc da análise secundária - MODERADA

**Correção:** inclusão de declaração explícita de que a análise é secundária e exploratória, formulada após o estudo-base. As extensões de robustez da v0.2 são identificadas como verificações posteriores ao parecer interno, não como análises pré-registradas.

### 8. Reutilização da mesma massa de dados - MODERADA

**Correção:** o artigo cita explicitamente o primeiro preprint, o DOI dos dados e o repositório. A pergunta e as estatísticas novas são separadas das análises originais. Não se reivindica nova amostra empírica.

## Avaliação após correções

- Distinção em relação ao primeiro artigo: satisfatória.
- Replicabilidade: forte.
- Validade interna do mecanismo de formação da semente: forte após derivação analítica.
- Robustez estrutural: satisfatória após redes e permutações.
- Validade externa: ainda ausente, por desenho.
- Originalidade ampla em dinâmica de opiniões: limitada.
- Originalidade específica para o arcabouço organizacional e auditoria: defensável.
- Risco de rejeição por "resultado já conhecido": reduzido, desde que a introdução reconheça explicitamente Golub-Jackson, Becker-Centola e Tian-Wang-Bullo.

## Recomendação

Prosseguir com v0.2 como preprint complementar. Manter linguagem de "análise secundária teórico-computacional" e evitar apresentar concentração de influência como descoberta inédita. O principal resultado novo deve ser a anatomia da reversão dentro do modelo, apoiada pela solução analítica e pelas verificações estruturais.
