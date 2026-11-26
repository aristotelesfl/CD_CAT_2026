# Roteiro de apresentação das CATs no Ceará em 2026

Apresentação planejada para **13 minutos, incluindo a futura parte de modelos**, com 12 slides. A sequência começa pela recapitulação da CAT e pelas perguntas do projeto, apresenta os resultados exploratórios e explica como a base foi preparada para a classificação.

Os textos de **conteúdo do slide** são sugestões para a tela. As **falas sugeridas** servem como guia para o apresentador e não precisam aparecer nos slides. Os tempos incluem a explicação dos gráficos e as transições.

Base: [relatório de análise exploratória](relatorio_analise_exploratoria.md) e [relatório de pré-processamento e redução](relatorio_pre_processamento_reducao.md).

**Nota para a montagem:** o relatório de pré-processamento indicado define óbito como alvo, enquanto o README menciona parte do corpo atingida. Este roteiro segue o alvo dos relatórios solicitados. Antes de incorporar a parte de modelos, alinhar essa definição entre os materiais. Os slides 10 e 11 são espaços planejados para resultados futuros; nenhum desempenho de modelo é antecipado aqui.

## Distribuição do tempo

| Slide | Tema | Duração | Tempo acumulado |
|---|---|---:|---:|
| 1 | O que é CAT e qual é o recorte | 0min40s | 0min40s |
| 2 | Perguntas que orientam o projeto | 0min45s | 1min25s |
| 3 | Origem dos dados e unidade de análise | 0min45s | 2min10s |
| 4 | Perfil dos registros e atividades econômicas | 1min05s | 3min15s |
| 5 | Tipos de acidente e parte do corpo | 0min50s | 4min05s |
| 6 | Emissão, variação mensal e limites geográficos | 1min10s | 5min15s |
| 7 | Limpeza e transformação dos dados | 1min | 6min15s |
| 8 | Alvo, divisão da base e desbalanceamento | 1min05s | 7min20s |
| 9 | Comparação das formas de redução | 1min40s | 9min |
| 10 | Modelos e estratégia de avaliação — futuro | 1min20s | 10min20s |
| 11 | Resultados dos modelos — futuro | 1min40s | 12min |
| 12 | Conclusões e próximos passos | 1min | **13min** |

## Slide 1 — O que é CAT e qual é o recorte

**Conteúdo do slide**

- **CAT: Comunicação de Acidente de Trabalho.**
- Reúne informações sobre o acidente, o trabalhador e o empregador.
- Recorte: UF do acidente informada como Ceará; ocorrência de janeiro a junho de 2026.
- Título da apresentação: **CATs no Ceará — exploração e preparação para classificação**.

**Visual sugerido:** três elementos simples para acidente, trabalhador e empregador, acompanhados do período analisado. Usar este slide também como capa.

**Fala sugerida**

“Antes dos resultados, vamos recapitular o que estamos analisando. CAT significa Comunicação de Acidente de Trabalho. Seus registros reúnem informações sobre o acidente, o trabalhador e o empregador. Nosso estudo considera as comunicações cuja UF do acidente foi informada como Ceará e cuja ocorrência foi registrada entre janeiro e junho de 2026. A proposta é entender o perfil dessa base e preparar os dados para uma etapa de classificação.”

**Transição:** “A partir desse recorte, organizamos as perguntas que orientam o projeto.”

## Slide 2 — Perguntas que orientam o projeto

**Conteúdo do slide**

1. Qual é o perfil por sexo e faixa etária?
2. Quais atividades econômicas concentram mais registros?
3. Quais tipos de acidente e partes do corpo são mais frequentes?
4. Quanto tempo decorre até a emissão da CAT?
5. Como os registros variam ao longo do semestre?

Em destaque abaixo: **Para a classificação: as informações selecionadas ajudam a identificar os registros com óbito?**

**Visual sugerido:** perguntas agrupadas em “Perfil”, “Acidentes” e “Tempo”, com a pergunta de classificação em uma faixa inferior.

**Fala sugerida**

