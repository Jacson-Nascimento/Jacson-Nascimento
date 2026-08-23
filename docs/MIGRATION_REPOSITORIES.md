# Migração não destrutiva para repositórios dedicados

Este runbook conclui a separação dos projetos atualmente mantidos no repositório de perfil.

## Repositórios de destino

Os três repositórios de destino já foram criados em 23/08/2026:

1. `Jacson-Nascimento/dependencia-fornecedores-compras-publicas`
2. `Jacson-Nascimento/dinamica-manada-organizacional`
3. `Jacson-Nascimento/modelo-axion-lotofacil`

No momento da preparação da migração, os dois primeiros estavam privados e o terceiro público. Essa visibilidade pode ser revista depois da validação dos conteúdos e metadados.

Cada destino recebeu apenas `MIGRATION_PROVENANCE.md`, com a origem anterior e o commit de referência `1f14be405b948f7091e14ccd88e8136ef40ba255`.

## Objetivo técnico

A migração usa `git subtree split` para reconstruir, em cada repositório de destino, o histórico de commits relacionado ao respectivo diretório. O repositório de origem permanece intacto.

Como os destinos já possuem um commit de inicialização, o script integra esse commit ao histórico filtrado com `--allow-unrelated-histories` e cria um merge explícito. Dessa forma, tanto a proveniência do novo repositório quanto o histórico do projeto são preservados.

Não são executados comandos de exclusão de arquivos, branches, tags ou diretórios.

## Pré-requisitos

- Git instalado e disponível no PowerShell.
- Clone local atualizado de `Jacson-Nascimento/Jacson-Nascimento`.
- Credencial do GitHub configurada no Git Credential Manager ou mecanismo equivalente.
- Acesso de escrita aos três repositórios de destino.
- Árvore de trabalho local sem alterações pendentes.

## Validação prévia

Na raiz do clone local:

```powershell
git status
git pull --ff-only origin main
.\tools\migrate_projects_to_repos.ps1 -DryRun
```

O `DryRun` apenas lista os projetos, destinos e branches previstas. Não cria branches nem envia commits.

## Execução

```powershell
.\tools\migrate_projects_to_repos.ps1
```

O script:

1. valida que está em um repositório Git;
2. exige árvore de trabalho limpa;
3. registra o commit atual da origem;
4. localiza cada diretório de projeto;
5. cria uma branch `migration/...` por projeto usando `git subtree split`;
6. registra um remote específico para cada novo repositório;
7. consulta a branch `main` do destino;
8. quando o destino já possui commits, cria uma branch de integração e faz merge não destrutivo dos dois históricos;
9. envia o resultado para `main` do novo repositório;
10. preserva integralmente o repositório de origem e as branches de migração.

## Validação após a migração

Em cada novo repositório, confirmar:

- presença do `README.md` do projeto;
- presença do `MIGRATION_PROVENANCE.md`;
- presença dos scripts e dados publicáveis esperados;
- histórico de commits anterior à migração;
- presença de um merge de integração entre o histórico filtrado e a inicialização do destino;
- execução dos scripts de reprodução;
- metadados `CITATION.cff`, Zenodo e DOI quando aplicáveis;
- workflows compatíveis com os novos caminhos de raiz.

## Ajustes específicos

### Dependência de Fornecedores e Compras Públicas

Após a migração, revisar workflows que atualmente utilizam caminhos iniciados por `research/dependencia-fornecedores-compras-publicas/`. No novo repositório, esses caminhos passam a partir da raiz.

### Dinâmica de Manada Organizacional

Revisar referências internas ao caminho `research/dinamica-manada-organizacional/`. O `CITATION.cff`, `REPRODUCIBILITY.md` e `ZENODO_RECORD.json` já residem no diretório do projeto e devem migrar junto com o histórico.

### Modelo Axion Lotofácil

O diretório `lotofacil_axion/` já recebeu cópias locais de `CITATION.cff` e `.zenodo.json`. Após a migração, revisar URLs que ainda apontam para `Jacson-Nascimento/Jacson-Nascimento` e para a release histórica do repositório de origem.

## Repositório de perfil após a migração

A separação não exige apagar os diretórios históricos do repositório de perfil. Eles podem permanecer como registro de origem, com avisos de que a continuidade passou aos repositórios dedicados.

O `README.md`, `GOVERNANCE.md` e `research/README.md` devem ser atualizados somente depois de validar os três destinos.
