param(
    [string]$GitHubUser = "Jacson-Nascimento",
    [string]$SourceRepoPath = ".",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$projects = @(
    @{
        Prefix = "research/dependencia-fornecedores-compras-publicas"
        Repo   = "dependencia-fornecedores-compras-publicas"
    },
    @{
        Prefix = "research/dinamica-manada-organizacional"
        Repo   = "dinamica-manada-organizacional"
    },
    @{
        Prefix = "lotofacil_axion"
        Repo   = "modelo-axion-lotofacil"
    }
)

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar: git $($Arguments -join ' ')"
    }
}

Push-Location (Resolve-Path $SourceRepoPath)

try {
    if (-not (Test-Path ".git")) {
        throw "Execute este script na raiz de um clone Git de Jacson-Nascimento/Jacson-Nascimento."
    }

    Invoke-Git -Arguments @("rev-parse", "--is-inside-work-tree")

    $pending = & git status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw "Não foi possível verificar o estado do repositório."
    }

    if ($pending) {
        throw "A árvore de trabalho possui alterações locais. Faça commit ou preserve essas alterações antes da migração."
    }

    Write-Host "Migração não destrutiva de projetos" -ForegroundColor Cyan
    Write-Host "Nenhum arquivo, branch ou histórico do repositório de origem será removido."
    Write-Host "Os repositórios de destino devem existir e estar vazios, sem README, licença ou .gitignore inicial."

    foreach ($project in $projects) {
        $prefix = $project.Prefix
        $repo = $project.Repo
        $safeName = $repo -replace "[^A-Za-z0-9._-]", "-"
        $splitBranch = "migration/$safeName-2026-08-23"
        $remoteName = "target-$safeName"
        $remoteUrl = "https://github.com/$GitHubUser/$repo.git"

        if (-not (Test-Path $prefix)) {
            throw "Diretório de origem não encontrado: $prefix"
        }

        Write-Host ""
        Write-Host "Projeto: $repo" -ForegroundColor Yellow
        Write-Host "Origem:  $prefix"
        Write-Host "Destino: $remoteUrl"
        Write-Host "Branch de preservação: $splitBranch"

        if ($DryRun) {
            Write-Host "DRY RUN: nenhuma alteração executada."
            continue
        }

        $branchExists = & git show-ref --verify --quiet "refs/heads/$splitBranch"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Branch de migração já existe. Ela será preservada e reutilizada."
        }
        else {
            Invoke-Git -Arguments @("subtree", "split", "--prefix=$prefix", "-b", $splitBranch)
        }

        $remotes = @(& git remote)
        if ($remotes -contains $remoteName) {
            Invoke-Git -Arguments @("remote", "set-url", $remoteName, $remoteUrl)
        }
        else {
            Invoke-Git -Arguments @("remote", "add", $remoteName, $remoteUrl)
        }

        & git ls-remote $remoteUrl *> $null
        if ($LASTEXITCODE -ne 0) {
            throw "O repositório de destino não existe ou não está acessível: $remoteUrl"
        }

        Invoke-Git -Arguments @("push", $remoteName, "$splitBranch`:refs/heads/main")

        Write-Host "Migração concluída para $repo. O histórico filtrado foi preservado no novo repositório." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Processo concluído. O repositório de origem permanece intacto." -ForegroundColor Green
    Write-Host "Após validar os novos repositórios, atualize links, metadados e workflows conforme docs/MIGRATION_REPOSITORIES.md."
}
finally {
    Pop-Location
}
