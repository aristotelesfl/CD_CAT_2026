"""Confere as colunas da CAT e compara entradas para prever a parte atingida.

Da raiz do projeto: python atividades/analisar_colunas.py
Usa somente a biblioteca padrão e dados de desenvolvimento.
"""

import csv
from collections import Counter, defaultdict
from datetime import date
from functools import cache
from pathlib import Path

DADOS = Path(__file__).resolve().parents[1] / "datasets"
CAMPOS = (
    "Agente Causador Acidente", "Data Acidente", "CBO", "CBO", "CID-10", "CID-10",
    "CNAE2.0 Empregador", "CNAE2.0 Empregador", "Emitente CAT", "Espécie do benefício",
    "Filiação Segurado", "Indica Óbito Acidente", "Munic Empr", "Natureza da Lesão",
    "Origem de Cadastramento CAT", "Parte Corpo Atingida", "Sexo", "Tipo do Acidente",
    "UF Munic. Acidente", "UF Munic. Empregador", "Data Afastamento",
    "Data Despacho Benefício", "Data Acidente", "Data Nascimento", "Data Emissão CAT",
    "Tipo de Empregador", "CNPJ/CEI Empregador",
)
MARCADORES = {"", "{ñ class}", "00/00/0000"}
POR_CAMPO = {
    2: {"000000"}, 6: {"0000"}, 12: {"000000-ignorado"},
    16: {"indeterminado", "não informado"}, 18: {"zerado"}, 19: {"zerado"},
}
AGENTE, CBO, CNAE, FILIACAO = 0, 2, 6, 10
ALVO, SEXO, TIPO, TIPO_EMPREGADOR = 15, 16, 17, 25
FAMILIA, DIVISAO = len(CAMPOS), len(CAMPOS) + 1


@cache
def data(texto):
    try:
        dia, mes, ano = texto.strip().split("/")
        return date(int(ano), int(mes), int(dia))
    except ValueError:
        return None


