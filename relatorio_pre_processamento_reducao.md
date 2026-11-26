# Relatório de pré-processamento e redução de dimensionalidade

## 1. Introdução

Os registros de Comunicação de Acidente de Trabalho (CAT) reúnem informações sobre o acidente, o trabalhador e o empregador. Seu uso em um experimento de classificação exige examinar a qualidade dos dados, definir quais informações estarão disponíveis para a previsão e transformar os atributos em uma representação numérica adequada.

Esta etapa investiga a preparação dos dados para a classificação de **Indica Óbito Acidente**, considerando **Sim** como classe positiva. O recorte abrange os registros cuja UF do acidente está informada como Ceará e cuja data do acidente pertence ao primeiro semestre de 2026. As análises descrevem os registros disponíveis nessa base. A interpretação de suas contagens depende da cobertura, do preenchimento e da identificação das CATs.

A redução de dimensionalidade foi estudada por meio de filtros de variância, qui-quadrado e informação mútua, seleção sequencial forward, seleção pela importância de uma árvore e análise de componentes principais (PCA). Os resultados apresentados foram extraídos da execução do notebook que acompanha este relatório. [Notebook do experimento](02_pre_processamento.ipynb)

## 2. Objetivo

O objetivo geral foi preparar os dados e comparar as representações obtidas por diferentes técnicas de seleção e extração de características para o problema de classificação de óbito.

Os objetivos específicos foram os seguintes.

- Examinar duplicatas, ausências, códigos sem informação e descrições truncadas.
- Definir os atributos utilizados no experimento e separar treino e teste.
- Transformar as categorias em indicadores binários por one-hot encoding.
- Aplicar métodos de seleção sobre uma base comum e identificar suas escolhas em comum.
- Aplicar PCA, analisar a variância explicada e interpretar as componentes.
- Discutir a redução de dimensão obtida e as limitações relacionadas ao desbalanceamento e às categorias raras.

## 3. Metodologia

### 3.1. Fonte e recorte dos dados

Foram utilizados os seis arquivos CSV mensais de janeiro a junho de 2026, disponíveis em `datasets/CAT_2026`. A leitura empregou separador ponto e vírgula e codificação `latin-1`. Os campos CBO e CNAE foram lidos como texto para preservar zeros à esquerda.

Os arquivos foram concatenados e filtrados pela UF do acidente Ceará. A data do acidente foi convertida para o formato de data, com valores inválidos tratados como ausentes. Em seguida, foram selecionadas as datas entre 1º de janeiro e 30 de junho de 2026. O recorte temporal foi estabelecido pelo valor registrado em cada linha, independentemente do mês indicado no nome do arquivo.

### 3.2. Limpeza e tratamento dos atributos

A inspeção inicial apresentou os tipos das colunas, a quantidade e o percentual de ausentes e o número de valores distintos. O marcador `{ñ class}` foi reconhecido como ausência. A detecção de duplicatas considerou os 27 campos originais, preservando uma ocorrência de cada combinação idêntica.

A remoção de duplicatas foi uma decisão de preparação da base. Sem um identificador único do acidente, a contagem de combinações distintas permanece sujeita às limitações de identificação dos registros.

No agente causador, descrições truncadas foram comparadas com o dicionário disponível no projeto. A associação ao código foi realizada quando havia uma correspondência única. Ausências, ambiguidades e descrições sem correspondência receberam a categoria `Desconhecido`. A situação de cada associação foi mantida na variável de auditoria `resultado_agente`.

Os códigos `000000` na CBO e `0000` na CNAE também foram tratados como desconhecidos. Nas três entradas utilizadas pelo one-hot, foram removidos espaços nas extremidades dos textos, e valores vazios ou ausentes foram preenchidos com `Desconhecido`.

### 3.3. Definição do alvo e das entradas

A revisão inicial dos atributos considerou a função de cada campo, sua diversidade e sua disponibilidade no momento da previsão.

| Campo ou grupo | Tratamento adotado |
|---|---|
| CNPJ/CEI Empregador | Exclusão do identificador por decisão de escopo |
| UF do acidente e espécie do benefício | Exclusão de campos constantes no recorte |
| Origem de Cadastramento CAT | Exclusão por escopo administrativo, considerando que o campo contém Internet e ausências |
| Data Despacho Benefício | Exclusão do campo preenchido com `00/00/0000` |
| CID-10 e sua descrição | Exclusão considerando um cenário de previsão anterior à disponibilidade do diagnóstico |
| Descrições de CBO e CNAE | Exclusão das descrições associadas aos códigos mantidos |

