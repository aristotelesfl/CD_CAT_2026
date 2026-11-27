"""Treinamento e grade de hiperparâmetros da rede neural MLP."""

from __future__ import annotations

from itertools import product
from typing import Any

from sklearn.neural_network import MLPClassifier


FAMILIA = "MLP"


def configuracoes(random_state: int = 42) -> list[dict[str, Any]]:
    """Retorna a grade de hiperparâmetros avaliada para a MLP."""
    return [
        {
            "hidden_layer_sizes": camadas,
            "alpha": alpha,
            "max_iter": 300,
            "random_state": random_state,
        }
        for camadas, alpha in product(((32,), (64,), (64, 32)), (0.0001, 0.01))
    ]


def treinar_mlp(
    X_treino,
    y_treino,
    hidden_layer_sizes: tuple[int, ...] = (64,),
    alpha: float = 0.0001,
    activation: str = "relu",
    solver: str = "adam",
    max_iter: int = 300,
    random_state: int = 42,
) -> MLPClassifier:
    """Instancia, ajusta nos dados de treino e retorna o classificador MLP."""
    modelo = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes,
        alpha=alpha,
        activation=activation,
        solver=solver,
        max_iter=max_iter,
        random_state=random_state,
    )
    modelo.fit(X_treino, y_treino)
    return modelo
