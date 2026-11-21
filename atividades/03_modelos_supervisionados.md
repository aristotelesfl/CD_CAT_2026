# Atividade 3 — Modelos supervisionados e avaliação

## Problema e viabilidade

Definir uma tarefa supervisionada de classificação pertinente aos registros de CAT, especificando alvo, classe positiva, unidade de análise, momento da previsão, horizonte e uso pretendido. Uma hipótese a investigar é classificar `Indica Óbito Acidente`, **somente se** a disponibilidade temporal dos atributos, a qualidade dos rótulos e a quantidade de casos positivos permitirem uma avaliação válida. Não presumir que o campo seja um desfecho futuro ou que os demais campos estejam disponíveis antes dele. Outra tarefa pode ser escolhida e justificada.

Antes de treinar, verificar distribuição do alvo, valores desconhecidos, quantidade de eventos por período e classe, disponibilidade e momento de cada preditor, e possíveis repetições entre conjuntos. Se não houver alvo e preditores temporalmente válidos, registrar a inviabilidade e a informação adicional necessária; não apresentar um experimento com vazamento como modelo utilizável.

## Instruções

Aplicar o recorte principal de registros cuja UF do acidente está registrada como Ceará, conforme a análise exploratória, e documentar a incerteza sobre a qualidade desse campo. A localização do empregador não restringe a população. Reproduzir e aproveitar as etapas pertinentes dos notebooks existentes, sem usar o filtro de UF não classificada de `main.ipynb` como sinônimo de Ceará.

1. Usar o [plano compartilhado](README.md) e as decisões da etapa 2. Descrever população, recorte, rótulo, classe positiva e custos relativos de falsos positivos e falsos negativos. Excluir alvo desconhecido da avaliação supervisionada e quantificar exclusões, sem tratá-lo como negativo.
2. Definir holdout antes de qualquer ajuste. Preferir divisão temporal quando coerente com o uso pretendido, com datas efetivas verificadas em vez de confiar no sufixo do arquivo. Considerar grupos de registros potencialmente relacionados quando identificáveis; se não houver chave confiável, registrar o risco de sobreposição. Justificar alternativa estratificada ou temporal conforme dados, e verificar representação de classes. Não usar o teste para escolher variáveis, limiar, modelos ou hiperparâmetros.
3. Aplicar k-fold cross-validation apenas no treino, estratificada quando adequada; para previsão temporal, usar validação cronológica apropriada e evitar informação futura. Ajustar imputação, codificação, escalonamento e redução dentro de cada dobra por pipelines. Garantir comparação nas mesmas partições e métricas, com transformações adequadas a cada algoritmo.
4. Construir e ajustar as quatro famílias exigidas: KNN, árvore de decisão, ensemble de árvores (Random Forest e/ou boosting) e MLP. Registrar grades de hiperparâmetros, configurações escolhidas, sementes, custo e eventuais problemas de convergência. Adicionar baseline simples para contextualizar o resultado.
5. No desenvolvimento, comparar acurácia, precisão, recall/sensibilidade, F1 e ROC-AUC, com dispersão entre dobras quando possível. Usar probabilidades ou escores contínuos para ROC/AUC; definir limiar e classe positiva no treino. Se classes raras ou ausentes tornarem uma métrica indefinida, explicitar isso e ajustar a estratégia sem inventar resultado. Considerar curva precisão–recall como complemento para desbalanceamento.
6. Escolher modelo, parâmetros e eventual limiar com base na validação e nos custos dos erros. Avaliar os modelos selecionados uma vez no teste reservado; não fazer nova escolha guiada por ele. Apresentar tabela com as métricas exigidas, matrizes de confusão do final e principais comparados, curvas ROC e interpretação de VP, FP, VN e FN. Comparar desenvolvimento e teste e discutir possível sobreajuste.
7. Justificar a escolha considerando desempenho, erros, interpretabilidade, limitações de cobertura, rótulos, subnotificação e generalização. Não interpretar a predição como causalidade ou promessa de aplicação operacional.

## Entregas

- Notebook executável com preparação final, treino, ajuste, validação e avaliação.
- Relatório curto com alvo, recorte, divisão, modelos, comparação, escolha e limitações.
- Tabela com acurácia, precisão, recall, F1 e AUC; matrizes de confusão do final e principais comparados; curvas ROC dos selecionados; registro dos hiperparâmetros avaliados e escolhidos.

## Critérios de aceitação

- [ ] Alvo, classe positiva, ponto de previsão e disponibilidade temporal dos preditores são definidos e validados; viabilidade e exclusões são documentadas.
- [ ] Holdout e k-fold são adequados ao uso e às classes; teste fica reservado e pré-processamento/seleção são ajustados dentro das dobras de treino.
- [ ] KNN, árvore, ensemble e MLP são ajustados e comparados nas mesmas partições; hiperparâmetros e baseline são registrados.
- [ ] Tabela contém as cinco métricas, matrizes e curvas exigidas; métricas indefinidas são explicadas.
- [ ] Escolha é baseada na validação, interpreta tipos de erro e trade-off precisão–recall e é confrontada com teste sem reajuste.
- [ ] Notebook e relatório são reproduzíveis, claros e reconhecem limitações de dados, vazamento residual e generalização.

Caso a viabilidade falhe, entregar o diagnóstico e as limitações em vez de declarar concluídos os critérios de treinamento e avaliação; indicar dados ou definições necessários para retomá-los.