“A exploração procura responder quem aparece nos registros, quais atividades econômicas concentram mais notificações e quais tipos de acidente e partes do corpo são mais frequentes. Também investigamos o intervalo até a emissão e a variação mensal. Depois, avançamos para uma pergunta de classificação: as informações selecionadas ajudam a identificar os registros que indicam óbito? A etapa atual prepara as representações que serão comparadas pelos modelos.”

**Transição:** “Para interpretar essas respostas, precisamos primeiro entender o que está sendo contado.”

## Slide 3 — Origem dos dados e unidade de análise

**Conteúdo do slide**

- Seis arquivos mensais de CAT disponibilizados pelo INSS.
- **620.163 linhas consolidadas → 8.849 no recorte → 7.201 combinações distintas.**
- Exploração: contagem principal de 8.849 linhas, com análise de sensibilidade.
- Pré-processamento: 7.201 combinações distintas dos 27 campos originais.

Rodapé: **Uma linha representa uma comunicação disponível; não identifica necessariamente um acidente ou trabalhador único.**

**Visual sugerido:** fluxo com os três totais. Sobre a última seta, escrever “remoção de 1.648 ocorrências adicionais de linhas idênticas”.

**Fala sugerida**

“Os seis arquivos somam mais de 620 mil linhas. Ao aplicar o recorte pela UF e pela data do acidente, chegamos a 8.849. A análise exploratória usa esse total e compara os resultados com 7.201 combinações distintas dos campos originais. A preparação para os modelos mantém essas combinações uma vez cada. Como não há identificador único da CAT, linhas iguais não comprovam que se trata do mesmo acidente. Por isso, precisamos explicitar a unidade de análise.”

**Transição:** “Com essa definição, podemos olhar para o perfil dos registros.”

## Slide 4 — Perfil dos registros e atividades econômicas

**Conteúdo do slide**

- Sexo registrado: **53,26% masculino** e **46,62% feminino**; 0,12% sem informação.
- Idade mediana: **37 anos**; faixa mais frequente: **18 a 29 anos, com 28,64%**.
- Saúde humana e serviços sociais: **25,52%** dos registros.
- Técnico de enfermagem: ocupação mais frequente, com **12,45%**.

Rodapé: percentuais calculados sobre as **8.849 linhas** do recorte.

**Visual sugerido:** usar o gráfico existente [perfil por idade e sexo](figuras/atividade_01/perfil_idade_sexo.png), com um destaque lateral para o setor de saúde. Evitar acrescentar uma tabela extensa de atividades.

**Fala sugerida**

“Há uma pequena predominância do sexo masculino, com 53,26% dos registros. A idade mediana é de 37 anos, e a faixa de 18 a 29 anos é a mais frequente. O gráfico também mostra que a composição por sexo muda entre as faixas etárias. Na atividade econômica do empregador, saúde humana e serviços sociais reúne cerca de um quarto das notificações. Técnico de enfermagem é a ocupação mais frequente. Esses resultados descrevem a composição dos registros: para comparar o risco entre setores, precisaríamos também saber quantos trabalhadores estão expostos em cada atividade.”

**Transição:** “Além do perfil, quais características dos acidentes aparecem com mais frequência?”

## Slide 5 — Tipos de acidente e parte do corpo

**Conteúdo do slide**

| Tipo registrado | Percentual |
|---|---:|
| Típico | **68,31%** |
| Trajeto | 23,70% |
| Doença | 7,99% |

- **Dedo** é a parte do corpo mais citada: **19,06%** de todos os registros.
- Entre os acidentes típicos, dedo aparece em **26,60%**.

Rodapé: distribuição por tipo e percentual geral de parte do corpo sobre **8.849 linhas**; percentual nos típicos sobre **6.045 linhas**.

**Visual sugerido:** gráfico de barras horizontais com os três tipos e um destaque para dedo.

**Fala sugerida**

