# Acidentes de trabalho no Ceará — CAT 2026

Pesquisa de Ciência de Dados sobre os registros de Comunicação de Acidente de Trabalho (CAT) cuja **UF do acidente está informada como Ceará**, com data do acidente entre 1º de janeiro e 30 de junho de 2026. O objetivo é descrever o perfil dos registros, as atividades econômicas, os tipos de acidente, as partes do corpo atingidas e sua distribuição no tempo.

A análise considera a UF do acidente, independentemente da localização do empregador. O município disponível na base é o do empregador; por isso, ele não permite identificar quais acidentes ocorreram em Fortaleza. A divergência observada entre os campos de UF do acidente e do empregador precisa ser investigada e considerada na interpretação dos resultados.

## Perguntas de pesquisa

| Nº | Pergunta | Atributos e análise proposta |
| --- | --- | --- |
| 1 | Qual é o perfil dos trabalhadores acidentados? | **Sexo e idade:** apresentar distribuição por sexo e faixas etárias; calcular idade na data do acidente e informar dados ausentes ou inválidos. |
| 2 | Quais atividades econômicas apresentam mais acidentes registrados? | **CNAE do empregador:** apresentar contagens e proporções por atividade, recuperando as descrições completas pelo código e informando os registros sem classificação. |
| 3 | Quais são os principais tipos de acidentes? | **Tipo do acidente:** comparar frequências e proporções das categorias registradas. |
| 4 | Quais partes do corpo são mais atingidas nos acidentes de trabalho? | **Parte do corpo atingida:** comparar as categorias registradas, incluindo categorias desconhecidas ou múltiplas quando presentes. |
| 5 | Existe diferença entre a data do acidente e a emissão da CAT? | **Datas do acidente e de emissão:** calcular o intervalo em dias, apresentar sua distribuição e mediana, e investigar datas inválidas ou intervalos negativos. |
| 6 | Como os registros variaram ao longo do primeiro semestre de 2026? | **Data do acidente:** apresentar contagens mensais de janeiro a junho e discutir possíveis efeitos de atrasos de registro e cobertura. |

As respostas devem apresentar evidências quantitativas ou visuais, com denominadores e quantidade de registros considerados. Resultados existentes nos notebooks são preliminares e devem ser reproduzidos após a definição e validação dos tratamentos da base.

## Dados

- [`datasets/CAT_2026/`](datasets/CAT_2026/): seis arquivos CSV mensais, de janeiro a junho de 2026. O período da pesquisa é definido pela **data do acidente**, não pelo nome do arquivo; registros podem aparecer em arquivos de outros meses ou ter emissão posterior a junho.
- [`datasets/cnae20.csv`](datasets/cnae20.csv), [`datasets/CBOs/`](datasets/CBOs/) e [`datasets/CIDs/`](datasets/CIDs/): tabelas de referência para recuperar descrições de classificações truncadas nas CATs.
- [`datasets/agente_causador_acidente_trabalho.csv`](datasets/agente_causador_acidente_trabalho.csv): referência para descrições de agente causador; a correspondência textual deve ser verificada quando houver ambiguidade.
- [`context/`](context/): enunciados das atividades da disciplina.

Os CSVs de CAT usam ponto e vírgula e são compatíveis com leitura `latin-1`; o arquivo de agente causador é UTF-8 e usa vírgula. As demais tabelas de referência inspecionadas são compatíveis com `latin-1` e usam ponto e vírgula. Confirmar a codificação de origem e preservar códigos como texto, inclusive zeros à esquerda.

## Abordagem

1. Ler os seis arquivos, preservar sua origem e aplicar o recorte de UF do acidente Ceará e data do acidente no primeiro semestre.
2. Examinar cabeçalhos repetidos, consistência das datas, valores ausentes e não classificados e possíveis repetições entre arquivos. Comparar resultados antes e depois de qualquer tratamento de linhas idênticas e documentar as decisões.
3. Associar códigos aos dicionários para recuperar rótulos completos, preservando as descrições originais e verificando cobertura, ambiguidades e quantidade de linhas antes e depois das junções.
4. Responder às seis perguntas com tabelas, gráficos e interpretações fundamentadas, identificando limitações e questões em aberto.
5. Prever a categoria registrada em **Parte Corpo Atingida** para cada CAT. A atividade 02 examina quais campos do primeiro relato ajudam a distinguir as classes e compara formas de reduzir as entradas. A atividade 03 compara classificadores e avalia as classes nos acidentes de junho. [Preparação dos dados](atividades/02_pre_processamento_reducao.md) e [avaliação dos modelos](atividades/03_modelos_supervisionados.md).

## Notebooks e organização

- [Modelos supervisionados](03_modelos_supervisionados.ipynb) compara KNN, árvore de decisão, Random Forest e MLP. O [relatório da atividade 03](relatorio_modelos_supervisionados.md) apresenta a escolha na validação temporal e o teste de junho.
- [Pré-processamento e redução de dimensionalidade](02_pre_processamento_reducao.ipynb) prepara a classificação de parte do corpo atingida. O [relatório da atividade 02](relatorio_pre_processamento_reducao.md) explica a escolha das entradas e compara as reduções.
- [`CAT2026.ipynb`](CAT2026.ipynb): análise exploratória iniciada, incluindo conferência dos arquivos, localização, período, repetições e algumas distribuições.
- [`main.ipynb`](main.ipynb): exploração anterior; aponta para uma pasta removida, omite maio e usa outro recorte geográfico. Precisa ser adaptado antes de ser reutilizado.
- [`atividades/README.md`](atividades/README.md): plano detalhado, decisões de dados e critérios compartilhados das atividades.

As atividades 01 e 02 usam caminhos relativos à raiz do projeto. Os respectivos relatórios descrevem o ambiente de execução. Os notebooks exploratórios anteriores incluem caminhos do Google Colab/Google Drive.

## Limites de interpretação

Uma linha é um registro disponível na base e não necessariamente uma pessoa ou acidente único. Sem identificador único, linhas iguais não comprovam o mesmo acidente, nem linhas diferentes comprovam acidentes distintos. Contagens de CATs não representam taxas de risco ou incidência sem denominadores adequados, e podem ser afetadas por cobertura, subnotificação, atrasos e atualizações. A confiabilidade do recorte geográfico também depende de esclarecer a discrepância observada entre os campos de UF. Associações observadas não demonstram causalidade.
