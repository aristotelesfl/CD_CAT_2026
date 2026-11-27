"""Treinamento e grade de hiperparâmetros da árvore de decisão."""

from __future__ import annotations

from itertools import product
from typing import Any

from sklearn.tree import DecisionTreeClassifier


FAMILIA = "Árvore de decisão"


def configuracoes(random_state: int = 42) -> list[dict[str, Any]]:
    """Retorna a grade de hiperparâmetros avaliada para a árvore de decisão."""
    return [
        {
            "max_depth": profundidade,
            "min_samples_leaf": minimo_folha,
            "class_weight": peso,
            "random_state": random_state,
        }
        for profundidade, minimo_folha, peso in product(
            (4, 8, None),
            (1, 8),
            (None, "balanced"),
        )
    ]


def treinar_arvore_decisao(
    X_treino,
    y_treino,
    max_depth: int | None = 4,
    min_samples_leaf: int = 8,
    class_weight: str | dict | None = "balanced",
    criterion: str = "gini",
    random_state: int = 42,
) -> DecisionTreeClassifier:
    """Instancia, ajusta nos dados de treino e retorna a árvore de decisão."""
    modelo = DecisionTreeClassifier(
        criterion=criterion,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=random_state,
    )
    modelo.fit(X_treino, y_treino)
    return modelo
