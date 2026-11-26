"""Configurações de número de vizinhos e votação do KNN."""

from itertools import product

from sklearn.neighbors import KNeighborsClassifier


def configuracoes():
    return [
        ("KNN", KNeighborsClassifier(n_neighbors=vizinhos, weights=voto))
        for vizinhos, voto in product((5, 15), ("uniform", "distance"))
    ]
