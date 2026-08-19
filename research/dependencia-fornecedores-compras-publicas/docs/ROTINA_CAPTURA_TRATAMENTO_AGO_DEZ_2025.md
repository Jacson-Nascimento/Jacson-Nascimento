# Rotina PNCP para agosto-dezembro de 2025

## Objetivo
Executar de forma reprodutível a expansão mensal da base PNCP até dezembro de 2025, preservando a especificação metodológica validada até julho.

## Comando único

```bash
cd research/dependencia-fornecedores-compras-publicas
python scripts/executar_pncp_meses_restantes_2025.py --start-month 8 --end-month 12
```

## Fluxo por mês
1. Dividir o mês em janelas consecutivas de até quatro dias.
2. Para cada janela, reutilizar checkpoint se base PJ e resumo já existirem.
3. Caso contrário, chamar `coletar_pncp_periodo.py`, com duas tentativas e espera de 60 segundos.
4. Consolidar o mês com `consolidar_mes_pncp_2025.py`.
5. Validar unicidade de `id_contrato`, parsing de datas e intervalo semiaberto do mês.
6. Recalcular o acumulado global com `analisar_acumulado_2025_global.py`.
7. Persistir bases, resumos, manifesto, métricas e resultados no GitHub.
8. Após cada mês, executar diagnóstico longitudinal mês anterior→mês atual, SICONFI incremental e modelo associativo genérico.

## Meses programados
- agosto: 2025-08
- setembro: 2025-09
- outubro: 2025-10
- novembro: 2025-11
- dezembro: 2025-12

## Especificação congelada
- unidade comprador: CNPJ institucional;
- fornecedores: PJ;
- análise econômica: instrumentos assinados em 2025 e `valorInicial > 0`;
- HHI bruto e normalizado;
- CountHHI bruto e normalizado;
- exposição na rede global;
- Strength global como ordenação principal dos choques;
- Degree global como complementar;
- 1.000 remoções aleatórias por cenário;
- sensibilidade de elegibilidade 3/5, 5/10, 5/20 e 10/20;
- publicação usada para captura, assinatura usada para pertencimento econômico a 2025.

## Controles mínimos antes de aceitar cada mês
- zero duplicidade de `id_contrato` entre partições;
- zero data de publicação não parseável;
- todas as publicações dentro do intervalo mensal correto;
- SHA-256 da base mensal consolidada;
- contagem de PJ, compradores, fornecedores e municípios;
- lags negativos preservados e sinalizados para sensibilidade;
- comparação das métricas acumuladas com o mês anterior.

## Etapas após dezembro
A base de 2025 não deve ser declarada final imediatamente em 31/12/2025. Deve ser executada uma janela complementar de captura em 2026 para localizar instrumentos assinados em 2025 e publicados tardiamente. O encerramento dessa janela deve ser definido por análise empírica da distribuição dos lags de publicação, e não por data arbitrária.

## Persistência Git
O orquestrador Python produz os arquivos. A persistência recomendada é um commit por partição e um commit de consolidação por mês, seguindo o padrão usado de abril a julho. Não substituir arquivos já validados sem registrar motivo, hash anterior e hash novo.
