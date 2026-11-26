"""Configurações de camadas ocultas e regularização da MLP."""

from itertools import product

from sklearn.neural_network import MLPClassifier


def configuracoes(semente):
    return [
        (
            "MLP",
            MLPClassifier(
                hidden_layer_sizes=camadas,
                alpha=alpha,
                solver="adam",
                max_iter=300,
                random_state=semente,
            ),
        )
        for camadas, alpha in product(((64,), (64, 32)), (0.0001, 0.01))
    ]
