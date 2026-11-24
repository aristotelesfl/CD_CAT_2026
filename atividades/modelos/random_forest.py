"""Configurações de profundidade e tamanho das folhas da Random Forest."""

from itertools import product

from sklearn.ensemble import RandomForestClassifier


def configuracoes(semente):
    return [
        (
            "Random Forest",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=profundidade,
                min_samples_leaf=minimo_por_folha,
                random_state=semente,
                n_jobs=1,
            ),
        )
        for profundidade, minimo_por_folha in product((15, None), (1, 5))
    ]
