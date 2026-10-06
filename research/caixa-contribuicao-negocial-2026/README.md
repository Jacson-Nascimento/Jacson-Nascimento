# CAIXA 2026: contribuição negocial por base sindical

Status: projeto de pesquisa em desenvolvimento.

Este diretório funciona apenas como **registro, índice e documentação metodológica** do projeto no repositório público de perfil.

Conforme `PUBLIC_DATA_POLICY.md`, as bases brutas, bases processadas, scripts operacionais, testes e outputs analíticos deste estudo não serão armazenados neste repositório. Esses artefatos deverão ser versionados em repositório canônico próprio.

## Escopo

Construir, exclusivamente a partir de fontes públicas, uma estimativa reprodutível da distribuição de empregados da Caixa Econômica Federal por UF e, quando houver evidência suficiente, por base territorial de sindicatos dos bancários, para avaliar cenários da contribuição negocial de 2026.

O estudo também examinará, de forma neutra, a literatura sobre financiamento sindical, ação coletiva, free riding, liberdade de associação, direito de oposição, densidade sindical e capacidade de barganha. O objetivo não é defender contribuição ou oposição, mas mensurar possíveis efeitos financeiros das escolhas institucionais e discutir os mecanismos sugeridos pela literatura sem extrapolar causalidade.

## Regra de dados

- somente fontes publicamente acessíveis;
- nenhum dado de intranet, sistema interno, relatório restrito ou acesso funcional à CAIXA;
- nenhuma lista interna de empregados, lotações ou matrículas;
- nenhum dado pessoal identificável;
- nenhuma informação obtida por canal privado ou documento vazado;
- toda estimativa deve registrar fonte, fórmula, hipótese e nível de evidência;
- lacunas permanecem como não estimadas quando não houver base pública defensável.

Se um número for conhecido por qualquer outro meio, mas não puder ser sustentado por fonte pública acessível a terceiros, ele não entra na base nem no artigo.

## Classificação de evidência

| Código | Significado |
|---|---|
| P1 | fonte pública institucional primária, como CAIXA, TST ou MTE |
| P2 | publicação pública direta de sindicato, federação, confederação ou entidade representativa |
| P3 | fonte pública secundária que reproduz dado institucional, pendente de confirmação primária quando possível |
| M1 | reconstrução aritmética feita somente a partir de números públicos |
| M2 | estimativa modelada combinando fontes públicas de anos ou níveis territoriais diferentes |

Os códigos M1 e M2 identificam resultados derivados. Eles não transformam estimativas em dados observados.

## Documentação metodológica e bibliográfica

- [`docs/METODOLOGIA.md`](docs/METODOLOGIA.md): regras de admissibilidade, hierarquia das fontes, modelos M2 e M3, tratamento das bases sindicais e fórmulas financeiras.
- [`docs/DECISOES_METODOLOGICAS.md`](docs/DECISOES_METODOLOGICAS.md): decisões que alteraram ou restringiram estimativas preliminares.
- [`docs/LIMITACOES_E_PENDENCIAS.md`](docs/LIMITACOES_E_PENDENCIAS.md): lacunas que precisam ser tratadas antes da redação do artigo.
- [`docs/REVISAO_LITERATURA.md`](docs/REVISAO_LITERATURA.md): revisão crítica preliminar da literatura brasileira e internacional, marco jurisprudencial e lacuna de pesquisa.
- [`docs/MATRIZ_REFERENCIAS.md`](docs/MATRIZ_REFERENCIAS.md): método, achado, posição predominante, uso permitido e limitação de cada referência central.

## Situação em 06/10/2026

A infraestrutura metodológica e o conjunto inicial de fontes foram preparados e validados fora deste repositório de perfil. O pacote de trabalho possui controles de reconciliação, reconstrução de denominadores, intervalos e cenários financeiros.

A revisão bibliográfica preliminar identificou literatura suficiente para sustentar as duas posições relevantes ao problema: necessidade de financiamento da representação coletiva e proteção da autonomia individual pelo direito de oposição. Não foi localizado, até esta etapa, estudo brasileiro publicado que mensure de forma reprodutível a exposição financeira das entidades sindicais ao exercício da oposição por base territorial dentro de um grande empregador nacional. Essa formulação será tratada como lacuna provisória, sujeita a atualização.

Nesta fase, os pontos prioritários são:

1. confirmar o dissídio em fonte pública primária do TST;
2. confirmar o quadro nacional de empregados em fonte pública primária da CAIXA;
3. ampliar os denominadores públicos das maiores bases sindicais;
4. construir o mapa territorial das bases representativas;
5. atualizar a situação do Tema 935 e do IRDR Tema 02 antes do fechamento do artigo;
6. manter como `NA` qualquer lacuna sem evidência pública suficiente.

## Repositório canônico

Nome planejado: `caixa-contribuicao-negocial-2026`.

O repositório canônico ainda não está disponível entre os repositórios acessíveis pela integração utilizada nesta etapa. Até sua criação, este diretório não receberá bases, scripts ou resultados operacionais.
