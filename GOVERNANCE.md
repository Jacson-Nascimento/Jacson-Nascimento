# Governança dos repositórios

Este documento estabelece a organização dos projetos mantidos na conta `Jacson-Nascimento`.

## Princípios

1. O repositório `Jacson-Nascimento/Jacson-Nascimento` tem função principal de perfil, índice, identidade acadêmica e registro histórico.
2. Projetos científicos independentes possuem repositórios próprios quando atingem maturidade operacional suficiente.
3. Pesquisas em elaboração podem permanecer privadas até a decisão de divulgação.
4. Código, dados publicáveis, documentação metodológica, resultados e materiais de reprodução devem ser versionados de forma rastreável.
5. Metadados de citação e integração com Zenodo devem pertencer ao projeto a que se referem.
6. Nenhum conteúdo histórico deve ser removido como parte de reorganizações. Migrações devem preservar a origem, referências, commits e registros existentes.
7. O repositório público de perfil não deve funcionar como armazenamento operacional de bases de pesquisa.

## Arquitetura vigente desde 23/08/2026

- `Jacson-Nascimento/Jacson-Nascimento`: perfil, índice e registro histórico público.
- `Jacson-Nascimento/ciclos-eleitorais-bancos`: pesquisa privada e canônica sobre ciclos eleitorais e desempenho bancário.
- `Jacson-Nascimento/dependencia-fornecedores-compras-publicas`: repositório dedicado da pesquisa de dependência estrutural de fornecedores. Privado durante a continuidade do desenvolvimento e validação pós-migração.
- `Jacson-Nascimento/dinamica-manada-organizacional`: repositório dedicado do pacote de reprodução do estudo de dinâmica de manada organizacional.
- `Jacson-Nascimento/modelo-axion-lotofacil`: repositório público dedicado do Modelo Axion Lotofácil e de seus pacotes de reprodutibilidade.
- `Jacson-Nascimento/lab-natty-or-not-`: laboratório histórico, sem desenvolvimento científico ativo.

A separação dos projetos anteriormente aninhados no repositório de perfil foi concluída em 23/08/2026 por migração não destrutiva com `git subtree split`. O histórico relevante foi preservado nos novos repositórios e as cópias de origem foram mantidas para rastreabilidade.

Branches de trabalho relacionadas às PRs históricas #5, #56, #60, #61 e #62 também foram preservadas em branches equivalentes nos novos repositórios.

Em 23/08/2026, as PRs históricas #5, #56, #60, #61 e #62 do repositório de perfil foram encerradas sem merge, após a continuidade ter sido registrada nos repositórios canônicos. Nenhuma branch, commit ou evidência foi apagada.

## Política de branches

Novos trabalhos devem preferir branches curtas e orientadas a uma finalidade clara:

- `feature/...` para funcionalidades e automações;
- `analysis/...` para análises;
- `data/...` para rotinas de coleta e tratamento;
- `paper/...` para manuscritos e documentação editorial;
- `release/...` para pacotes de reprodução e versões de publicação;
- `governance/...` para organização e governança;
- `legacy/...` para preservação explícita de trabalho histórico que não representa desenvolvimento corrente.

Branches históricas já existentes são preservadas. A redução do conjunto de branches operacionais deve ocorrer apenas por política futura que não elimine evidências ou histórico necessário.

## Pull requests

Mudanças relevantes de método, coleta, modelagem ou publicação devem continuar sendo registradas por pull request, com objetivo, alterações, validações, limitações e decisão de continuidade.

Após a migração, novas PRs devem ser abertas no repositório canônico de cada projeto. PRs antigas do repositório de perfil funcionam como registro histórico de proveniência e podem ser encerradas sem merge quando houver sucessora canônica claramente identificada.

Uma PR de natureza `legacy` deve permanecer aberta apenas quando houver decisão operacional pendente. Se a finalidade for exclusivamente preservar evidência e rastreabilidade, a PR pode ser encerrada sem merge, mantendo branch, commits e documentação.

No projeto `ciclos-eleitorais-bancos`, a PR #1 foi encerrada em 23/08/2026 como etapa sucedida pela PR #2, que permanece como referência científica corrente.

## Metadados científicos

Cada projeto independente deve manter, conforme aplicável:

- `README.md`;
- `CITATION.cff`;
- `REPRODUCIBILITY.md`;
- licença ou aviso de licença;
- ambiente ou dependências;
- referência ao Zenodo e DOI;
- manifesto ou checksums quando houver artefatos de reprodução.

Links de `repository-code` e documentação operacional devem apontar para o repositório canônico vigente. Links para releases históricas podem continuar apontando para o repositório de origem quando aquele release permanece materialmente hospedado lá.

## Privacidade e dados públicos

A visibilidade do repositório deve refletir o estágio do trabalho e o conteúdo armazenado. Bases ou materiais com restrições de divulgação não devem ser publicados apenas para facilitar a reprodução.

A classificação de um fornecedor como pessoa jurídica não elimina a necessidade de revisão textual do registro, pois nomes empresariais podem incorporar elementos identificáveis de pessoas naturais.

O repositório público de perfil não deve receber novas bases brutas, bases processadas, checkpoints ou arquivos operacionais da pesquisa de dependência de fornecedores. O `.gitignore` e o workflow `public-data-guard` funcionam como controles preventivos para esse legado.

A política detalhada está em `PUBLIC_DATA_POLICY.md`.

Projetos com DOI e pacote público de reprodução devem, quando não houver restrição de conteúdo, preferencialmente manter repositório público para coerência com a documentação científica.

## Configuração administrativa desejada

Para repositórios públicos científicos ativos, a configuração alvo é:

- branch `main` protegida contra alterações acidentais e force push;
- mudanças relevantes preferencialmente por pull request;
- verificações de CI exigidas quando houver workflow de validação;
- descrição do repositório coerente com o objeto científico;
- tópicos que representem área, método e linguagem principal.

O repositório `lab-natty-or-not-` deve ser tratado como arquivo histórico e, quando a configuração administrativa permitir, marcado como arquivado sem exclusão do conteúdo.
