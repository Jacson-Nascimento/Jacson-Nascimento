# Configuração administrativa alvo dos repositórios

Este arquivo registra as configurações administrativas desejadas para a conta `Jacson-Nascimento`. Ele serve como referência de governança quando determinada configuração não puder ser alterada por automação.

## Jacson-Nascimento/Jacson-Nascimento

**Finalidade:** perfil acadêmico, índice de projetos e registro histórico público.

**Descrição desejada:**

`Perfil acadêmico e índice de projetos em auditoria, economia aplicada, finanças públicas e pesquisa computacional.`

**Topics desejados:**

- `audit`
- `economics`
- `public-finance`
- `data-analysis`
- `reproducible-research`
- `research`
- `r`
- `python`

**Branch main:** impedir force push e exclusão acidental. Mudanças metodológicas ou estruturais devem preferir PR.

## Jacson-Nascimento/dinamica-manada-organizacional

**Descrição atual adequada:** modelo computacional e estudo reprodutível sobre dinâmica de manada e processos de decisão em ambientes organizacionais.

**Topics desejados:**

- `agent-based-modeling`
- `monte-carlo`
- `organizational-behavior`
- `social-influence`
- `audit`
- `r`
- `python`
- `reproducible-research`

**Branch main:** proteger contra force push e exigir verificações de CI aplicáveis antes de incorporação de mudanças relevantes.

## Jacson-Nascimento/modelo-axion-lotofacil

**Descrição atual adequada:** pesquisa computacional reprodutível sobre combinatória, otimização de carteiras, simulação e validação aplicada à Lotofácil.

**Topics desejados:**

- `combinatorics`
- `monte-carlo`
- `optimization`
- `python`
- `r`
- `reproducible-research`
- `lotofacil`

**Branch main:** proteger contra force push e exigir verificações de CI aplicáveis antes de incorporação de mudanças relevantes.

## Jacson-Nascimento/ciclos-eleitorais-bancos

**Visibilidade:** privada durante a fase atual de reanálise.

**Branch main:** proteger contra force push. Mudanças de método, mensuração e resultados devem ser incorporadas por PR quando possível.

## Jacson-Nascimento/dependencia-fornecedores-compras-publicas

**Visibilidade:** privada durante a fase atual de desenvolvimento e validação.

**Branch main:** proteger contra force push. Coletas, mudanças metodológicas, painéis e resultados devem permanecer versionados em branches e PRs canônicas.

## Jacson-Nascimento/lab-natty-or-not-

**Finalidade:** registro histórico de laboratório, sem desenvolvimento ativo.

**Descrição desejada:**

`Laboratório histórico preservado para rastreabilidade. Projeto não ativo.`

**Estado desejado:** `archived = true`, sem exclusão de conteúdo, commits ou histórico.

## Observação operacional

Descrição, topics, proteção de branch e flag de arquivamento são configurações administrativas do repositório. Quando o conector utilizado não expuser essas operações de escrita, este arquivo permanece como especificação canônica para aplicação manual ou por ferramenta administrativa futura.
