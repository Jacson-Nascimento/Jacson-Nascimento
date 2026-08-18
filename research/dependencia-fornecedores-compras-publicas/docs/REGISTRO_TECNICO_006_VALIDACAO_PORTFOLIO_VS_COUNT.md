# Registro Técnico 006 - Validação de PortfolioHHI versus CountHHI

## Objetivo

Verificar se a concentração monetária da carteira e a concentração da frequência contratual capturam dimensões distintas antes da coleta anual completa.

## Base

Foi reutilizada a amostra sentinela de 12 datas de 2025, classificada pelo ano de assinatura. Para evitar que compradores observados com apenas um ou dois fornecedores dominassem o teste matematicamente, a comparação principal deste diagnóstico reteve compradores com:

- pelo menos 3 fornecedores observados;
- pelo menos 5 instrumentos observados;
- assinatura em 2025.

Esse filtro existe apenas para validação da métrica. Não é o critério de inclusão do artigo final.

## Resultado com todos os tipos de fornecedor

A amostra diagnóstica contém 437 compradores institucionais.

- PortfolioHHI médio: 0,3161;
- PortfolioHHI mediano: 0,2619;
- CountHHI médio: 0,1278;
- CountHHI mediano: 0,1111;
- correlação de Spearman PortfolioHHI × CountHHI: 0,5689;
- em 97,71% dos compradores, PortfolioHHI foi maior que CountHHI;
- mediana da participação financeira do maior fornecedor: 40,42%;
- mediana do número efetivo de fornecedores por valor: 3,82.

O quartil superior de PortfolioHHI continha 110 compradores e o quartil superior de CountHHI, 98. Apenas 40 compradores estavam simultaneamente no quartil superior das duas métricas.

A diferença absoluta mediana entre os rankings percentuais das duas métricas foi de aproximadamente 16,7 pontos percentuais. No percentil 90, a diferença alcançou aproximadamente 42,4 pontos percentuais.

## Resultado restrito a fornecedores PJ

Com somente fornecedores pessoa jurídica e os mesmos requisitos mínimos, permaneceram 416 compradores.

- PortfolioHHI médio: 0,3233;
- PortfolioHHI mediano: 0,2693;
- CountHHI médio: 0,1296;
- CountHHI mediano: 0,1200;
- correlação de Spearman: 0,5632;
- PortfolioHHI maior que CountHHI em 97,60% dos compradores.

A semelhança dos resultados indica que a divergência não é produzida principalmente pela presença de fornecedores PF na amostra.

## Interpretação

O teste confirma que valor e frequência não são medidas intercambiáveis.

Um comprador pode ter muitos instrumentos relativamente distribuídos, mas concentrar parcela elevada do valor anual em um fornecedor associado a poucos contratos de grande porte. A situação inversa também é possível: elevada recorrência com fornecedor específico sem dominância financeira equivalente.

A diferença é relevante para auditoria porque:

- concentração por valor sinaliza exposição financeira e dependência de contratos de maior peso;
- concentração por frequência sinaliza repetição e persistência operacional da relação contratual.

## Limitação decisiva

A amostra sentinela não é probabilística, é geograficamente enviesada e contém somente 12 datas de publicação. Portanto, esses números **não serão reportados como estimativas da população brasileira**.

Sua função é validar a escolha de manter PortfolioHHI e CountHHI como resultados separados no desenho definitivo.

## Decisão

A hipótese de divergência entre concentração por valor e por frequência permanece no artigo. O teste substantivo será repetido somente após a construção da base anual de 2025 e, para persistência, após a base comparável de 2024.
