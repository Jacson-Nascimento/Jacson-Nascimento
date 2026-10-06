# Metodologia

## 1. Princípio de dados públicos

O estudo é desenhado para ser reproduzível por qualquer pesquisador sem vínculo funcional com a CAIXA. Nenhuma etapa depende de credencial corporativa, sistema interno ou dado confidencial.

A regra de admissibilidade é simples: se um terceiro não consegue localizar a fonte pública registrada no projeto canônico, o dado não deve fundamentar resultado do artigo.

## 2. Hierarquia das fontes

A prioridade é:

1. documento institucional público da CAIXA ou órgão governamental, P1;
2. publicação pública da entidade sindical que realizou a assembleia ou representa a base, P2;
3. fonte pública secundária que reproduz dado institucional, P3;
4. reconstruções aritméticas, M1;
5. modelos de alocação, M2.

Quando duas fontes divergem, não é permitido escolher silenciosamente a que produz o resultado desejado. A divergência deve ser registrada e, se material, submetida a análise de sensibilidade.

## 3. Âncora nacional

A versão preliminar usa 84.136 empregados em junho de 2026, valor divulgado publicamente em fonte secundária que reproduz resultados da CAIXA. Como a fonte primária correspondente ainda não foi incorporada ao projeto, esse parâmetro permanece classificado como P3.

## 4. Distribuição por UF

Não foi localizada uma tabela pública contemporânea com o quadro de empregados da CAIXA para as 27 UFs em 2026. Por isso, o projeto não apresenta a distribuição estadual como observada.

São calculados dois modelos.

### M2, modelo preferencial nesta fase

1. usar os empregados permanentes por região divulgados pela CAIXA em 2024;
2. escalar os cinco totais regionais para a âncora nacional de junho de 2026;
3. dentro de cada região, repartir o total entre as UFs com base na participação observada no 33º CONECEF de 2017;
4. aplicar método dos maiores restos para que todos os resultados sejam inteiros e a soma nacional seja exatamente 84.136.

Formalmente:

`R_2026_hat = N_2026 * R_2024 / soma(R_2024)`

`UF_2026_hat = R_2026_hat * UF_2017 / soma(UF_2017 na região)`

Os arredondamentos são reconciliados por maiores restos.

### M3, modelo de sensibilidade

O total nacional de 2026 é distribuído diretamente pelas participações estaduais observadas em 2017:

`UF_2026_M3 = N_2026 * UF_2017 / soma(UF_2017)`

A diferença M2 versus M3 deve ser publicada no projeto canônico. Essa diferença não é intervalo de confiança. É uma medida de sensibilidade do resultado à escolha do padrão territorial.

## 5. Base sindical

A UF não é considerada equivalente a uma base sindical. O projeto rejeita rateios automáticos por população, número de municípios ou agências quando não houver justificativa pública.

São aceitos os seguintes casos:

### Contagem direta

Quando o sindicato publica o número de empregados aptos a votar, esse número é registrado como ponto observado da base, P2.

### Reconstrução aritmética, M1

Quando são publicados número de votantes e taxa de participação, o número de aptos pode ser reconstruído:

`aptos_hat = arredondar(votantes / taxa_de_participacao)`

### Intervalo

Se a publicação informa que um número de votantes representa mais de determinada taxa da base, o projeto registra um intervalo, e não um ponto.

### Somente limite inferior

Se há número de votantes, mas não taxa de participação, o número observado é somente um limite inferior do universo elegível.

### Sem denominador

Percentuais de aprovação ou rejeição sem contagem de votos ou taxa de participação não permitem inferir o número de empregados.

## 6. Contribuição negocial

A versão preliminar registra a regra publicamente reproduzida pelas entidades sindicais após a sentença normativa de 2026:

- 1,5% sobre a base remuneratória definida na decisão;
- piso de R$ 63 e teto de R$ 310 para a contribuição sobre remuneração fixa;
- sobre a PLR, 1,5%, sem piso, limitada a R$ 262,30 por pagamento;
- 70% destinados ao sindicato da base;
- 15% à federação;
- 10% à confederação;
- 5% à central sindical;
- direito de oposição conforme regras divulgadas.

Antes do artigo final, deve ser incorporada ao projeto canônico uma fonte pública primária do processo no TST, se tecnicamente acessível, para substituir ou confirmar as reproduções sindicais.

## 7. Fórmulas de receita potencial

Para um universo elegível `E`, taxa de oposição hipotética `o`, valor individual `c` e parcela do sindicato `s = 0,70`:

`receita_sindicato = E * (1 - o) * c * s`

A análise nacional deve publicar cenários para:

- piso normativo, R$ 63;
- cenário de referência preliminar, R$ 235,54, sempre rotulado como não observado;
- teto da remuneração fixa, R$ 310;
- teto de PLR por pagamento, R$ 262,30.

A taxa real de oposição não é presumida. São apresentados apenas cenários hipotéticos.

## 8. O que os resultados não medem

Os cálculos não são:

- receita contábil efetivamente recebida por cada sindicato;
- estimativa da taxa real de oposição;
- quadro oficial de empregados da CAIXA por UF em 2026;
- número oficial de empregados por base sindical, salvo quando a própria fonte pública fornece o denominador;
- demonstração de filiação sindical;
- apuração de valores individuais de empregados.

## 9. RAIS

Os microdados públicos de RAIS e CAGED são tratados apenas dentro das condições de acesso e identificação formalmente publicadas pelo MTE. O projeto não presume que seja possível isolar a CAIXA como empregador quando a versão pública disponibilizada não permitir identificação direta. Bases sujeitas a acordo de acesso ou restrição não atendem à regra deste estudo e não serão utilizadas.