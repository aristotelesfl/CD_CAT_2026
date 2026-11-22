# Atividade 2 — Preparar os dados para classificar a parte do corpo atingida

A pergunta é **qual categoria será registrada no campo `Parte Corpo Atingida` de uma CAT?** Cada registro tem uma única resposta. “Dedo”, “Joelho”, “Ombro” e “Partes múltiplas” são exemplos de classes possíveis. A análise simula o primeiro relato de um acidente já ocorrido. Os CSVs trazem a CAT preenchida, por isso a disponibilidade do tipo e do agente do acidente nesse primeiro relato é uma hipótese do estudo.

**Começar com o agente informado, o tipo do acidente e o setor do empregador** (divisão da CNAE), quando conhecidos no relato inicial. Comparar a ocupação (CBO) como quarta entrada antes de decidir se vale a pena mantê-la. Todas as entradas são categorias. As datas servem apenas para organizar os registros. A lista de entradas também exclui idade, mês, dia da semana e intervalos entre datas.

## Como definir a resposta

- Usar a UF **do acidente** registrada como Ceará e a data do acidente entre janeiro e junho de 2026. Das 8.849 linhas de origem, contar uma vez cada combinação idêntica dos 27 valores brutos. Isso produz 7.201 registros distintos. Guardar o vínculo entre cada registro e suas linhas de origem. [Análise exploratória](../relatorio_analise_exploratoria.md)
- Manter o texto original de `Parte Corpo Atingida` e criar `parte_atingida_classe` padronizando espaços e maiúsculas. Preservar as categorias registradas, inclusive as raras, as múltiplas e as descrições truncadas. Por exemplo, `Mao (Exceto Punho ou` é um rótulo observado. Guardá-lo como tal evita adivinhar o restante da descrição. Uma CAT com “partes múltiplas” tem uma classe própria.
- Se a resposta estiver vazia ou marcada como `{ñ class}`, guardar a linha e o motivo na auditoria e excluí-la do treino e da avaliação. Uma entrada ausente recebe a categoria “desconhecida” e a CAT continua elegível. Se surgir na avaliação uma classe informada que o treino nunca viu, contá-la no denominador e relatar a dificuldade de prevê-la.
- Em janeiro–maio há **5.988 registros distintos, 42 classes informadas e nenhum alvo ausente**. “Dedo” aparece 1.166 vezes e “Joelho”, 330. Seis classes têm menos de dez registros cada. Por isso vamos medir tanto a proporção total de acertos quanto o resultado de cada classe.

## O que os 27 campos acrescentam?

A tabela usa a posição de cada coluna no CSV porque há nomes repetidos. As contagens são do desenvolvimento (janeiro–maio), antes de qualquer agrupamento aprendido com os dados.

| Posição e campo | Decisão | Evidência ou motivo |
| --- | --- | --- |
| 1 · Agente causador | Usar como entrada se informado no primeiro relato. | Há 187 descrições informadas e 119 ausências. Sozinho, foi o campo com melhor resultado entre os candidatos testados. Usar o texto observado e padronizado. Só recuperar o nome completo quando houver uma única correspondência no dicionário. |
| 18 · Tipo do acidente | Usar como entrada se conhecido no primeiro relato. | Tem três categorias e está preenchido nos 5.988 registros. Distingue contextos como acidente típico e de trajeto com poucas colunas. |
| 7–8 · CNAE, código e descrição | Usar uma versão do código por vez. Começar pela divisão. | Há 288 códigos informados. O dicionário os resume em 69 divisões observadas. O agrupamento funcionou bem na comparação abaixo. Usar a descrição apenas para explicar o código. |
| 3–4 · CBO, código e descrição | Testar a contribuição adicional da ocupação completa e da família ocupacional. | Há 576 códigos informados e 287 famílias confirmadas. A descrição falta em 918 registros, mas o código falta em apenas um. Na primeira comparação, acrescentar CBO às outras três entradas reduziu o F1 médio entre as classes. |
| 16 · Parte do corpo atingida | Usar exclusivamente como resposta. | Inserir seu texto, um código equivalente ou um grupo anatômico entre as entradas revelaria a classe. |
| 5–6 e 14 · CID-10, sua descrição e natureza da lesão | Excluir das entradas. | São informações clínicas do acidente já caracterizado. O diagnóstico pode nomear diretamente a região afetada. |
| 2, 21–25 · Duas datas do acidente, afastamento, despacho, nascimento e emissão | Excluir as seis colunas e tudo que for calculado a partir delas das entradas. | Acidente e emissão organizam os cortes de treino e avaliação. A data de despacho está ausente nos 5.988 registros. |
| 11, 17 e 26 · Filiação do segurado, sexo e tipo de empregador | Deixar fora da primeira seleção. | Testado isoladamente, cada campo obteve o mesmo resultado da regra que sempre escolhe a classe mais frequente. Esse teste mede a utilidade de cada campo usado sozinho. |
| 9, 10, 12 e 15 · Emitente, espécie do benefício, indicação de óbito e origem do cadastro | Reservar para auditoria. | Descrevem o registro, o benefício ou o desfecho. A espécie do benefício tem um único valor no desenvolvimento. A origem do cadastro tem um único valor informado e 575 ausências. |
| 13, 19, 20 e 27 · Município do empregador, UF do acidente, UF do empregador e CNPJ/CEI | Usar a UF do acidente para o recorte. Reservar os demais para auditoria. | A UF do acidente é constante no recorte. O endereço identifica o empregador, com a divergência de UFs já descrita na AED. Há 2.435 identificadores de empregador. Usá-los favoreceria memorizar empresas. |

