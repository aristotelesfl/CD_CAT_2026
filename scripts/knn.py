"""Treinamento e grade de hiperparâmetros do classificador KNN."""

from __future__ import annotations

from itertools import product
from typing import Any

from sklearn.neighbors import KNeighborsClassifier


FAMILIA = "KNN"


def configuracoes() -> list[dict[str, Any]]:
    """Retorna a grade de hiperparâmetros avaliada para o KNN."""
    return [
        {
            "n_neighbors": vizinhos,
            "weights": voto,
            "metric": "euclidean",
        }
        for vizinhos, voto in product((3, 5, 11, 21), ("uniform", "distance"))
    ]


def treinar_knn(
    X_treino,
    y_treino,
    n_neighbors: int = 11,
    weights: str = "distance",
    metric: str = "euclidean",
) -> KNeighborsClassifier:
    """Instancia, ajusta nos dados de treino e retorna o classificador KNN."""
    modelo = KNeighborsClassifier(
        n_neighbors=n_neighbors,
        weights=weights,
        metric=metric,
    )
    modelo.fit(X_treino, y_treino)
    return modelo
