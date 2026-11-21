# Atividade 1 — Análise exploratória de CAT

## Problema

Investigar padrões nos registros de CAT cuja UF do acidente está registrada como Ceará, no primeiro semestre de 2026, e como variam por tipo de acidente, atividade econômica, ocupação e período. A localização do empregador não define o recorte; a base não identifica o município da ocorrência e não permite selecionar acidentes ocorridos em Fortaleza. Formular perguntas específicas após conhecer os dados. Se a equipe definir um grupo prioritário, explicitar seu critério, justificá-lo e não confundir volume de notificações com risco ou gravidade.

## Instruções

1. Ler o [plano compartilhado](README.md) e revisar as análises já realizadas em `CAT2026.ipynb` e `main.ipynb`; reproduzir e conferir suas saídas. Inspecionar os seis arquivos e documentar origem, unidade de análise, período observado, esquema e limitações. Consolidar com rastreabilidade, preservando os originais e nomes únicos para cabeçalhos repetidos.
2. Quantificar linhas e colunas por arquivo, tipos, ausências e marcadores, duplicatas potenciais e intervalos de datas; comparar datas e colunas repetidas. Investigar discrepâncias entre mês do arquivo, acidente e emissão. Não descartar registros sem justificativa.
3. Definir a população principal pela UF do acidente registrada como Ceará. Investigar a divergência em relação à UF do empregador e o efeito do filtro `{ñ class}` de `main.ipynb`, sem usá-los para restringir a população. Não inferir município de ocorrência; registrar a incerteza sobre a qualidade do campo. Formular perguntas e definir medidas, recortes e denominadores antes de interpretar. Examinar distribuições e, quando fizer sentido, cruzar tipo de acidente, sexo, faixa etária derivada de datas válidas, CNAE, CBO, natureza da lesão, parte atingida e localização. Distinguir UF do acidente da UF do empregador.
4. Usar tabelas e gráficos legíveis, com unidades, categorias, totais, valores ausentes e tamanho dos grupos. Avaliar categorias raras, possíveis distorções, valores extremos e relações redundantes; verificar se padrões persistem em recortes relevantes, evitando inferências frágeis.
5. Redigir de 3 a 5 achados relevantes, cada um acompanhado de números ou visualização e seus denominadores. Explicitar incertezas, limitações e perguntas em aberto; não atribuir causalidade a associações.

## Entregas

- Notebook executável, organizado e comentado, com ingestão, diagnóstico e análises.
- Relatório analítico curto com problema e recorte, evidências, 3 a 5 achados, limitações e próximos passos.

## Critérios de aceitação

- [ ] Pergunta central e perguntas analíticas são pertinentes à CAT; eventual grupo prioritário tem definição operacional e justificativa.
- [ ] O recorte principal usa a UF do acidente registrada como Ceará; a divergência entre campos foi investigada e a incerteza sobre a localização está explícita.
- [ ] Todos os arquivos utilizados e o recorte estão identificados; integridade, marcadores, duplicatas e datas são investigados e decisões registradas.
- [ ] Cada análise contribui para responder às perguntas e informa medidas, denominadores e tamanho dos grupos.
- [ ] De 3 a 5 conclusões relevantes estão apoiadas por evidências quantitativas ou visuais verificáveis.
- [ ] Limitações, possíveis vieses, interpretações alternativas e questões abertas estão explícitos; contagens não são apresentadas como taxas nem associações como causas.
- [ ] Notebook executa do início ao fim com instruções e relatório é claro e conciso.
