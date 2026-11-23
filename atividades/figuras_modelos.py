"""Gráficos da avaliação da atividade 03."""

import matplotlib.pyplot as plt
import numpy as np


def desempenho(mensais, finalistas):
    fig, eixo = plt.subplots(figsize=(8, 4.2), layout="constrained")
    for linha in finalistas.itertuples():
        selecao = mensais.loc[(mensais.variante == linha.variante)
                              & (mensais.representacao == linha.representacao)].sort_values("mes")
        eixo.plot(selecao.mes, selecao.f1_macro * 100, marker="o", label=linha.familia)
    eixo.set(xticks=[3, 4, 5], xticklabels=["Março", "Abril", "Maio"],
             ylabel="F1 macro (%)", title="Desempenho mensal das configurações selecionadas")
    eixo.legend(ncols=2)
    eixo.grid(axis="y", alpha=0.25)
    return fig


def confusoes(erros):
    topo = erros.head(10).iloc[::-1]
    fig, eixo = plt.subplots(figsize=(10, 5), layout="constrained")
    eixo.barh(np.arange(len(topo)), topo.contagem, color="#32658a")
    eixo.set(yticks=np.arange(len(topo)),
             yticklabels=[f"{real} → {prevista}" for real, prevista in
                          topo[["registrada", "prevista"]].itertuples(index=False)],
             xlabel="Registros de CAT", title="Junho · dez confusões mais frequentes")
    return fig


def painel_roc(curvas, aucs):
    classes = aucs.loc[aucs.auc.notna()].sort_values("classe")
    ncol = 5
    fig, eixos = plt.subplots(int(np.ceil(len(classes) / ncol)), ncol, squeeze=False,
                              figsize=(15, 2.0 * int(np.ceil(len(classes) / ncol))),
                              layout="constrained", sharex=True, sharey=True)
    for eixo, linha in zip(eixos.flat, classes.itertuples()):
        curva = curvas.loc[curvas.classe.eq(linha.classe)]
        eixo.plot([0, 1], [0, 1], "--", color=".75", linewidth=0.8)
        eixo.plot(curva.fpr, curva.tpr, color="#176b69", linewidth=1.3)
        eixo.set_title(f"{linha.classe}\nAUC {linha.auc:.2f} · n={linha.positivos}", fontsize=8)
    for eixo in list(eixos.flat)[len(classes):]:
        eixo.set_visible(False)
    fig.suptitle("Junho · curva ROC de cada classe contra as demais")
    fig.supxlabel("Taxa de falsos positivos")
    fig.supylabel("Taxa de verdadeiros positivos")
    return fig