def hierarquias():
    with (DADOS / "CBOs" / "CBO2002 - Familia.csv").open(encoding="latin-1", newline="") as f:
        familias = {r["CODIGO"].strip() for r in csv.DictReader(f, delimiter=";")}
    with (DADOS / "CBOs" / "CBO2002 - Ocupacao.csv").open(encoding="latin-1", newline="") as f:
        ocupacoes = [r["CODIGO"].strip() for r in csv.DictReader(f, delimiter=";")]
    familia_por_cbo = {c: c[:4] for c in ocupacoes if c[:4] in familias}
    divisoes = {}
    with (DADOS / "cnae20.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            chave = "".join(c for c in r["cod_classe"] if c.isdigit())
            divisao = r["cod_divisao"].strip().zfill(2)
            if len(chave) != 5 or chave[:4] in divisoes:
                raise ValueError(f"Classe CNAE inválida ou repetida: {chave}")
            divisoes[chave[:4]] = divisao
    return familia_por_cbo, divisoes


def carregar():
    familias, divisoes = hierarquias()
    distintas = set()
    for mes in range(1, 7):
        nome = f"D.SDA.PDA.005.CAT.2026{mes:02d}.csv"
        with (DADOS / "CAT_2026" / nome).open(encoding="latin-1", newline="") as arquivo:
            leitor = csv.reader(arquivo, delimiter=";")
            if tuple(" ".join(c.split()) for c in next(leitor)) != CAMPOS:
                raise ValueError(f"Cabeçalho inesperado em {nome}")
            for linha in leitor:
                if linha[18].strip().casefold() != "ceará":
                    continue
                primeira, segunda = data(linha[1]), data(linha[22])
                ocorrencia = primeira or segunda
                if primeira and segunda and primeira != segunda:
                    continue
                if ocorrencia and date(2026, 1, 1) <= ocorrencia < date(2026, 6, 1):
                    distintas.add(tuple(linha))
    registros = []
    for linha in distintas:
        campos = []
        for i, texto in enumerate(linha):
            valor = " ".join(texto.split()).casefold()
            if valor in MARCADORES or valor in POR_CAMPO.get(i, ()):
                valor = ""
            campos.append(valor)
        campos.extend([familias.get(campos[CBO], ""), divisoes.get(campos[CNAE], "")])
        registros.append((data(linha[1]) or data(linha[22]), data(linha[24]), tuple(campos)))
    return registros


def comparar(treino, avaliacao, grupos):
    # Testa primeiro a combinação mais específica e recua quando ela é inédita.
    totais = Counter(r[ALVO] for r in treino)
    ordem = sorted(totais, key=lambda classe: (-totais[classe], classe))
    tabelas = []
    for grupo in grupos:
        contagens = defaultdict(Counter)
        for r in treino:
            contagens[tuple(r[i] for i in grupo)][r[ALVO]] += 1
        classe_por_grupo = {
            chave: max(ordem, key=frequencias.__getitem__)
            for chave, frequencias in contagens.items()
        }
        tabelas.append((grupo, classe_por_grupo))

    reais = Counter()
    previstas = Counter()
    acertos = Counter()
    for r in avaliacao:
        prevista = ordem[0]
        for grupo, tabela in tabelas:
            chave = tuple(r[i] for i in grupo)
            if chave in tabela:
                prevista = tabela[chave]
                break
        reais[r[ALVO]] += 1
        previstas[prevista] += 1
        if prevista == r[ALVO]:
            acertos[prevista] += 1
    f1_macro = sum(2 * acertos[c] / (reais[c] + previstas[c]) for c in reais) / len(reais)
    return sum(acertos.values()) / len(avaliacao), f1_macro


def main():
    registros = carregar()
    print(f"{len(registros)} registros distintos de janeiro a maio")
    for i, nome in enumerate(CAMPOS):
        freq = Counter(r[i] for _, _, r in registros)
        faltas = freq.pop("", 0)
        print(f"{i+1:2}  {nome:30} {len(freq):5} valores informados; {faltas:5} ausências")
    classes = Counter(r[ALVO] for _, _, r in registros if r[ALVO])
    print("Classes mais frequentes:", classes.most_common(5))
    print("Classes com menos de dez registros:", sum(n < 10 for n in classes.values()))
    for i, nome in ((FAMILIA, "Família CBO"), (DIVISAO, "Divisão CNAE")):
        freq = Counter(r[i] for _, _, r in registros)
        faltas = freq.pop("", 0)
        print(f"{nome}: {len(freq)} categorias informadas; {faltas} sem grupo confirmado")

    campos_individuais = (AGENTE, CBO, CNAE, TIPO, SEXO, FILIACAO, TIPO_EMPREGADOR)
    tipo_agente = [(AGENTE, TIPO), (AGENTE,), (TIPO,)]
    tipo_agente_cnae = [(AGENTE, TIPO, CNAE), *tipo_agente]
    tipo_agente_divisao = [(AGENTE, TIPO, DIVISAO), *tipo_agente]
    configuracoes = {
        "Classe mais frequente": [],
        **{CAMPOS[i]: [(i,)] for i in campos_individuais},
        "Tipo e agente": tipo_agente,
        "Tipo, agente e CBO": [(AGENTE, TIPO, CBO), *tipo_agente],
        "Tipo, agente e CNAE": tipo_agente_cnae,
        "Tipo, agente, CNAE e CBO": [(AGENTE, TIPO, CNAE, CBO), *tipo_agente_cnae],
        "Tipo e divisão": [(TIPO, DIVISAO), (TIPO,), (DIVISAO,)],
        "Tipo, agente e divisão": tipo_agente_divisao,
        "Tipo, agente e hierarquias": [(AGENTE, TIPO, DIVISAO, FAMILIA), *tipo_agente_divisao],
        "CBO e CNAE": [(CBO, CNAE), (CBO,), (CNAE,)],
        "Tipo, CNAE e CBO": [(TIPO, CNAE, CBO), (TIPO, CNAE), (TIPO,), (CNAE,)],
    }
    resultados = defaultdict(list)
    for mes in (3, 4, 5):
        corte = date(2026, mes, 1)
        treino = [r for acidente, emissao, r in registros
                  if emissao and acidente <= emissao < corte and r[ALVO]]
        avaliacao = [r for acidente, _, r in registros if acidente.month == mes and r[ALVO]]
        print(f"Mês {mes}: {len(treino)} no treino e {len(avaliacao)} na validação")
        for nome, grupos in configuracoes.items():
            resultados[nome].append(comparar(treino, avaliacao, grupos))
    print("Entrada | acurácia média | F1-macro médio | F1-macro em março, abril e maio (%)")
    for nome, dobras in resultados.items():
        acuracias, escores = zip(*dobras)
        print(f"{nome:24} {100*sum(acuracias)/3:5.2f}  {100*sum(escores)/3:5.2f}  "
              + "  ".join(f"{100*x:.2f}" for x in escores))


if __name__ == "__main__":
    main()