Essa revisão produziu uma tabela com 18 colunas, incluindo o alvo. Após a separação de `Indica Óbito Acidente`, restaram 17 atributos candidatos. Para os experimentos de redução, foram escolhidas três entradas categóricas.

| Entrada | Informação representada |
|---|---|
| Tipo do Acidente | Categoria registrada como típico, trajeto ou doença |
| Agente Causador Acidente | Código associado ao agente causador ou categoria desconhecida |
| Tipo de Empregador | Categoria de identificação do empregador |

A escolha dessas três entradas define o alcance das comparações. Sua utilização pressupõe que estejam disponíveis no momento da previsão. Essa hipótese deve ser verificada antes de uma aplicação operacional.

### 3.4. Divisão e codificação dos dados

Foi realizada uma divisão aleatória estratificada, com 80% dos registros no treino, 20% no teste e `random_state=42`. A estratificação preservou aproximadamente a proporção das classes. As análises por tipo de acidente e agente causador foram realizadas no treino.

O one-hot encoding criou uma coluna binária para cada categoria aprendida no treino. Por exemplo, `Tipo do Acidente_Trajeto` assume valor 1 quando o registro é de trajeto e 0 nos demais registros. Esse procedimento gerou 163 indicadores a partir das três entradas.

O encoder foi ajustado no treino e aplicado ao teste com `handle_unknown="ignore"`. Uma categoria encontrada apenas no teste é representada por zeros no bloco de indicadores do atributo correspondente. As matrizes foram convertidas em DataFrames densos para facilitar a apresentação dos nomes das colunas e a aplicação do procedimento didático de PCA.

### 3.5. Métodos de seleção

Primeiro foi aplicado o filtro de variância zero. A base resultante serviu de entrada para qui-quadrado, informação mútua, Wrapper e árvore. A interseção dos filtros foi construída como uma representação adicional.

| Técnica | Critério e configuração |
|---|---|
| Variância | `VarianceThreshold(threshold=0.0)`, removendo indicadores constantes no treino |
| Qui-quadrado | `SelectKBest` com os 50 maiores escores de associação entre indicador e alvo |
| Informação mútua | `SelectKBest` com os 50 maiores escores, usando `discrete_features=True` para os indicadores binários |
| Interseção | Retenção dos indicadores aprovados por variância, qui-quadrado e informação mútua |
| Wrapper forward | Seleção sequencial de 8 indicadores, com árvore de profundidade máxima 4, pesos de classe balanceados e average precision em três partições estratificadas |
| Método embutido | Árvore de profundidade máxima 5, mínimo de 8 registros por folha, pesos de classe balanceados e retenção dos indicadores com importância maior que zero |

As quantidades de 50 indicadores nos filtros supervisionados e 8 no Wrapper foram parâmetros definidos para o experimento. A quantidade utilizada pela árvore decorreu do ajuste realizado. As divisões internas do Wrapper e as árvores utilizaram `random_state=42`.

O qui-quadrado e a informação mútua avaliam cada indicador individualmente. O Wrapper acrescenta indicadores considerando sua contribuição junto aos que já foram escolhidos. A árvore utiliza os atributos nas divisões construídas durante o treinamento e atribui importância conforme a redução de impureza obtida.

### 3.6. Extração com PCA

O PCA foi aplicado à base produzida pelo filtro de variância. Antes do ajuste, os indicadores foram padronizados com `StandardScaler`, utilizando médias e desvios-padrão calculados no treino. Nos indicadores binários, essa transformação aumenta o peso relativo das categorias raras.

Inicialmente, foram calculadas todas as componentes para examinar o scree plot e a variância explicada acumulada. Em seguida, foi ajustada uma representação com retenção de 90% da variância, usando `PCA(n_components=0.90, svd_solver="full")`.

As componentes são combinações lineares dos indicadores padronizados. Foram examinados seus coeficientes, os maiores pesos em módulo e a projeção dos registros nas duas primeiras componentes. O alvo foi utilizado para identificar visualmente os registros com óbito. A construção das componentes depende da variação dos dados de entrada.

## 4. Resultados

### 4.1. Preparação e distribuição dos registros

O recorte inicial reuniu 8.849 linhas e 27 campos. Foram identificadas 3.296 linhas envolvidas em duplicatas exatas. A remoção das ocorrências adicionais eliminou 1.648 linhas e produziu 7.201 combinações distintas dos campos originais.

No tratamento do agente causador, os resultados foram os seguintes.

| Situação da associação ao dicionário | Registros |
|---|---:|
| Correspondência única | 6.538 |
| Descrição sem correspondência | 393 |
| Descrição ambígua | 131 |
| Ausência | 139 |
| Total | 7.201 |

