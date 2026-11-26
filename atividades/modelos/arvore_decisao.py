"""Configurações de profundidade e tamanho das folhas da árvore de decisão."""

from itertools import product

from sklearn.tree import DecisionTreeClassifier


def configuracoes(semente):
    return [
        (
            "Árvore",
            DecisionTreeClassifier(
                max_depth=profundidade,
                min_samples_leaf=minimo_por_folha,
                random_state=semente,
            ),
        )
        for profundidade, minimo_por_folha in product((10, None), (1, 5))
    ]
