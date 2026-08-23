# Migração não destrutiva para repositórios dedicados

Este runbook conclui a separação dos projetos atualmente mantidos no repositório de perfil.

## Repositórios de destino

Criar no GitHub, vazios e sem README, licença ou `.gitignore` inicial:

1. `Jacson-Nascimento/dependencia-fornecedores-compras-publicas`
2. `Jacson-Nascimento/dinamica-manada-organizacional`
3. `Jacson-Nascimento/modelo-axion-lotofacil`

Os três projetos já possuem conteúdo público no repositório de origem. A visibilidade pública preserva o estado atual de divulgação. Caso haja decisão editorial diferente antes da criação, a visibilidade pode ser ajustada no próprio GitHub sem alterar o procedimento de migração.

## Objetivo técnico

A migração usa `git subtree split` para reconstruir, em cada repositório de destino, o histórico de commits relacionado ao respectivo diretório. O repositório de origem permanece intacto.

Não são executados comandos de exclusão de arquivos, branches, tags ou diretórios.

## Pré-requisitos

- Git instalado e disponível no PowerShell.
- Clone local atualizado de `Jacson-Nascimento/Jacson-Nascimento`.
- Credencial do GitHub configurada no Git Credential Manager, GitHub CLI ou mecanismo equivalente.
- Repositórios de destino já criados e vazios.
- Árvore de trabalho local sem alterações pendentes.

## Validação prévia

Na raiz do clone local:

```powershell
git status
git pull --ff-only origin main
.\tools\migrate_projects_to_repos.ps1 -DryRun
```

O `DryRun` apenas lista os projetos e destinos. Não cria branches nem envia commits.

## Execução

```powershell
.\tools\migrate_projects_to_repos.ps1
```

O script:

1. valida que está em um repositório Git;
2. exige árvore de trabalho limpa;
3. localiza cada diretório de projeto;
4. cria uma branch de preservação `migration/...` por projeto usando `git subtree split`;
5. registra um remote específico para cada novo repositório;
6. verifica acesso ao destino;
7. envia o histórico filtrado para a branch `main` do novo repositório;
8. preserva integralmente o repositório de origem e as branches de migração.

## Validação após a migração

Em cada novo repositório, confirmar:

- presença do `README.md` do projeto;
- presença dos scripts e dados publicáveis esperados;
- histórico de commits anterior à migração;
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
