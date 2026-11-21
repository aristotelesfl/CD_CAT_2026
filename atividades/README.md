# Plano das atividades com dados de CAT de 2026

## Objetivo e escopo

Adaptar os três projetos da disciplina aos registros de Comunicação de Acidente de Trabalho (CAT) disponíveis em `datasets/CAT_2026/`, com foco em acidentes cuja UF de ocorrência está registrada como Ceará. A unidade inicial de análise é o **registro de CAT**; não presumir que cada linha corresponda a uma pessoa, acidente único ou empresa única. Os temas e dados de varejo dos enunciados são exemplos substituíveis; suas exigências metodológicas e entregas continuam aplicáveis. Não transferir para a CAT as dimensões, o dicionário ou a distribuição de classes das bases de exemplo.

1. [Análise exploratória](01_analise_exploratoria.md): formular perguntas e produzir evidências sobre os registros.
2. [Pré-processamento e redução de dimensionalidade](02_pre_processamento_reducao.md): diagnosticar e preparar os dados, comparando representações.
3. [Modelos supervisionados e avaliação](03_modelos_supervisionados.md): definir um problema viável, comparar os modelos exigidos e justificar a escolha.

## Dados e cuidados compartilhados

- Entradas: seis arquivos `D.SDA.PDA.005.CAT.202601.csv` a `D.SDA.PDA.005.CAT.202606.csv`. Guardar os arquivos originais sem alteração e registrar arquivo de origem e linha de origem durante a ingestão.
- A inspeção inicial encontrou separador `;`, bytes compatíveis com Latin-1, espaços em valores e cabeçalhos repetidos para `CBO`, `CID-10`, `CNAE2.0 Empregador` e `Data Acidente`. Confirmar codificação e esquema em **todos** os arquivos; preservar colunas por posição e atribuir nomes únicos antes de selecionar campos. Comparar as duas datas de acidente e os pares código/descrição antes de eliminar qualquer coluna.
- Há exemplos de `00/00/0000` e `{ñ class}`; investigar seu significado e frequência, mantendo a distinção entre ausência, código não classificado e erro quando possível. Não converter automaticamente em zero.
- O sufixo mensal do arquivo não prova que a data do acidente pertença ao mesmo mês: há exemplo de acidente em abril no arquivo de junho. Verificar cobertura e significado temporal; não assumir que o sufixo equivale à data do acidente, emissão ou atualização sem documentação.
- Registros repetidos podem ser reapresentações, notificações distintas ou duplicatas; sem chave confiável, quantificar e investigar antes de remover. Não inventar identificador de pessoa ou acidente.
- Preservar códigos como texto, inclusive zeros à esquerda. Investigar valores truncados e categorias de alta cardinalidade. `CNPJ/CEI Empregador`, datas de nascimento e informações de saúde exigem cuidado: usar apenas quando necessários, evitar exposição em relatórios e exemplos e preferir agregações. Não afirmar anonimização apenas pela remoção de nomes.
- Contagens descrevem notificações disponíveis, não taxas de risco ou incidência populacional sem denominadores adequados. Considerar cobertura, subnotificação, atrasos e possível atualização dos arquivos. Associações não demonstram causalidade.
- Registrar origem, recorte, data de acesso se conhecida, bibliotecas, versões, parâmetros e sementes. Dados derivados e resultados devem ser reproduzíveis sem modificar os arquivos brutos.

## Recorte geográfico e trabalho já realizado

- O objetivo principal é estudar acidentes cuja **UF do acidente** está registrada como Ceará. Os campos disponíveis exigem distinguir **UF do acidente**, **UF do empregador** e **município do empregador**. `Munic Empr = 230440-Fortaleza` identifica município do empregador, não necessariamente município da ocorrência. Não afirmar que os acidentes ocorreram em Fortaleza apenas com esse campo.
- O notebook `CAT2026.ipynb` já examina os seis arquivos, datas, repetições, ausências e distribuições. Suas saídas registradas apontam uma divergência: 10.295 linhas com UF do acidente Ceará, 13.879 com UF do empregador Ceará e apenas 13 com ambos; 9.545 das primeiras indicam empregador no Distrito Federal. Esses números são resultados salvos no notebook e devem ser reproduzidos e conferidos, não considerados validação da origem ou do significado dos campos. Investigar documentação e consistência; até a discrepância ser esclarecida, explicitar que o recorte depende da confiabilidade da UF registrada.
- `main.ipynb` contém um recorte por empregador no Ceará e município de Fortaleza, mas também exige que a UF do acidente seja `{ñ class}`. Esse filtro adicional exclui registros com UF do acidente preenchida e não representa todos os empregadores de Fortaleza. Comparar quantidades e consequências com e sem ele. O notebook ainda aponta para `datasets/CATs`, pasta que foi removida, omite maio e depende de montagem do Google Drive. Atualizar a leitura para `datasets/CAT_2026/`, que contém os seis meses, antes de reutilizar seus resultados.
- Definir a população principal por `UF  Munic.  Acidente = Ceará`, após remover espaços e conferir o significado do campo. Usar UF e município do empregador apenas para diagnóstico e caracterização, sem restringir a população principal. Comparar a sobreposição entre os campos e investigar a divergência; sem validação, manter as conclusões condicionais. Não tratar uma categoria não classificada como Ceará. A base não permite selecionar acidentes ocorridos em Fortaleza, pois não informa o município da ocorrência.
- O período explorado no `CAT2026.ipynb` é de 1º de janeiro a 30 de junho de 2026 pela data do acidente, incluindo CATs emitidas posteriormente presentes nos arquivos. Documentar os limites de disponibilidade e comparar as duas colunas de data do acidente. O notebook encontra 8.849 linhas no recorte de UF do acidente Ceará e, após colapsar linhas idênticas nos 27 campos, 7.201 linhas distintas; isso é uma representação alternativa, não uma contagem comprovada de acidentes únicos. Comparar resultados com e sem esse colapso e investigar a repetição entre arquivos.
- Aproveitar as análises de tipo de acidente, idade e sexo, CNAE, mês do acidente e prazo de emissão já existentes, refazendo-as no recorte escolhido. Usar os dicionários locais para recuperar os rótulos truncados nas CATs, conferindo chaves, descrições e versões e mantendo os valores originais.