Os três últimos grupos resultaram em 663 registros com agente representado como `Desconhecido`.

A distribuição do alvo evidencia o desbalanceamento.

| Conjunto | Total de registros | Sem óbito | Com óbito | Percentual com óbito |
|---|---:|---:|---:|---:|
| Base após deduplicação | 7.201 | 7.174 | 27 | 0,37% |
| Treino | 5.760 | 5.738 | 22 | 0,38% |
| Teste | 1.441 | 1.436 | 5 | 0,35% |

No treino, os acidentes de trajeto reuniram 12 óbitos em 1.373 registros, aproximadamente 0,87%. Os acidentes típicos reuniram 10 óbitos em 3.982 registros, aproximadamente 0,25%. Entre os 405 registros classificados como doença, foram observados zero óbitos.

### 4.2. Dimensão das representações

A tabela compara a quantidade de colunas de cada representação. A redução percentual foi calculada em relação aos 163 indicadores iniciais.

| Representação | Colunas resultantes | Redução da dimensão |
|---|---:|---:|
| One-hot completo | 163 | 0,00% |
| Após filtro de variância | 163 | 0,00% |
| Qui-quadrado | 50 | 69,33% |
| Informação mútua | 50 | 69,33% |
| Interseção dos filtros | 49 | 69,94% |
| Wrapper | 8 | 95,09% |
| Método embutido | 10 | 93,87% |
| PCA com retenção de 90% | 142 | 12,88% |

Todos os indicadores apresentaram variância positiva no treino. O filtro com limiar zero manteve as 163 colunas, permitindo que categorias raras continuassem participando das demais seleções.

### 4.3. Qui-quadrado, informação mútua e interseção

O maior escore de qui-quadrado foi obtido pelo indicador de medicamento em geral, código `305068300`. A categoria reuniu apenas três registros e um óbito. O alto escore decorre da diferença entre a contagem observada e a esperada em uma base com baixa frequência de óbito.

| Indicador | Registros no treino | Óbitos | Escore qui-quadrado |
|---|---:|---:|---:|
| Medicamento em geral | 3 | 1 | 85,6112 |
| Edifício ou estrutura, código `302050900` | 22 | 1 | 10,0231 |
| Acidente de trajeto | 1.373 | 12 | 8,7369 |
| Agente do acidente inexistente | 92 | 2 | 7,7644 |
| Veículo, código `303075900` | 336 | 4 | 5,7729 |

A leitura conjunta dos escores e das contagens evidencia que as associações têm suportes amostrais distintos. No caso de medicamento em geral, a posição no ranking depende de um único registro com óbito.

Na informação mútua, o indicador de trajeto ocupou a primeira posição, seguido por medicamento em geral e acidente típico. A ordem diferiu daquela obtida pelo qui-quadrado, embora os conjuntos selecionados tenham sido muito semelhantes.

Os dois métodos compartilharam 49 dos 50 indicadores escolhidos. O qui-quadrado incluiu adicionalmente o indicador de chão, código `302010550`, enquanto a informação mútua incluiu o de bicicleta, código `303075100`. A interseção com o filtro de variância produziu uma representação com 49 indicadores.

### 4.4. Wrapper, árvore e concordância entre métodos

O Wrapper selecionou os três indicadores de tipo do acidente e cinco indicadores de agente causador. Estes correspondem a rua ou estrada, calçada ou caminho para pedestre, escada permanente, chão e agente do acidente inexistente.

A árvore do método embutido utilizou dez indicadores. Acidente de trajeto apresentou a maior importância, com valor aproximado de 0,332, seguido por agente do acidente inexistente, piso de veículo e edifício ou estrutura. Essas importâncias descrevem a participação relativa dos atributos nas reduções de impureza obtidas por essa árvore.

Quatro indicadores foram escolhidos por qui-quadrado, informação mútua, Wrapper e método embutido.

- Acidente de trajeto.
- Acidente típico.
- Calçada ou caminho para pedestre.
- Agente do acidente inexistente.

Os indicadores de tipo de empregador ficaram fora das quatro seleções. No treino, CNPJ/CGC estava presente em 5.755 dos 5.760 registros, indicando pequena diversidade desse atributo na amostra utilizada.

### 4.5. PCA e variância explicada

A quantidade de componentes necessária para atingir cada limite de variância acumulada foi a seguinte.

| Limite de variância acumulada | Componentes necessárias |
|---|---:|
| Pelo menos 85% | 134 |
| Pelo menos 90% | 142 |
| Pelo menos 95% | 150 |

