"""Treinamento e avaliação temporal da atividade 03."""

import json
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed, parallel_config
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from atividades.modelos import arvore_decisao, knn, mlp, random_forest
from atividades.representacoes import ENTRADAS, representacao


ALVO = "parte_atingida_classe"
ID = "id_registro"
MESES = (3, 4, 5)
SEMENTE = 42
REFERENCIA = "Classe mais frequente"


def grade():
    """Reúne as configurações na ordem usada para numerar as variantes."""
    return [
        *knn.configuracoes(),
        *arvore_decisao.configuracoes(SEMENTE),
        *random_forest.configuracoes(SEMENTE),
        *mlp.configuracoes(SEMENTE),
    ]


def ler_base(pasta, nome):
    base = pd.read_parquet(pasta / f"{nome}.parquet").set_index(ID, verify_integrity=True)
    campos = set().union(*ENTRADAS.values())
    assert set(base) == campos | {ALVO}
    assert base[list(campos)].notna().all().all()
    return base


def conferir_dobra(base, avaliacao, datas, particoes, mes):
    corte = pd.Timestamp(2026, mes, 1)
    dobra = particoes.loc[particoes.mes.eq(mes)]
    papel = "teste" if mes == 6 else "validacao"
    assert not dobra[ID].duplicated().any() and set(dobra.papel) == {"treino", papel}
    treino = base.loc[dobra.loc[dobra.papel.eq("treino"), ID]]
    valida = avaliacao.loc[dobra.loc[dobra.papel.eq(papel), ID]]
    anteriores = datas.loc[base.index]
    elegiveis = (anteriores.ocorrencia.lt(corte)
                 & anteriores.emissao.ge(anteriores.ocorrencia)
                 & anteriores.emissao.lt(corte) & base[ALVO].notna())
    datas_avaliacao = datas.loc[avaliacao.index, "ocorrencia"]
    no_mes = datas_avaliacao.between(corte, corte + pd.offsets.MonthEnd(0))
    assert set(treino.index) == set(base.index[elegiveis])
    assert set(valida.index) == set(avaliacao.index[no_mes & avaliacao[ALVO].notna()])
    assert treino.index.intersection(valida.index).empty
    return treino, valida


def ajustar(modelo, x, y):
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always", ConvergenceWarning)
        modelo.fit(x, y)
    convergencia = []
    for aviso in avisos:
        if issubclass(aviso.category, ConvergenceWarning):
            convergencia.append(str(aviso.message))
        else:
            warnings.warn(aviso.message, aviso.category, stacklevel=2)
    return " | ".join(convergencia)


def medidas(y, classes, prob):
    assert prob.shape == (len(y), len(classes)) and np.isfinite(prob).all()
    np.testing.assert_allclose(prob.sum(axis=1), 1, atol=1e-6)
    prevista = classes[prob.argmax(axis=1)]
    rotulos = np.union1d(y, classes)
    matriz = confusion_matrix(y, prevista, labels=rotulos)
    suporte, previsoes = matriz.sum(axis=1), matriz.sum(axis=0)
    vp = matriz.diagonal()
    detalhe = pd.DataFrame({
        "classe": rotulos, "suporte": suporte, "previsoes": previsoes,
        "vp": vp, "fp": previsoes - vp, "fn": suporte - vp,
        "vn": len(y) - suporte - previsoes + vp,
        "precisao": vp / np.maximum(previsoes, 1),
        "recall": vp / np.maximum(suporte, 1),
        "f1": 2 * vp / np.maximum(suporte + previsoes, 1),
        "precisao_indefinida": previsoes == 0,
        "inédita": ~np.isin(rotulos, classes),
    })
    presentes = detalhe.loc[detalhe.suporte.gt(0)]
    resumo = {
        "n": len(y), "classes_presentes": len(presentes), "acuracia": vp.sum() / len(y),
        "precisao_macro": presentes.precisao.mean(), "recall_macro": presentes.recall.mean(),
        "f1_macro": presentes.f1.mean(), "sem_previsao": presentes.precisao_indefinida.sum(),
        "registros_inéditos": presentes.loc[presentes["inédita"], "suporte"].sum(),
    }
    return resumo, detalhe, pd.DataFrame(matriz, index=rotulos, columns=rotulos)


