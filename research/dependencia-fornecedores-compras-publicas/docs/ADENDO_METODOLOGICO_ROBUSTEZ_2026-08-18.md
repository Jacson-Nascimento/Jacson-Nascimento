# Adendo Metodológico de Robustez — 18/08/2026

## Status

Este documento registra decisões empíricas adotadas após os testes de robustez de janeiro–fevereiro de 2025. Nos pontos em que houver conflito, este adendo prevalece sobre `METODOLOGIA_REESPECIFICADA.md` até a consolidação da próxima versão integral da metodologia.

## 1. PortfolioHHI bruto e HHI normalizado

O `PortfolioHHI` permanece como medida principal de concentração monetária da carteira:

`PortfolioHHI_bt = Σ_s q_bst²`

Como o piso mecânico do HHI depende do número `N_bt` de fornecedores observados, será calculada obrigatoriamente uma versão normalizada para `N_bt > 1`:

`PortfolioHHI_norm_bt = (PortfolioHHI_bt - 1/N_bt) / (1 - 1/N_bt)`

Interpretação:

- `0`: distribuição monetária uniforme entre os `N_bt` fornecedores observados;
- valores próximos de `1`: forte dominância de um fornecedor;
- o indicador não mede competição antitruste nem define mercado relevante.

A mesma normalização poderá ser aplicada a `CountHHI`:

`CountHHI_norm_bt = (CountHHI_bt - 1/N_bt) / (1 - 1/N_bt)`

O artigo reportará, no mínimo:

- PortfolioHHI bruto;
- PortfolioHHI normalizado;
- CountHHI;
- CountHHI normalizado;
- CR1;
- CR4;
- número efetivo de fornecedores.

## 2. Sensibilidade ao critério de elegibilidade

O corte diagnóstico inicial `N_fornecedores >= 3` e `N_instrumentos >= 5` não será tratado como parâmetro natural ou universal.

Os resultados deverão ser reapresentados para, no mínimo:

1. `3 fornecedores / 5 instrumentos`;
2. `5 fornecedores / 10 instrumentos`;
3. `5 fornecedores / 20 instrumentos`;
4. `10 fornecedores / 20 instrumentos`.

Os testes janeiro–fevereiro mostraram que o nível absoluto do HHI é sensível ao tamanho mínimo da carteira. Portanto, não se apresentará uma única mediana de HHI como estimativa invariável do universo sem análise de sensibilidade.

Em contraste, os testes preliminares mostraram estabilidade em três padrões que deverão ser reavaliados na base anual:

- concentração monetária superior à concentração por frequência em aproximadamente 98% dos compradores elegíveis;
- presença do quadrante de baixa concentração relativa e alta exposição estrutural em aproximadamente 13%–15%;
- associação positiva entre HHI normalizado e exposição estrutural nos diferentes cortes.

A escolha definitiva do corte principal somente será feita após a coleta anual e não poderá ser orientada por maximização do efeito encontrado.

## 3. Rede global como referência para centralidade

A classificação principal dos fornecedores por centralidade será calculada na **rede global observada** do período, antes da seleção da subamostra de compradores usada para avaliar impacto.

Para fornecedor `s` no período `t`:

`Degree_st = |{b : V_bst > 0}|`

`Strength_st = Σ_b V_bst`

Essas medidas serão calculadas usando todos os compradores e fornecedores que satisfizerem os filtros gerais da base pública/analítica, e não apenas os compradores do corte de elegibilidade usado em uma tabela específica.

A especificação que recalcula degree/strength apenas dentro da subamostra elegível será mantida como teste de robustez.

Justificativa: classificar um fornecedor como “sistêmico” a partir da mesma subamostra sobre a qual o impacto é medido pode tornar o ranking excessivamente endógeno à seleção analítica. O ranking global reduz esse problema de construção.

## 4. Simulações de choque

Para conjunto removido `R`:

`Loss_bt(R) = Σ_{s∈R} q_bst`

Para limiar `τ`:

`Severe_t(R,τ) = (1/N_B) Σ_b I[Loss_bt(R) >= τ]`

A especificação principal deverá comparar:

1. remoção aleatória no universo global de fornecedores observados;
2. remoção direcionada pelos maiores `Degree` globais;
3. remoção direcionada pelos maiores `Strength` globais.

Cenários mínimos:

- 1% dos fornecedores;
- 5%;
- 10%.

Limiar de perda mínimo a reportar:

- `τ = 0,25`;
- `τ = 0,50`;
- `τ = 0,75`.

Para cada cenário aleatório serão utilizadas inicialmente 1.000 repetições, com semente registrada para replicabilidade. A versão final poderá ampliar as repetições se a precisão empírica exigir.

Serão reportados:

- média sob remoção aleatória;
- intervalo empírico de 95%;
- resultado direcionado;
- excesso de exposição em relação à média aleatória;
- perda média de carteira.

A linguagem será “exposição contratual simulada” ou “vulnerabilidade estrutural”, nunca interrupção comprovada de serviços.

## 5. Especificação principal e robustez

### Principal

- comprador: CNPJ institucional;
- fornecedor: PJ na base pública identificada;
- período anual por data de assinatura, com coleta estendida de publicações tardias;
- PortfolioHHI bruto e normalizado;
- ranking de fornecedores na rede global;
- impacto medido em compradores que satisfazem o critério de elegibilidade definido ex ante após a análise anual;
- simulação aleatória versus direcionada.

### Robustez

- diferentes cortes de elegibilidade;
- ranking recalculado apenas na rede elegível;
- inclusão agregada de PF/PE na base privada;
- exclusão de lags temporais inconsistentes;
- valor inicial versus especificações alternativas de valor;
- exclusão/inclusão de compras compartilhadas;
- comprador institucional versus agregações territoriais adequadas;
- diferentes limiares de perda.

## 6. Integração fiscal

O SICONFI/DCA entra como controle territorial apenas quando a associação entre CNPJ comprador e município for não ambígua no período analisado.

A razão:

`ProcurementIntensity_it = ValorContratadoPNCP_it / DespesaEmpenhadaSICONFI_it`

é medida de escala/diagnóstico e não identidade contábil. Em coortes parciais de publicação ela não será utilizada para interpretação substantiva do nível, pois o numerador é incompleto enquanto o denominador fiscal é anual.

## 7. Regra de interpretação

Nenhuma medida isolada será tratada como prova de irregularidade. O desenho pretende medir dependência financeira, recorrência e exposição estrutural. Especialização, escala, exclusividade, contratos de grande porte, estrutura regional de oferta e compras compartilhadas podem produzir concentração legítima.

## 8. Decisões que ficam pendentes da base anual

- corte principal definitivo de elegibilidade;
- número final de simulações aleatórias;
- tratamento principal de instrumentos com lag negativo;
- especificação final de valores contratuais;
- inclusão de categorias administrativas como controles;
- modelos econométricos finais;
- eventual construção de índice composto, que continua vedada sem validação de dimensionalidade e pesos.