## Dicionários para normalização de descrições

As descrições correspondentes às classificações dos arquivos adicionais estão truncadas nos dados brutos de CAT. Os arquivos em `datasets/` são tabelas de referência para recuperar esses rótulos completos, mantendo os valores brutos e os códigos originais. A inspeção dos bytes mostrou codificações distintas: os seis CSVs de CAT e as tabelas de CNAE, CBO e CID não são UTF-8 válido e são compatíveis com `cp1252` e `latin-1`; a amostra é lida corretamente com `latin-1`, mas a codificação de origem deve ser confirmada. Já `agente_causador_acidente_trabalho.csv` é UTF-8 válido e usa vírgula como separador. Não lê-lo como Latin-1, pois isso pode corromper a exibição dos acentos. Os demais arquivos inspecionados usam ponto e vírgula. Preservar códigos como texto e conferir a versão e o significado antes de cruzar:

| Campo da CAT | Referência local | Chave e cuidado |
| --- | --- | --- |
| `CBO` | `CBOs/CBO2002 - Ocupacao.csv` | `CODIGO` de seis dígitos; usar `TITULO`. Os arquivos de família e grupos são níveis hierárquicos distintos; sinônimos e perfil podem ter várias linhas por código. |
| `CID-10` | `CIDs/CID-10-CATEGORIAS.CSV` e `CID-10-SUBCATEGORIAS.CSV` | Comparar o código normalizado com `CAT` ou `SUBCAT`, conforme o nível; preservar o código e não presumir correspondência por prefixo quando a subcategoria não for encontrada. CID-O é outra classificação. |
| `CNAE2.0 Empregador` | `cnae20.csv` | O arquivo usa `cod_classe` com pontuação e dígito verificador; conferir a correspondência dos quatro dígitos da CAT com a classe normalizada. Na inspeção inicial, os quatro primeiros dígitos geraram 673 chaves distintas sem ambiguidades nessa tabela; validar novamente na execução. |
| `Agente Causador Acidente` | `agente_causador_acidente_trabalho.csv` | O CSV de CAT inspecionado traz descrição, sem coluna de código de agente identificada. A descrição na CAT está truncada; comparar com as descrições completas da referência e recuperar o rótulo quando a correspondência for inequívoca e auditável. Registrar e revisar casos com mais de uma correspondência possível. |

Em cada junção, validar unicidade da chave, manter a quantidade de linhas e registrar quantos registros e códigos distintos foram associados, não encontrados ou ambíguos. Não substituir valores desconhecidos por suposições nem excluir linhas sem correspondência. Guardar descrição original e descrição normalizada separadamente; revisar divergências, códigos incompletos e descrições truncadas. Em particular, não unir diretamente tabelas com múltiplos sinônimos ou atividades por código sem controlar multiplicação de registros. Documentar critérios de correspondência, exemplos e proporção de cobertura no recorte de UF do acidente Ceará.

## Organização sugerida dos produtos

Criar um notebook executável e um relatório curto por etapa, além das bases derivadas e artefatos exigidos nos respectivos roteiros. Usar caminhos relativos à raiz do projeto e documentar como instalar dependências e executar cada notebook do início ao fim. Resultados e conclusões devem ser produzidos a partir dos dados efetivamente processados; estes arquivos são instruções, não resultados da análise.

## Fontes dos requisitos

- `context/atividade_projeto_aed.pdf`.
- `context/atividade_projeto_pre_processamento_reducao_dimensionalidade.pdf`.
- `context/modelos_supervisionados.pdf`.
