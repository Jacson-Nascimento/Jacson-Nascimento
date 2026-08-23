# Migração das PRs e branches ativas

A migração do `main` para repositórios dedicados foi concluída em 23/08/2026. Este documento trata do trabalho que ainda permanecia aberto no repositório de perfil no momento da separação.

## Branches a preservar nos novos repositórios

| PR antiga | Branch de origem | Novo repositório | Nova branch |
|---|---|---|---|
| #62 | `research/artigo-primeiro-semestre-2025` | `dependencia-fornecedores-compras-publicas` | `paper/artigo-primeiro-semestre-2025` |
| #56 | `research/pncp-2025-08` | `dependencia-fornecedores-compras-publicas` | `data/pncp-2025-08` |
| #60 | `research/pncp-restante-2025-rotina` | `dependencia-fornecedores-compras-publicas` | `data/pncp-restante-2025-rotina` |
| #61 | `agent/lotofacil-reprodutibilidade-v12` | `modelo-axion-lotofacil` | `release/reprodutibilidade-v1.2` |
| #5 | `research/pncp-piloto-2025-run` | `dependencia-fornecedores-compras-publicas` | `legacy/pncp-piloto-2025-run` |

## Procedimento

Na raiz do clone local atualizado:

```powershell
git switch main
git pull --ff-only origin main
.\tools\migrate_active_pr_branches.ps1 -DryRun
```

Após conferir a listagem:

```powershell
.\tools\migrate_active_pr_branches.ps1
```

A rotina usa `git subtree split` em cada branch de origem, preserva o histórico relacionado ao diretório do projeto e cria uma nova branch no repositório dedicado. Ela não fecha PRs antigas, não elimina branches, não usa `--force` e não sobrescreve branches já existentes no destino.

## Workflows fora dos diretórios dos projetos

Duas PRs possuem workflows na raiz do repositório antigo, portanto esses arquivos não entram automaticamente no `subtree split`:

- PR #60: `.github/workflows/pncp-mensal-restante-2025.yml`;
- PR #61: `.github/workflows/lotofacil-v12-pr-validation.yml` e `.github/workflows/lotofacil-v12-reproducibility.yml`.

Depois que as novas branches forem confirmadas no destino, esses workflows devem ser copiados para as respectivas branches e ter seus caminhos ajustados para a nova raiz do projeto.

## Continuidade

As PRs antigas permanecem como evidência histórica. A continuidade operacional deve passar às novas PRs abertas nos repositórios dedicados somente depois de validar as branches migradas e os workflows adaptados.