def rodada(mes, nome, treino, valida):
    if nome == REFERENCIA:
        x, xv = np.zeros((len(treino), 1)), np.zeros((len(valida), 1))
        modelos = [(-1, (REFERENCIA, DummyClassifier(strategy="prior")))]
    else:
        prep = representacao(nome)
        x = prep.fit_transform(treino[ENTRADAS[nome]], treino[ALVO])
        xv = prep.transform(valida[ENTRADAS[nome]])
        modelos = enumerate(grade())
    resultados = []
    for numero, (familia, modelo) in modelos:
        aviso = ajustar(modelo, x, treino[ALVO])
        prob = modelo.predict_proba(xv)
        resumo, detalhe, _ = medidas(valida[ALVO], modelo.classes_, prob)
        chave = dict(mes=mes, representacao=nome, familia=familia, variante=numero)
        linha = dict(**chave, **resumo, campos=len(ENTRADAS.get(nome, [])),
                     parametros=json.dumps(modelo.get_params(), sort_keys=True),
                     iteracoes=getattr(modelo, "n_iter_", None), aviso=aviso)
        resultados.append((linha, detalhe.assign(**chave), modelo.classes_, prob))
    return resultados


def validar(dobras, trabalhadores=3):
    nomes = ["PCA 95%", *[n for n in ENTRADAS if n != "PCA 95%"], REFERENCIA]
    with parallel_config(backend="loky", inner_max_num_threads=1):
        blocos = Parallel(n_jobs=trabalhadores)(
            delayed(rodada)(mes, nome, *dobras[mes]) for nome in nomes for mes in MESES)
    linhas, detalhes, escores = [], [], {}
    for bloco in blocos:
        for linha, detalhe, classes, prob in bloco:
            linhas.append(linha)
            detalhes.append(detalhe)
            escores[linha["mes"], linha["representacao"], linha["variante"]] = classes, prob
    return pd.DataFrame(linhas), pd.concat(detalhes, ignore_index=True), escores


def classificar(medidas_mensais):
    return (medidas_mensais.groupby(["familia", "representacao", "variante"], as_index=False)
            .agg(campos=("campos", "first"), f1_medio=("f1_macro", "mean"),
                 desvio_f1=("f1_macro", "std"), acuracia_media=("acuracia", "mean"),
                 precisao_media=("precisao_macro", "mean"), recall_medio=("recall_macro", "mean"))
            .sort_values("f1_medio", ascending=False, ignore_index=True))


def escolher(tabela):
    elegiveis = tabela.loc[tabela.f1_medio.ge(tabela.f1_medio.max() - 0.005)]
    return elegiveis.sort_values(
        ["campos", "desvio_f1", "f1_medio", "variante", "representacao"],
        ascending=[True, True, False, True, True]).iloc[0]


def ajustar_final(escolha, treino):
    modelo = clone(grade()[int(escolha.variante)][1])
    nome = escolha.representacao
    pipeline = Pipeline([("preparacao", representacao(nome)), ("classificador", modelo)])
    with threadpool_limits(limits=1):
        aviso = ajustar(pipeline, treino[ENTRADAS[nome]], treino[ALVO])
    return pipeline, aviso


def diagnosticos(y, classes, prob):
    resumo, detalhes, matriz = medidas(y, classes, prob)
    indices = {classe: i for i, classe in enumerate(classes)}
    curvas = []
    aucs = []
    for classe, suporte in detalhes[["classe", "suporte"]].itertuples(index=False):
        disponivel = classe in indices
        auc = np.nan
        if disponivel and 0 < suporte < len(y):
            resposta = y.eq(classe)
            pontos = prob[:, indices[classe]]
            auc = roc_auc_score(resposta, pontos)
            fp, vp, limiar = roc_curve(resposta, pontos)
            curvas.append(pd.DataFrame(dict(classe=classe, fpr=fp, tpr=vp, limiar=limiar)))
        aucs.append(dict(classe=classe, positivos=suporte, negativos=len(y) - suporte,
                         pontuacao_disponivel=disponivel, auc=auc))
    aucs = pd.DataFrame(aucs)
    resumo.update(auc_macro=aucs.auc.mean(), classes_com_auc=aucs.auc.count())
    return resumo, detalhes, matriz, aucs, pd.concat(curvas, ignore_index=True)