“Os acidentes típicos predominam, com cerca de 68% dos registros, seguidos pelos de trajeto e pela categoria doença. Essa liderança se mantém quando contamos apenas as linhas distintas. Dedo é a parte do corpo mais citada, presente em 19% do total e em aproximadamente 27% dos acidentes típicos. Isso responde às perguntas sobre as características mais frequentes, sem estabelecer por si só as causas dessas ocorrências.”

**Transição:** “A dimensão temporal traz outro resultado importante, mas também mostra o efeito da qualidade dos dados.”

## Slide 6 — Emissão, variação mensal e limites geográficos

**Conteúdo do slide**

- Intervalo até a emissão: **mediana de 5 dias corridos**; **64,13%** emitidas até o sétimo dia.
- Pico mensal: **junho nas 8.849 linhas**; **maio nas 7.201 linhas distintas**.
- **8,07%** das linhas do recorte têm emissão posterior a junho.
- Município disponível: **do empregador**, insuficiente para localizar o acidente.

**Visual sugerido:** gráfico mensal com duas séries, “Todas as linhas” e “Linhas distintas”, usando a tabela da seção 4.6 do relatório exploratório. Apresentar o prazo mediano em um pequeno destaque. O gráfico existente de [prazo de emissão](figuras/atividade_01/prazo_emissao.png) pode ficar como material de apoio.

**Fala sugerida**

“O intervalo mediano entre acidente e emissão é de cinco dias corridos, e cerca de 64% das CATs foram emitidas até o sétimo dia. Na série mensal, junho lidera quando contamos todas as linhas, mas maio passa à frente quando contamos cada combinação uma vez. Portanto, o pico de junho é sensível às repetições entre arquivos. Além disso, parte das comunicações foi emitida depois do semestre. Há também um limite geográfico: o município disponível é o do empregador, e existe uma divergência expressiva entre as UFs do acidente e do empregador. Essa base não permite comparar municípios de ocorrência.”

**Transição:** “Essas observações orientam a passagem da exploração para a preparação dos dados.”

## Slide 7 — Limpeza e transformação dos dados

**Conteúdo do slide**

- Remoção de **1.648 linhas adicionais idênticas**, considerando os 27 campos originais.
- Tratamento de ausências, códigos sem informação e descrições truncadas.
- Agente causador: **6.538 correspondências únicas** e **663 registros como Desconhecido**.
- Três entradas no experimento: **tipo do acidente, agente causador e tipo de empregador**.
- **One-hot encoding: 3 entradas categóricas → 163 indicadores binários.**

**Visual sugerido:** fluxo “Limpeza → Escolha das entradas → Codificação”. Mostrar um único exemplo: `Tipo do Acidente_Trajeto = 1` quando a CAT é de trajeto.

**Fala sugerida**

“Na preparação, mantivemos uma ocorrência de cada combinação idêntica e tratamos valores ausentes ou sem classificação. Para o agente causador, usamos o dicionário quando havia uma correspondência única. Ausências e associações sem solução foram reunidas em Desconhecido. O experimento de redução utiliza três entradas: tipo do acidente, agente causador e tipo de empregador. A codificação one-hot transforma suas categorias em 163 colunas de zero ou um. O diagnóstico foi excluído considerando um cenário anterior à sua disponibilidade; as três entradas escolhidas também precisam estar disponíveis no momento da previsão.”

**Transição:** “Depois de definir as entradas, precisamos observar a distribuição do que queremos prever.”

## Slide 8 — Alvo, divisão da base e desbalanceamento

**Conteúdo do slide**

- Alvo: **Indica Óbito Acidente**, com **Sim** como classe positiva.
- Base preparada: **27 registros com óbito em 7.201**, aproximadamente **0,37%**.
- Treino: **5.760 registros, com 22 óbitos**.
- Teste: **1.441 registros, com 5 óbitos**.
- Prever “Não” para toda a base: **99,63% de acurácia e nenhum óbito identificado**.

**Visual sugerido:** dois cartões para treino e teste, acompanhados de uma barra de proporção com destaque ampliado para a classe positiva. Evitar gráfico de pizza com uma fatia quase invisível.

**Fala sugerida**

