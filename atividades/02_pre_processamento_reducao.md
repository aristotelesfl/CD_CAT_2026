# Atividade 2 — Pré-processamento e redução de dimensionalidade

## Problema

Preparar os registros de CAT para a análise e eventual modelagem, verificando se representações menores preservam informação relevante. Justificar cada transformação e comparar pelo menos duas estratégias de redução estudadas.

## Instruções

Aplicar o recorte principal de registros cuja UF do acidente está registrada como Ceará, conforme a análise exploratória, e documentar a incerteza sobre a qualidade desse campo. A localização do empregador não restringe a população. Reproduzir e aproveitar as etapas pertinentes dos notebooks existentes, sem usar o filtro de UF não classificada de `main.ipynb` como sinônimo de Ceará.

1. Aplicar o [plano compartilhado](README.md) e registrar diagnóstico antes de modificar os dados: tipos, ausências, marcadores, duplicatas potenciais, datas inválidas ou incoerentes, categorias equivalentes, alta cardinalidade, constantes e extremos. Diferenciar erro comprovado de valor possível e documentar evidências e contagens.
2. Definir o objetivo e a unidade de análise. Inventariar campos disponíveis no momento de uso, identificadores, atributos potencialmente redundantes e possíveis vazamentos. Avaliar separadamente códigos e descrições repetidas; não presumir que colunas com mesmo nome sejam idênticas. CNPJ/CEI não deve ser usado como preditor direto sem justificativa robusta.
3. Aplicar os dicionários locais de CBO, CID-10, CNAE e agente causador conforme as regras do [plano compartilhado](README.md), preservando códigos e descrições originais. Auditar chaves, cobertura, ambiguidades e contagem de linhas antes e depois das junções; não adivinhar correspondências textuais truncadas. Definir e documentar tratamentos para ausências, datas, categorias, codificação, escalonamento e extremos. Manter rastreabilidade das linhas e distinguir estados desconhecidos de valores reais. Quando aplicável, derivar idade apenas de datas válidas e verificar plausibilidade, sem expor datas de nascimento individuais.
4. Quando houver modelagem supervisionada, definir alvo e ponto de previsão primeiro; separar treino e teste antes de ajustar imputação, codificação, escalonamento, seleção ou PCA. Ajustar esses passos apenas no treino e, durante validação cruzada, dentro de cada dobra via pipeline. Reservar o teste para avaliação final.
5. Comparar pelo menos duas estratégias de redução estudadas, incluindo seleção de atributos e PCA quando viáveis. Considerar filtro, wrapper e embutido conforme o objetivo, custo e tipo dos dados; métodos supervisionados exigem alvo válido e devem ser ajustados somente no treino. Justificar limitações ou inviabilidade de técnicas.
6. Para PCA, justificar variáveis e escala, relatar variância explicada individual e acumulada, número de componentes e contribuições; avaliar CP1–CP2 quando útil, sem presumir separação. Comparar representação completa, atributos selecionados e componentes em dimensão, informação preservada, custo e interpretabilidade. Variância explicada não garante preservação da capacidade preditiva.
7. Salvar base final e documentação das transformações; quando aplicável, preservar treino e teste separadamente, sem dados identificáveis desnecessários. Registrar decisões ambíguas e o que mudaria com informação adicional de domínio.

## Entregas

- Notebook executável com diagnóstico, transformações e comparação de pelo menos duas estratégias.
- Relatório curto com evidências e justificativas, seleção de atributos, PCA, comparação e limitações.
- Base final pré-processada e, quando aplicável, conjuntos de treino e teste separados; documentar formato e reprodução.

## Critérios de aceitação

- [ ] Diagnóstico quantifica problemas antes do tratamento e distingue hipóteses de erros comprovados.
- [ ] Descrições normalizadas são rastreáveis aos dicionários; cobertura, ambiguidades, códigos não encontrados e preservação da quantidade de linhas são documentados.
- [ ] Cada transformação tem problema, regra, justificativa e impacto documentados; originais permanecem intactos.
- [ ] Identificadores, redundâncias, categorias e vazamentos são avaliados; passos ajustáveis respeitam treino, dobras e teste quando aplicável.
- [ ] Pelo menos duas estratégias de redução são comparadas com a representação original em dimensão, informação e interpretabilidade; suas escolhas são justificadas.
- [ ] PCA apresenta escala, variância explicada, componentes escolhidas e interpretação, ou registra uma justificativa fundamentada para sua inviabilidade.
- [ ] Notebook, relatório e base final são reproduzíveis; limitações e decisões dependentes do domínio são explícitas.
