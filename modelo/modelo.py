import pandas as pd
import Levenshtein
import numpy as np


def distPalabras(s1, s2):
    if s1 in s2 or s2 in s1:
        return 0
    else:
        return Levenshtein.distance(s1, s2)


def distVectores(v1, v2):
    semi = 0
    for i in v1:
        for j in v2:
            semi = semi + distPalabras(i, j)

    semi = semi / (int(len(v1) * len(v2)))
    return semi


def getCluster(datosX, column, tag):
    arr = []
    for i in datosX:
        if i[column] == tag:
            arr.append(i)
    return np.array(arr)


def getDataById(datosX, column, ids):
    arr = []
    for id in ids:
        for i in datosX:
            if i[column] == id:
                arr.append(i)
    return np.array(arr)


class KNN:

    def __init__(self, k_neigh=5, orden_metrica=2) -> None:
        self.orden_metrica = orden_metrica
        self.k_neigh = k_neigh
        self.n_clases = None
        self.clases = None

    def entrenar(self, X_tr, y_tr, X_id):
        self.X_tr = X_tr
        self.Y_tr = y_tr
        self.X_id = X_id
        self.n_clases = len(np.unique(y_tr))
        self.clases = np.unique(y_tr)

    def predecir(self, X):
        distancias = []
        Recom = []
        for j in range(len(self.X_tr)):
            distancias.append([distVectores(X, self.X_tr[j]), self.Y_tr[j], self.X_id[j]])
        kneighb = sorted(distancias)[:self.k_neigh]
        count = np.zeros(self.n_clases)
        for neigh in kneighb:
            Recom.append(neigh[2])
            for z in range(self.n_clases):
                if neigh[1] == self.clases[z]:
                    count[z] += 1
        Y_tag = int(self.clases[np.array(count).argmax()])

        return Y_tag, Recom


def llamaModelo(vector):
    file = 'modelo\DatasetInvest'
    datos = np.array(pd.read_csv(file + ".csv", header=None))
    # Columnas con características
    datos = datos[:, 0:11]
    # Características para clasificación
    X = datos[:, 4:7]
    # Etiquetas
    Y = datos[:, 10]
    # Ids de los usuarios
    X_id = np.array(datos[:, 0])
    knn = KNN()
    knn.entrenar(X, Y, X_id)
    Y_res, rec = knn.predecir(vector)

    return getDataById(datos, 0, rec)
