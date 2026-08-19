# Rotina mensal PNCP — agosto a dezembro de 2025

## Objetivo

Padronizar a captura, validação, consolidação e análise dos meses restantes de 2025 sem criar um workflow diferente para cada mês.

## Meses cobertos

- agosto/2025 (`08`)
- setembro/2025 (`09`)
- outubro/2025 (`10`)
- novembro/2025 (`11`)
- dezembro/2025 (`12`)

## Branch mensal

Cada execução utiliza uma branch no padrão:

`research/pncp-2025-MM`

Exemplo: `research/pncp-2025-08`.

## Gatilho

Criar na branch mensal um arquivo em:

`research/dependencia-fornecedores-compras-publicas/triggers/pncp-2025-MM.txt`

E abrir uma PR contra `main`. O workflow genérico identifica o mês pela branch e executa toda a rotina.

## Etapas automáticas

1. Geração de oito partições de aproximadamente quatro dias.
2. Consulta do endpoint público de contratos do PNCP.
3. Duas tentativas por partição.
4. Persistência imediata de cada partição validada, com commit `[skip ci]`.
5. Base pública identificada restrita a fornecedores PJ.
6. Consolidação mensal com validação de unicidade de `id_contrato`.
7. Validação de que `data_publicacao` pertence ao intervalo semiaberto do mês.
8. Geração de hash SHA-256 da base mensal.
9. Recalculo acumulado janeiro–mês com comprador = CNPJ institucional.
10. HHI bruto e normalizado, CountHHI, CR1, CR4 e número efetivo.
11. Rede global, Strength principal e Degree complementar.
12. Choques direcionados versus 1.000 remoções aleatórias, semente fixa 20260818.
13. Sensibilidade de elegibilidade 3/5, 5/10, 5/20 e 10/20.
14. Diagnóstico longitudinal contra o mês anterior.
15. Upload de artefato do GitHub Actions.

## Regra temporal

A API é percorrida pela **data de publicação**. As métricas econômicas usam somente instrumentos com **ano de assinatura = 2025**. Assim, publicações tardias de instrumentos antigos podem permanecer na base mensal de publicação, mas não entram na carteira econômica de 2025.

## Política de dados

- GitHub público: fornecedor PJ identificado.
- PF e PE: somente diagnósticos agregados; não republicar nome/CPF.
- Cópias integrais ou artefatos que possam conter dados pessoais: Drive privado.

## Critério de incorporação

Uma PR mensal só deve ser incorporada ao `main` depois de:

- workflow concluído com sucesso;
- zero duplicidade de `id_contrato` entre partições;
- janela de publicação validada;
- hash mensal gerado;
- outputs acumulados e longitudinais presentes;
- revisão dos principais indicadores contra o mês anterior.

## Após dezembro

A conclusão de dezembro não encerra a coleta econômica de 2025. Será executada uma janela adicional de **publicações tardias em 2026**, retendo somente instrumentos com assinatura entre 2025-01-01 e 2025-12-31. A extensão serve para reduzir truncamento por atraso de publicação.
