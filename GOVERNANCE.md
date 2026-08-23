# Governança dos repositórios

Este documento estabelece a organização dos projetos mantidos na conta `Jacson-Nascimento`.

## Princípios

1. O repositório `Jacson-Nascimento/Jacson-Nascimento` tem função principal de perfil, índice e identidade acadêmica.
2. Projetos científicos independentes devem, quando maduros, possuir repositório próprio.
3. Pesquisas em elaboração podem permanecer privadas até a decisão de divulgação.
4. Código, dados publicáveis, documentação metodológica, resultados e materiais de reprodução devem ser versionados de forma rastreável.
5. Metadados de citação e integração com Zenodo devem pertencer ao projeto a que se referem.
6. Nenhum conteúdo histórico deve ser removido como parte de reorganizações. Migrações devem preservar a origem, referências, commits e registros existentes.

## Arquitetura alvo

- `Jacson-Nascimento/Jacson-Nascimento`: perfil e índice público.
- `Jacson-Nascimento/ciclos-eleitorais-bancos`: pesquisa privada e canônica sobre ciclos eleitorais e desempenho bancário.
- `dependencia-fornecedores-compras-publicas`: candidato a repositório independente.
- `dinamica-manada-organizacional`: candidato a repositório independente.
- `modelo-axion-lotofacil`: candidato a repositório independente.

Enquanto os novos repositórios não forem criados, os diretórios existentes neste repositório permanecem como fontes canônicas dos respectivos projetos públicos.

## Política de branches

Novos trabalhos devem preferir branches curtas e orientadas a uma finalidade clara:

- `feature/...` para funcionalidades e automações;
- `analysis/...` para análises;
- `data/...` para rotinas de coleta e tratamento;
- `paper/...` para manuscritos e documentação editorial;
- `governance/...` para organização e governança.

Branches históricas já existentes são preservadas. A redução do conjunto de branches operacionais deve ocorrer apenas por política futura que não elimine evidências ou histórico necessário.

## Pull requests

Mudanças relevantes de método, coleta, modelagem ou publicação devem continuar sendo registradas por pull request, com objetivo, alterações, validações, limitações e decisão de continuidade.

## Metadados científicos

Cada projeto independente deve manter, conforme aplicável:

- `README.md`;
- `CITATION.cff`;
- `REPRODUCIBILITY.md`;
- licença ou aviso de licença;
- ambiente ou dependências;
- referência ao Zenodo e DOI;
- manifesto ou checksums quando houver artefatos de reprodução.

## Privacidade

A visibilidade do repositório deve refletir o estágio do trabalho e o conteúdo armazenado. Bases ou materiais com restrições de divulgação não devem ser publicados apenas para facilitar a reprodução.