A representação escolhida produziu 142 componentes e preservou 90,15% da variância da matriz padronizada. A redução de dimensão foi de 12,88%. Esse resultado mostra que a variação está distribuída entre muitas componentes.

A primeira componente explicou aproximadamente 1,54% da variância e apresentou coeficientes destacados para acidente típico e trajeto, com sinais opostos, além de agentes relacionados a veículos e vias. A segunda explicou aproximadamente 1,38% e apresentou pesos destacados para tipo de empregador.

Juntas, as duas primeiras componentes preservaram 2,92% da variância padronizada. Na projeção bidimensional, os registros com óbito apareceram sobrepostos a registros sem óbito. A pequena proporção de variância representada limita as conclusões sobre a estrutura completa dos dados a partir desse gráfico.

## 5. Discussão

### 5.1. Redução de dimensão e escolha de uma representação

Os métodos de seleção produziram representações mais compactas, conservando o significado dos indicadores escolhidos. A interseção reduziu a matriz para 49 colunas e apresentou forte concordância entre os dois filtros supervisionados. Wrapper e árvore produziram subconjuntos menores, com critérios que consideram a utilização conjunta dos indicadores.

A quantidade de colunas deve ser interpretada junto aos parâmetros. Os filtros foram configurados para selecionar 50 indicadores, e o Wrapper foi configurado para selecionar oito. A dimensão obtida por essas técnicas reflete esses limites. A capacidade de preservar informação útil para identificar óbitos depende da avaliação preditiva de cada representação.

O PCA com padronização exigiu 142 componentes para atingir a retenção proposta. Essa configuração ofereceu uma redução menor de dimensão e gerou colunas cujo significado é descrito por combinações de indicadores. A padronização do one-hot contribui para dar participação relativa às categorias raras e ajuda a contextualizar a distribuição da variância por muitas componentes.

### 5.2. Categorias raras e interpretação das associações

A categoria de medicamento em geral exemplifica a sensibilidade dos rankings a poucos registros. Seu escore elevado de qui-quadrado foi sustentado por um óbito em três observações. A estabilidade dessa associação depende de sua avaliação em outras partições e amostras.

Trajeto apresentou uma associação observada em um grupo maior, com 12 óbitos em 1.373 registros do treino, e foi destacado pelos diferentes métodos. Esse resultado justifica sua discussão como característica relevante para a classificação no recorte estudado. Uma explicação causal exige investigação específica sobre os acidentes, os registros e os possíveis fatores associados.

O tratamento das descrições truncadas também influencia as entradas. A categoria `Desconhecido` reuniu situações de ausência, ambiguidade e falta de correspondência ao dicionário. Essa decisão preservou os registros, mas agregou situações potencialmente diferentes em um mesmo indicador.

### 5.3. Desbalanceamento e avaliação preditiva

A amostra contém 27 registros com óbito, dos quais 22 ficaram no treino e cinco no teste. Um classificador que atribuísse Não a todos os registros da base teria acurácia de aproximadamente 99,63% e recall de Sim igual a zero. Por isso, a avaliação deve examinar métricas voltadas à classe positiva.

Average precision resume a relação entre precisão e recall ao variar o limiar de decisão. O recall de Sim indica a fração dos óbitos identificados em um limiar escolhido. A precisão e a contagem de falsos positivos ajudam a interpretar quantos alertas gerados correspondem a registros com óbito.

A comparação preditiva entre todas as representações ainda está pendente nesta versão do notebook. A validação interna do Wrapper foi utilizada para escolher seu subconjunto. Para estimar o desempenho das representações, o procedimento deve reajustar o one-hot, os seletores e, quando aplicável, a padronização e o PCA dentro do treino de cada fold, usando partições e classificador comparáveis. O teste deve ser utilizado na avaliação final do procedimento escolhido.

Com cinco óbitos no teste, a identificação de um caso adicional altera o recall em 20 pontos percentuais. Esse tamanho amostral exige considerar a variação dos resultados ao interpretar diferenças entre métodos.

### 5.4. Alcance dos resultados desta etapa

A preparação produziu uma base com 7.201 registros e matrizes consistentes de treino e teste. O experimento documentou o tratamento das ausências e ambiguidades, explicitou as três entradas utilizadas e gerou diferentes representações para a etapa de classificação.

A concordância dos filtros, a presença de trajeto entre os indicadores destacados e a redução limitada obtida pelo PCA padronizado constituem os principais resultados observados. As conclusões se aplicam ao recorte de CATs do Ceará, às entradas escolhidas, à divisão aleatória estratificada e aos parâmetros registrados. A definição da representação final depende da comparação de seu desempenho na identificação de óbitos.
