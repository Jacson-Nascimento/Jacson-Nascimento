param(
    [string]$GitHubUser = "Jacson-Nascimento",
    [string]$SourceRepoPath = ".",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$migrations = @(
    @{
        SourceBranch = "research/artigo-primeiro-semestre-2025"
        Prefix       = "research/dependencia-fornecedores-compras-publicas"
        TargetRepo   = "dependencia-fornecedores-compras-publicas"
        TargetBranch = "paper/artigo-primeiro-semestre-2025"
        LegacyPR     = 62
    },
    @{
        SourceBranch = "research/pncp-2025-08"
        Prefix       = "research/dependencia-fornecedores-compras-publicas"
        TargetRepo   = "dependencia-fornecedores-compras-publicas"
        TargetBranch = "data/pncp-2025-08"
        LegacyPR     = 56
    },
    @{
        SourceBranch = "research/pncp-restante-2025-rotina"
        Prefix       = "research/dependencia-fornecedores-compras-publicas"
        TargetRepo   = "dependencia-fornecedores-compras-publicas"
        TargetBranch = "data/pncp-restante-2025-rotina"
        LegacyPR     = 60
    },
    @{
        SourceBranch = "agent/lotofacil-reprodutibilidade-v12"
        Prefix       = "lotofacil_axion"
        TargetRepo   = "modelo-axion-lotofacil"
        TargetBranch = "release/reprodutibilidade-v1.2"
        LegacyPR     = 61
    },
    @{
        SourceBranch = "research/pncp-piloto-2025-run"
        Prefix       = "research/dependencia-fornecedores-compras-publicas"
        TargetRepo   = "dependencia-fornecedores-compras-publicas"
        TargetBranch = "legacy/pncp-piloto-2025-run"
        LegacyPR     = 5
    }
)

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar: git $($Arguments -join ' ')"
    }
}

Push-Location (Resolve-Path $SourceRepoPath)
try {
    if (-not (Test-Path ".git")) {
        throw "Execute este script na raiz do clone Jacson-Nascimento/Jacson-Nascimento."
    }

    $pending = & git status --porcelain
    if ($LASTEXITCODE -ne 0) { throw "Não foi possível verificar o estado do repositório." }
    if ($pending) { throw "A árvore de trabalho possui alterações locais. Preserve-as antes de continuar." }

    Write-Host "Migração não destrutiva das branches ativas" -ForegroundColor Cyan
    Write-Host "Nenhuma branch, PR, arquivo ou histórico da origem será removido."
    Write-Host "Nenhuma branch existente no destino será sobrescrita."

    foreach ($item in $migrations) {
        $sourceBranch = $item.SourceBranch
        $prefix = $item.Prefix
        $targetRepo = $item.TargetRepo
        $targetBranch = $item.TargetBranch
        $legacyPR = $item.LegacyPR
        $remoteName = "target-$targetRepo"
        $remoteUrl = "https://github.com/$GitHubUser/$targetRepo.git"

        Write-Host ""
        Write-Host "PR antiga #$legacyPR | $sourceBranch" -ForegroundColor Yellow
        Write-Host "Destino: $targetRepo -> $targetBranch"

        if ($DryRun) {
            Write-Host "DRY RUN: nenhuma alteração executada."
            continue
        }

        Invoke-Git -Arguments @("fetch", "origin", $sourceBranch)
        $sourceSha = (& git rev-parse "origin/$sourceBranch").Trim()
        if (-not $sourceSha) { throw "Não foi possível identificar a origem $sourceBranch." }
        $shortSha = $sourceSha.Substring(0, 12)
        $safeTarget = $targetBranch -replace "[^A-Za-z0-9._-]", "-"
        $splitBranch = "migration-active/$safeTarget-$shortSha"

        $localExists = & git show-ref --verify --quiet "refs/heads/$splitBranch"
        if ($LASTEXITCODE -ne 0) {
            Invoke-Git -Arguments @("subtree", "split", "--prefix=$prefix", "-b", $splitBranch, "origin/$sourceBranch")
        }
        else {
            Write-Host "Branch local de preservação já existe: $splitBranch"
        }

        $remotes = @(& git remote)
        if ($remotes -contains $remoteName) {
            Invoke-Git -Arguments @("remote", "set-url", $remoteName, $remoteUrl)
        }
        else {
            Invoke-Git -Arguments @("remote", "add", $remoteName, $remoteUrl)
        }

        & git ls-remote $remoteUrl *> $null
        if ($LASTEXITCODE -ne 0) { throw "Destino não acessível: $remoteUrl" }

        $existingTarget = & git ls-remote --heads $remoteUrl "refs/heads/$targetBranch"
        if ($LASTEXITCODE -ne 0) { throw "Não foi possível consultar $targetBranch em $targetRepo." }

        if ($existingTarget) {
            Write-Host "ATENÇÃO: a branch de destino já existe e foi preservada. Nenhum push foi feito." -ForegroundColor Yellow
            continue
        }

        Invoke-Git -Arguments @("push", $remoteName, "$splitBranch`:refs/heads/$targetBranch")
        Write-Host "Branch migrada: $targetRepo/$targetBranch" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Migração das branches concluída. A origem permanece intacta." -ForegroundColor Green
    Write-Host "Os workflows externos às pastas dos projetos serão tratados separadamente após a validação das branches."
}
finally {
    Pop-Location
}