“O alvo é a indicação de óbito registrada na CAT. Há apenas 27 registros positivos entre os 7.201 da base preparada. A divisão aleatória estratificada separou 80% para treino e 20% para teste, preservando aproximadamente essa proporção. O encoder foi ajustado somente no treino. O desbalanceamento muda a forma de avaliar: prever Não para todos daria 99,63% de acurácia, mas não identificaria nenhum óbito. Por isso, a etapa de modelos deve olhar para recall da classe positiva, precisão, average precision e falsos positivos. Com cinco óbitos no teste, um único acerto adicional altera o recall em 20 pontos percentuais.”

**Transição:** “Antes de avaliar os modelos, comparamos formas de representar essas entradas com menos colunas.”

## Slide 9 — Comparação das formas de redução

**Conteúdo do slide**

| Representação | Número de colunas |
|---|---:|
| One-hot e filtro de variância zero | 163 |
| Qui-quadrado / informação mútua | 50 cada |
| Interseção dos filtros | 49 |
| Wrapper forward | 8 |
| Seleção por árvore | 10 |
| PCA com retenção de 90% da variância | 142 |

- Os filtros supervisionados compartilham **49 dos 50 indicadores** escolhidos.
- PCA preservou **90,15% da variância** e reduziu a dimensão em apenas **12,88%**.
- **Menos colunas não determina melhor desempenho preditivo.**

**Visual sugerido:** barras horizontais com a quantidade de colunas por método. Identificar “indicadores selecionados” e “componentes do PCA”. Elaborar o gráfico a partir desta tabela, sem inserir resultados de desempenho de outra etapa.

**Fala sugerida**

“Comparamos seleção de características, que mantém alguns indicadores originais, e PCA, que cria combinações desses indicadores. O filtro de variância zero manteve todas as 163 colunas. Qui-quadrado e informação mútua foram configurados para escolher 50 e concordaram em 49. O Wrapper foi configurado para oito indicadores, e a árvore selecionou dez. Esses tamanhos precisam ser lidos junto com os parâmetros do experimento.

No PCA, foram necessárias 142 componentes para preservar cerca de 90% da variância padronizada. A redução foi pequena, pois a variação ficou distribuída entre muitas componentes. Além disso, preservar variância não equivale a preservar a capacidade de identificar óbitos.

Trajeto aparece entre os indicadores destacados por diferentes métodos. Já o maior escore de qui-quadrado, para medicamento em geral, se apoia em apenas três registros, um deles com óbito. Isso mostra por que precisamos interpretar os rankings junto com suas contagens. A escolha final da representação depende da comparação preditiva.”

**Transição:** “Essas representações são o ponto de partida para a etapa de modelos.”

## Slide 10 — Modelos e estratégia de avaliação

**Reservado para a etapa futura — 1min20s.**

**Conteúdo a preencher quando a etapa estiver concluída**

- Quais classificadores foram comparados e por que foram escolhidos.
- Quais representações entraram na comparação, incluindo uma referência com as 163 colunas.
- Como foram definidas as partições de validação e o critério de escolha.
- Como o procedimento evitou usar o teste durante a seleção.

**Visual sugerido:** fluxo “Treino → Validação e escolha → Teste final”, com os nomes dos modelos efetivamente avaliados.

**Roteiro de fala a completar**

“Com os dados preparados, comparamos [modelos] usando [representações]. A validação seguiu [procedimento], e a escolha considerou [critério]. Em cada partição, ajustamos a codificação e a seleção ou extração de características apenas nos dados de treinamento. Depois da escolha, utilizamos o teste para estimar o desempenho final.”

**Orientação para a futura implementação:** para uma comparação válida, reajustar encoder, seletores e, quando aplicáveis, padronização e PCA dentro do treino de cada fold. Usar partições comparáveis. A validação interna do Wrapper serve à escolha de seu subconjunto e não substitui a avaliação do procedimento completo. A fala acima só deve descrever procedimentos efetivamente realizados.

## Slide 11 — Resultados dos modelos

**Reservado para a etapa futura — 1min40s.**

**Conteúdo a preencher quando houver resultados**

