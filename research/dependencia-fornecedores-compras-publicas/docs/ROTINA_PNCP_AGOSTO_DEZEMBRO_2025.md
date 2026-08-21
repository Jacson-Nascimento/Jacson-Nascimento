# Rotina PNCP — agosto a dezembro de 2025

## Objetivo

Completar o recorte econômico de 2025 sem alterar a especificação metodológica já validada até julho.

## Mês-alvo

O mês em execução é definido em:

`config/pncp_mes_alvo_2025.txt`

Valores permitidos: `08`, `09`, `10`, `11`, `12`.

## Fluxo mensal

1. Dividir automaticamente o mês em blocos de até 4 dias: 01–04, 05–08, 09–12, 13–16, 17–20, 21–24, 25–28 e 29–fim do mês.
2. Consultar o endpoint de contratos/empenhos do PNCP por data de publicação.
3. Aplicar o tratamento já congelado:
   - comprador principal = CNPJ institucional do órgão;
   - fornecedor público identificado = PJ;
   - PF/PE somente em diagnósticos agregados privados;
   - valor principal = `valorInicial`;
   - chave do instrumento = `numeroControlePNCP`;
   - não deduplicar por `numeroControlePNCPCompra`.
4. Persistir cada bloco imediatamente no GitHub com hash e resumo de qualidade.
5. Consolidar o mês e falhar se houver:
   - duplicidade de `id_contrato`;
   - data de publicação fora do mês;
   - data de publicação não parseável.
6. Recalcular o acumulado janeiro–mês final com:
   - HHI e HHI normalizado;
   - CountHHI e CountHHI normalizado;
   - CR1, CR4 e número efetivo de fornecedores;
   - exposição em rede global;
   - Strength global como ranking principal;
   - Degree global como complementar;
   - 1.000 choques aleatórios por cenário;
   - sensibilidade de elegibilidade 3/5, 5/10, 5/20 e 10/20.
7. Executar diagnóstico longitudinal contra o mês anterior com o módulo genérico.
8. Gerar artefato mensal do GitHub Actions.

## Sequência

- Agosto: `08`
- Setembro: `09`
- Outubro: `10`
- Novembro: `11`
- Dezembro: `12`

A metodologia não deve ser alterada entre esses meses. Qualquer nova robustez deve ser executada em módulo separado.

## Após dezembro

O fechamento de dezembro não encerra a base de 2025. Como a coleta é feita por data de publicação e a análise econômica por data de assinatura, será executada uma janela adicional de captura em 2026 para localizar instrumentos assinados em 2025 e publicados tardiamente.

A versão definitiva de 2025 somente será declarada após essa etapa de catch-up e a reexecução dos controles de cobertura, lags, rede, robustez e integração fiscal.

## Regra de interpretação

Resultados acumulados mensais são diagnósticos de convergência e estabilidade. Não devem ser descritos como estimativa anual definitiva antes do fechamento de dezembro e da janela tardia de 2026.
