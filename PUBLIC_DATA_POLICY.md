# Política de dados do repositório público

Este repositório tem função principal de perfil, índice acadêmico e registro histórico. Não deve ser utilizado como armazenamento operacional de bases de pesquisa.

## Regra vigente desde 23/08/2026

1. Novas bases brutas ou processadas de projetos científicos devem ser versionadas apenas no respectivo repositório canônico, observada a visibilidade adequada ao conteúdo.
2. O diretório histórico `research/dependencia-fornecedores-compras-publicas/data/` não deve receber novas bases neste repositório público.
3. Dados destinados à publicação devem ser previamente minimizados e revisados quanto a identificadores pessoais, nomes empresariais que incorporem identificadores numéricos, credenciais, chaves, tokens, e-mails não necessários e outros elementos cuja divulgação não seja necessária à finalidade científica.
4. A classificação de um registro como fornecedor pessoa jurídica não é, isoladamente, critério suficiente para concluir que o texto do registro não contém elemento identificável de pessoa natural.
5. Amostras públicas devem conter somente o mínimo necessário para documentação ou reprodução e devem possuir justificativa metodológica explícita.
6. Bases completas, checkpoints operacionais e arquivos intermediários devem permanecer fora do repositório público de perfil.
7. O histórico já versionado é preservado por razões de proveniência. Qualquer decisão futura de saneamento retroativo do histórico deve ser tratada como procedimento específico de governança, com avaliação prévia de impactos sobre rastreabilidade, DOI, releases, branches e referências existentes.

## Prevenção

O `.gitignore` da raiz bloqueia novas inclusões ordinárias nos diretórios históricos `data/raw` e `data/processed` do projeto de dependência de fornecedores. Arquivos já rastreados pelo Git permanecem preservados e exigem tratamento específico caso se decida por saneamento retroativo.

## Repositório canônico

A continuidade da pesquisa ocorre em `Jacson-Nascimento/dependencia-fornecedores-compras-publicas`, atualmente privado durante a fase de desenvolvimento e validação.