- Comparação de **average precision, recall de Sim e precisão**, com conjunto avaliado e limiar identificados.
- Matriz de confusão do procedimento escolhido no teste.
- Quantidade de óbitos identificados e de falsos positivos.
- Efeito da redução de dimensão sobre os resultados.

**Visual sugerido:** tabela compacta dos resultados de validação e matriz de confusão do teste, claramente separadas. Destacar as contagens absolutas, além dos percentuais.

**Roteiro de fala a completar**

“Na validação, [procedimento] foi escolhido com base em [critério e resultados]. Na avaliação final, identificou [quantidade] dos cinco registros com óbito e produziu [quantidade] falsos positivos, no limiar [valor]. A representação com [quantidade] colunas apresentou [resultado observado] em relação à referência. Como o teste tem poucos casos positivos, interpretamos essas diferenças junto com as contagens e a variação observada na validação.”

**Cuidado na conclusão:** não declarar um método superior apenas porque usa menos colunas ou tem acurácia alta. Se a divisão da base mudar na etapa futura, atualizar os totais e a descrição dos slides 8, 10 e 11.

## Slide 12 — Conclusões e próximos passos

**Conteúdo do slide**

- Exploração: predominância de acidentes típicos e destaque das atividades de saúde.
- Qualidade dos dados: repetições afetam a série mensal; o município do acidente não está disponível.
- Preparação: diferentes representações geradas, com **forte desbalanceamento do alvo**.
- Modelos: **[inserir a conclusão sustentada pela avaliação futura]**.

**Visual sugerido:** três blocos curtos — “O que aprendemos”, “Limites da base” e “O que a avaliação dos modelos acrescenta”.

**Fala sugerida para a versão atual**

“A exploração mostrou a predominância de acidentes típicos e a concentração de notificações nas atividades de saúde. Também mostrou que as repetições alteram a leitura da evolução mensal e que o município do empregador não permite localizar os acidentes. Na preparação, construímos diferentes representações para a classificação de óbito. Os métodos de seleção geraram subconjuntos compactos, enquanto o PCA padronizado reduziu pouco a dimensão. A próxima etapa é verificar quais combinações de representação e modelo ajudam a identificar a classe positiva, considerando o número reduzido de óbitos e o custo dos falsos positivos.”

**Ao incorporar os modelos:** substituir as duas últimas frases pela conclusão efetivamente observada e por seu principal limite. Manter o fechamento em um minuto.

## Ajustes para apresentações de 10 a 15 minutos

**Versão de 10 minutos:** manter 3 minutos para modelos e 1 minuto para conclusão. Reduzir os slides 1, 2 e 3 para 30 segundos cada; os slides 4, 5, 6, 7 e 8 para 40 segundos cada; e o slide 9 para 1min10s. Nos resultados exploratórios, apresentar apenas os destaques. No slide 9, explicar a diferença entre seleção e PCA, sem detalhar o exemplo de medicamento.

**Versão de 13 minutos:** seguir a distribuição principal. É a versão recomendada para explicar os resultados sem sobrecarregar cada slide.

**Versão de até 15 minutos:** usar os dois minutos adicionais para interpretar os erros dos modelos e explicar a escolha final. Manter detalhes de parâmetros, códigos e tabelas completas como apoio para perguntas.

**Enquanto a parte de modelos não estiver pronta:** apresentar os slides 1 a 9 e o fechamento, totalizando aproximadamente 10 minutos. Os slides 10 e 11 permanecem no roteiro de montagem, sem serem exibidos como resultados.

## Conferência antes da montagem final

- Manter o alvo de classificação consistente com a futura etapa de modelos.
- Identificar o denominador: **8.849 linhas na exploração**, **7.201 na preparação** e **5.760 nas associações do treino**.
- Distinguir frequência de notificações de risco de acidente; associação de causalidade; variância explicada de desempenho preditivo.
- Usar fonte e recorte em rodapé, deixando referências completas e tabelas extensas em slides de apoio.
- Ensaiar as falas com os gráficos na tela e ajustar as pausas ao tempo disponível.
