"""Treinamento e grade de hiperparâmetros do classificador Random Forest."""

from __future__ import annotations

from itertools import product
from typing import Any

from sklearn.ensemble import RandomForestClassifier


FAMILIA = "Random Forest"


def configuracoes(random_state: int = 42) -> list[dict[str, Any]]:
    """Retorna a grade de hiperparâmetros avaliada para a Random Forest."""
    return [
        {
            "n_estimators": 200,
            "max_depth": profundidade,
            "min_samples_leaf": minimo_folha,
            "class_weight": peso,
            "random_state": random_state,
        }
        for profundidade, minimo_folha, peso in product(
            (6, 15, None),
            (1, 5),
            (None, "balanced"),
        )
    ]


def treinar_random_forest(
    X_treino,
    y_treino,
    n_estimators: int = 200,
    max_depth: int | None = 15,
    min_samples_leaf: int = 5,
    class_weight: str | dict | None = "balanced",
    random_state: int = 42,
    n_jobs: int = -1,
) -> RandomForestClassifier:
    """Instancia, ajusta nos dados de treino e retorna o classificador Random Forest."""
    modelo = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    modelo.fit(X_treino, y_treino)
    return modelo
