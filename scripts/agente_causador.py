"""Associa descrições de agente das CATs ao código do dicionário oficial."""

import re
import unicodedata
from pathlib import Path

import pandas as pd


REFERENCIA_AGENTES = (
    Path(__file__).resolve().parents[1]
    / "datasets"
    / "agente_causador_acidente_trabalho.csv"
)


def _normalizar_texto(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.casefold().split())


def codificar_agentes(
    descricoes: pd.Series,
    referencia: str | Path = REFERENCIA_AGENTES,
) -> pd.DataFrame:
    """Retorna o código como texto e a situação de cada descrição, no índice original."""
    dicionario = pd.read_csv(
        referencia,
        encoding="utf-8-sig",
        dtype="string",
        usecols=["codigo", "descricao"],
    ).dropna()
    codigos_referencia = dicionario["codigo"].str.strip()
    codigos_validos = set(codigos_referencia)
    descricoes_referencia = dicionario["descricao"].map(_normalizar_texto)
    sem_pontuacao_referencia = descricoes_referencia.str.replace(
        r"[^a-z0-9]+", " ", regex=True
    ).str.strip()

    textos = descricoes.astype("string").str.strip()
    mapa_codigo = {}
    mapa_situacao = {}

    for texto in textos.dropna().unique():
        chave = _normalizar_texto(texto)
        if chave in {"", "{n class}", "desconhecido"}:
            mapa_situacao[texto] = "ausente"
            continue

        # Mantém o código se a célula for executada sobre uma coluna já convertida.
        if texto in codigos_validos:
            mapa_codigo[texto] = texto
            mapa_situacao[texto] = "associado"
            continue

        # A pontuação pode distinguir prefixos truncados de agentes diferentes.
        candidatos = codigos_referencia[descricoes_referencia.str.startswith(chave)].unique()
        if len(candidatos) == 0:
            chave_sem_pontuacao = re.sub(r"[^a-z0-9]+", " ", chave).strip()
            if chave_sem_pontuacao:
                candidatos = codigos_referencia[
                    sem_pontuacao_referencia.str.startswith(chave_sem_pontuacao)
                ].unique()

        if len(candidatos) == 1:
            mapa_codigo[texto] = candidatos[0]
            mapa_situacao[texto] = "associado"
        else:
            mapa_situacao[texto] = "ambíguo" if len(candidatos) > 1 else "sem correspondência"

    return pd.DataFrame({
        "codigo": textos.map(mapa_codigo).astype("string"),
        "situacao": textos.map(mapa_situacao).fillna("ausente").astype("string"),
    })
