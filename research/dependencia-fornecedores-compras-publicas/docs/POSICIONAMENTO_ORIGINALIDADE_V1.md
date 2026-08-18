# Posicionamento de Originalidade v1

## Objetivo

Evitar reivindicações de originalidade que a literatura disponível até agosto de 2026 não sustenta e definir onde a contribuição potencial do artigo permanece defensável.

## 1. PortfolioHHI não é uma medida nova

Sharma, Saboo, Borah e Adhikary (2026), em *Supplier concentration and firm performance: the role of relative size, relative reputation, and network position*, medem concentração de fornecedores com um HHI adaptado às participações dos fornecedores nos custos de insumos do comprador.

Referência:

Sharma, A.; Saboo, A. R.; Borah, S. B.; Adhikary, A. (2026). Supplier concentration and firm performance: the role of relative size, relative reputation, and network position. *International Journal of Research in Marketing*. DOI: 10.1016/j.ijresmar.2026.01.006.

### Consequência

O artigo não apresentará `PortfolioHHI` como índice original. Ele será uma adaptação transparente da literatura de supply-base concentration ao contexto de compradores públicos brasileiros.

## 2. Divergência valor-contagem também já foi proposta

Fountoukidis (2026), em *Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement*, propõe `Value–Count Divergence` para medir a divergência entre rankings de fornecedores por número de contratos e por valor, usando TED da União Europeia entre 2018 e 2022.

O estudo também mostra que variáveis estruturais de rede têm forte capacidade de prever fornecedores que capturam parcela elevada do valor em período posterior.

### Consequência

A comparação `PortfolioHHI × CountHHI` e a divergência entre valor e frequência não serão vendidas como invenção metodológica. O artigo deverá reconhecer explicitamente esse trabalho e tratar a evidência brasileira como replicação, extensão e reespecificação em nível de comprador institucional.

Referência de trabalho:

Fountoukidis, I. (2026). Many Suppliers Win, Few Capture the Value: Participation and Value Concentration in EU Public Procurement. SSRN 6897598. DOI: 10.2139/ssrn.6897598.

## 3. Concentração + persistência em compras públicas também já aparece em 2026

Fountoukidis, Dafli, Antoniou e Varsakelis (2026) propõem um `Institutional Closure Index`, indicador em nível de autoridade que combina concentração em base limitada de fornecedores com relações persistentes e incorporadas comprador-fornecedor.

### Consequência

A combinação genérica entre concentração e repetição também não é suficiente, isoladamente, para sustentar originalidade.

Referência:

Fountoukidis, I.; Dafli, E.; Antoniou, I.; Varsakelis, N. (2026). Measuring Institutional Closure in Public Procurement: A Network-Based Index from European Buyer-Supplier Data. SSRN 6765160.

## 4. Análise de redes em compras públicas brasileiras não é nova

Fonseca (2025), em dissertação de mestrado na NOVA IMS, analisa compras públicas federais brasileiras entre 2022 e meados de 2024 como redes bipartidas comprador-fornecedor e emprega Degree, Betweenness, Closeness, Eigenvector Centrality e detecção de comunidades.

### Consequência

Não reivindicar pioneirismo no uso de network analysis no PNCP ou em compras públicas brasileiras.

Referência:

Fonseca, Fernanda da Trindade (2025). *Patterns In Public Contracting: A Network Theory Perspective on Procurement Dynamics in Brazil*. NOVA Information Management School. Dissertação de mestrado. Handle: 10362/190144.

## 5. Repetição contratual já tem literatura internacional

Estudos de compras públicas anteriores analisam seleção repetida de fornecedores, persistência de relações e sua associação com preços, transparência ou características procedimentais.

Portanto, repetição de fornecedor também não pode ser apresentada como tema inédito.

## 6. Compras compartilhadas e centralização possuem literatura própria

A literatura e documentos da OCDE reconhecem ganhos potenciais de centralização e joint procurement, como escala, especialização e redução de custos de transação, mas também riscos dinâmicos, inclusive aumento de concentração de oferta, barreiras a fornecedores menores e redução de resiliência.

### Consequência

`SharedProcurementShare` tem fundamentação econômica clara e deve ser tratada de forma simétrica: compras compartilhadas podem reduzir custos e aumentar capacidade de compra, mas também podem alterar a estrutura da base de fornecedores. O sinal deve ser estimado, não presumido.

## 7. Onde permanece a contribuição potencial

A contribuição do artigo deve ser construída como **integração empírica e institucional**, não como invenção de uma métrica isolada.

### 7.1 Unidade institucional brasileira

O PNCP permite distinguir:

- CNPJ do órgão/entidade do instrumento;
- município da unidade executora;
- CNPJ da contratação de origem.

O piloto mostrou que agregar simplesmente por município pode alterar materialmente o HHI. A distinção institucional será parte central da construção da base.

### 7.2 Compras compartilhadas observadas diretamente no PNCP

O artigo poderá medir sistematicamente a diferença entre comprador do instrumento e proprietário da contratação de origem e avaliar sua associação com concentração da carteira e exposição de rede.

Esse mecanismo é especialmente relevante no contexto de consórcios públicos e estruturas de contratação compartilhada.

### 7.3 Três dimensões mensuradas no mesmo painel

O desenho integrará no mesmo comprador-ano:

1. concentração financeira da carteira;
2. concentração de frequência;
3. exposição a fornecedores centrais e choques de rede.

A literatura possui elementos dessas dimensões, mas a contribuição potencial está em avaliar como elas divergem no ambiente institucional brasileiro e como a classificação dos compradores muda entre elas.

### 7.4 Choques estruturais em rede pública de contratação

A simulação de perda da carteira após remoção direcionada de fornecedores oferece uma medida operacional de exposição que vai além da simples centralidade. A originalidade dessa aplicação específica deverá ser verificada em revisão sistemática antes da submissão.

### 7.5 Integração PNCP + SICONFI + IBGE

A combinação de estrutura comprador-fornecedor com controles fiscais do mesmo exercício permite analisar concentração condicionada à escala fiscal e às características do ente.

### 7.6 Pipeline reproduzível

O trabalho está sendo construído com:

- código versionado;
- registros técnicos de decisões;
- bases públicas minimizadas;
- cópias integrais privadas;
- manifestos e checksums;
- critérios explícitos de cobertura e qualidade.

Essa característica aumenta auditabilidade e replicação, embora também não seja, por si só, contribuição teórica.

## 8. Formulação conservadora de contribuição

Uma formulação provisória aceitável é:

> Este estudo adapta medidas de concentração da base de fornecedores e análise de redes ao contexto das compras públicas brasileiras, distinguindo concentração monetária, recorrência contratual e exposição estrutural. O desenho explora características institucionais do PNCP, incluindo a separação entre comprador do instrumento, unidade executora e contratação de origem, e integra essas medidas a controles fiscais municipais.

Evitar, até revisão sistemática concluída:

- primeiro estudo;
- índice inédito;
- primeira aplicação;
- nova medida de HHI;
- primeira análise de redes de compras públicas brasileiras.

## 9. Próxima etapa de originalidade

Antes da versão de submissão, executar revisão sistemática ou bibliométrica focada em:

- supplier concentration / supply-base concentration;
- buyer-supplier dependence;
- public procurement concentration;
- value-count divergence;
- repeated awards / supplier persistence;
- buyer-supplier network public procurement;
- joint procurement / central purchasing bodies;
- procurement network resilience / disruption simulation;
- aplicações PNCP e Brasil.

A reivindicação final de contribuição deverá ser definida somente após esse mapeamento.
