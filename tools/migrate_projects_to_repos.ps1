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

    $originalBranch = (& git branch --show-current).Trim()
    if (-not $originalBranch) {
        throw "Não foi possível identificar a branch atual."
    }

    $sourceHead = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $sourceHead) {
        throw "Não foi possível identificar o commit atual da origem."
    }

    $shortSourceHead = $sourceHead.Substring(0, 12)

    Write-Host "Migração não destrutiva de projetos" -ForegroundColor Cyan
    Write-Host "Origem: $sourceHead"
    Write-Host "Nenhum arquivo, branch ou histórico do repositório de origem será removido."
    Write-Host "Os destinos podem estar vazios ou conter apenas commits de inicialização e proveniência."

    foreach ($project in $projects) {
        $prefix = $project.Prefix
        $repo = $project.Repo
        $safeName = $repo -replace "[^A-Za-z0-9._-]", "-"
        $splitBranch = "migration/$safeName-$shortSourceHead"
        $mergeBranch = "migration-merge/$safeName-$shortSourceHead"
        $remoteName = "target-$safeName"
        $remoteUrl = "https://github.com/$GitHubUser/$repo.git"

        if (-not (Test-Path $prefix)) {
            throw "Diretório de origem não encontrado: $prefix"
        }

        Write-Host ""
        Write-Host "Projeto: $repo" -ForegroundColor Yellow
        Write-Host "Origem:  $prefix"
        Write-Host "Destino: $remoteUrl"
        Write-Host "Branch de histórico filtrado: $splitBranch"
        Write-Host "Branch de integração: $mergeBranch"

        if ($DryRun) {
            Write-Host "DRY RUN: nenhuma alteração executada."
            continue
        }

        $splitExists = & git show-ref --verify --quiet "refs/heads/$splitBranch"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Branch de histórico filtrado já existe. Ela será preservada e reutilizada."
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

        $remoteMain = & git ls-remote --heads $remoteUrl refs/heads/main
        if ($LASTEXITCODE -ne 0) {
            throw "Não foi possível consultar a branch main do destino: $remoteUrl"
        }

        if ($remoteMain) {
            Invoke-Git -Arguments @("fetch", $remoteName, "main")

            $mergeExists = & git show-ref --verify --quiet "refs/heads/$mergeBranch"
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Branch de integração já existe. Ela será preservada e reutilizada."
                Invoke-Git -Arguments @("switch", $mergeBranch)
            }
            else {
                Invoke-Git -Arguments @("switch", "-c", $mergeBranch, $splitBranch)
            }

            $remoteMainSha = (& git rev-parse "$remoteName/main").Trim()
            $remoteAlreadyMerged = & git merge-base --is-ancestor $remoteMainSha HEAD

            if ($LASTEXITCODE -eq 0) {
                Write-Host "O commit atual do destino já está incorporado à branch de integração."
            }
            else {
                Invoke-Git -Arguments @(
                    "merge",
                    "--allow-unrelated-histories",
                    "--no-ff",
                    "$remoteName/main",
                    "-m",
                    "Migra histórico de $repo preservando inicialização do destino"
                )
            }

            Invoke-Git -Arguments @("push", $remoteName, "$mergeBranch`:refs/heads/main")
            Invoke-Git -Arguments @("switch", $originalBranch)
        }
        else {
            Invoke-Git -Arguments @("push", $remoteName, "$splitBranch`:refs/heads/main")
        }

        Write-Host "Migração concluída para $repo. O histórico filtrado e os commits já existentes no destino foram preservados." -ForegroundColor Green
    }

    Invoke-Git -Arguments @("switch", $originalBranch)

    Write-Host ""
    Write-Host "Processo concluído. O repositório de origem permanece intacto." -ForegroundColor Green
    Write-Host "Após validar os novos repositórios, atualize links, metadados e workflows conforme docs/MIGRATION_REPOSITORIES.md."
}
finally {
    Pop-Location
}
