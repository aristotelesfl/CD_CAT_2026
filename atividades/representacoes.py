"""Representações da CAT para as atividades 02 e 03. Ajustar sempre no treino."""

from functools import partial

from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectPercentile, mutual_info_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DETALHADA = ["agente", "tipo", "cnae", "cbo"]
ENTRADAS = {
    "Completa": DETALHADA,
    "Tipo e agente": ["tipo", "agente"],
    "Tipo, agente e divisão": ["tipo", "agente", "cnae_divisao"],
    "Com família CBO": ["tipo", "agente", "cnae_divisao", "cbo_familia"],
    "Sem agente": ["tipo", "cnae_divisao"],
    "Informação mútua": DETALHADA,
    "PCA 95%": DETALHADA,
}


def representacao(nome):
    """Recebe as categorias preparadas e devolve um pipeline ainda sem ajuste."""
    denso = nome == "PCA 95%"
    codificar = ColumnTransformer(
        [("categorias", OneHotEncoder(handle_unknown="ignore", sparse_output=not denso),
          ENTRADAS[nome])],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    passos = [("codificar", codificar)]
    if nome == "Informação mútua":
        informacao_discreta = partial(mutual_info_classif, discrete_features=True, random_state=42)
        passos.append(("reduzir", SelectPercentile(informacao_discreta, percentile=50)))
    if denso:
        passos.append(("reduzir", PCA(n_components=0.95, svd_solver="full")))
    return Pipeline(passos)