## Como verificamos quais entradas merecem prioridade?

A primeira comparação usa uma regra simples. Para cada combinação de entradas, prevê a parte do corpo mais frequente nos registros anteriores com aquela combinação. Para combinações inéditas, consulta grupos menores e, por último, a classe mais frequente do treino. Todas as opções foram avaliadas nas mesmas CATs de março, abril e maio. A coluna **F1 por classe (média)** dá o mesmo peso a cada classe presente no mês e considera tanto os acertos quanto as confusões. Cada mês tem o mesmo peso no resultado abaixo.

| Entradas usadas pela regra | Acertos | F1 por classe (média) |
| --- | ---: | ---: |
| Sempre escolher a classe mais frequente | 19,29% | 0,81% |
| Ocupação (CBO) | 20,28% | 3,71% |
| Atividade econômica (CNAE) | 21,77% | 4,11% |
| Tipo do acidente | 25,28% | 3,23% |
| Agente informado | 27,25% | 7,02% |
| Tipo e agente | **27,85%** | 7,69% |
| Tipo e divisão da CNAE | 24,35% | 5,03% |
| Tipo, agente e CNAE completa | 25,89% | 9,00% |
| Tipo, agente e divisão da CNAE | 26,16% | **9,25%** |
| Tipo, agente, CNAE e CBO completas | 25,36% | 8,71% |
| Tipo, agente, divisão da CNAE e família da CBO | 25,21% | 8,89% |

**Decisão para a atividade 02.** A divisão da CNAE oferece o melhor ponto de partida para representar as várias partes do corpo. A maior taxa de acertos ocorreu com apenas tipo e agente. Levar as duas opções para a comparação e observar quais classes ganham ou perdem. Os valores baixos de F1 mostram que ainda é difícil reconhecer várias classes. Os resultados valem para essa regra simples e para os três meses de validação. Quando o agente ainda for desconhecido no primeiro relato, avaliar também o cenário com os campos disponíveis, mantendo as mesmas linhas de validação. Para reproduzir a tabela e o perfil das 27 colunas, executar `python atividades/analisar_colunas.py` na raiz do projeto. [Código da análise](analisar_colunas.py)

## Como preparar e reduzir as entradas

1. **Conferir a leitura.** Aplicar as regras do [plano compartilhado](README.md) para os seis arquivos e os dicionários. Guardar os códigos como texto, inclusive zeros à esquerda. Auditar, por campo, valores distintos, ausências, constantes, repetições e pares código–descrição. Conferir que as junções preservam a quantidade de linhas. Códigos como `000000` na CBO e `0000` na CNAE significam “não informado”. Guardar o motivo de cada ausência. Se houver código informado fora do dicionário, conservá-lo na versão completa e marcar seu grupo como desconhecido.
2. **Separar os meses.** Reservar os 1.213 registros de junho para o teste da atividade 03. Validar em março, abril e maio usando os meses anteriores para treino. Exigir emissão válida, a partir do acidente e anterior ao primeiro dia do mês avaliado. Os treinos têm, respectivamente, 1.816, 3.004 e 4.203 registros antes do filtro de classe. Para o ajuste antes de junho são 5.565. Conferir as duas datas do acidente e usar a única data válida quando só uma puder ser lida. Guardar para auditoria os conflitos e as linhas sem data de acidente válida. Nas avaliações, considerar o rótulo observado nos arquivos, inclusive nas emissões posteriores ao mês avaliado.
3. **Medir a redução.** Partir da versão detalhada com uma coluna de sim/não para cada categoria de agente, tipo, CBO e CNAE. Comparar, nas mesmas linhas, a retirada de campos inteiros e a troca dos códigos por grupos de ocupação e atividade econômica. Registrar quantas colunas numéricas sobram em cada versão. Completar a comparação com duas técnicas da disciplina.
   - **Seleção por informação mútua.** Manter a metade das colunas de sim/não mais associadas à classe no treino. Registrar quais permaneceram e se a escolha se repete entre os meses.
   - **PCA.** Centrar as colunas de sim/não e manter sua escala original para evitar dar peso excessivo às categorias raras. Reter o menor número de componentes que explique 95% da variação do treino. Mostrar a variação explicada por componente e acumulada, quais categorias mais contribuem e o que se observa nas duas primeiras componentes.
4. **Comparar de forma justa.** Aprender as categorias, a seleção e a PCA apenas com o treino de cada mês. Permitir categorias novas na validação. Usar o mesmo classificador de referência nas matrizes completas e reduzidas (regressão logística multiclasse, com os mesmos parâmetros). Comparar tamanho, tempo, acertos, F1 médio entre classes e facilidade de interpretação. Em caso de resultados semelhantes, preferir a versão com menos entradas e nomes compreensíveis.

## O que entregar à atividade 03

- Notebook executável e relatório curto com o perfil das colunas, contagens por classe e mês, exclusões, comparação das reduções e limitações do primeiro relato.
- Duas bases separadas, desenvolvimento e teste de junho, com um ID por combinação distinta, as entradas **antes** da transformação em colunas numéricas e a resposta `parte_atingida_classe`. Entregar a lista explícita de entradas de cada versão, as regras de preparação e a tabela com os IDs de treino e avaliação em cada mês.
- Conferir que as contagens por classe mais os alvos ausentes fecham o total, que nenhum ID está simultaneamente no treino e na avaliação de um mesmo corte e que as matrizes contêm apenas as entradas previstas. Origem, datas e demais campos de auditoria ficam acessíveis separadamente. [Atividade 03](03_modelos_supervisionados.md)
