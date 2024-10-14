import math
import time

import TasMinimum
from TasMinimum import *
from FileBinomial import *

import matplotlib.pyplot as plt
import os
import re
import textwrap
import timeit

cles_path = './cles_alea'

valeursCles = []


def FichierVersCles(filename):
    listeCles = []
    with open(os.path.join(cles_path, filename), 'r') as file:
        for line in file:
            cle = textwrap.wrap(line[2:], 8)
            key = [int(elt, 16) for elt in cle]
            key = Key(key)
            listeCles.append(key)

    return listeCles


AjoutsIteratifs = {}
falses = []
for filename in os.listdir(cles_path):
    if os.path.isfile(os.path.join(cles_path, filename)):
        nbCles = re.split(r'[_.]', filename)[-2]
        valeursCles.append(nbCles)

        listeCles = FichierVersCles(filename)

        taille = len(listeCles)
        liste1 = listeCles[:(taille // 2)]
        liste2 = listeCles[(taille // 2):]
        arbre1 = copy.copy(listeCles)
        file1 = ajoutIteratif(FB(), liste1)
        file = ajoutIteratif(FB(),liste2)

        debut = time.time()
        fileunion = unionFile(file1,file)
        fin = time.time()
        tempsExecutionAjoutsIteratifs = fin - debut
        print(str(tempsExecutionAjoutsIteratifs))
        if nbCles in AjoutsIteratifs:
            AjoutsIteratifs[nbCles].append(tempsExecutionAjoutsIteratifs)
        else:
            AjoutsIteratifs[nbCles] = [tempsExecutionAjoutsIteratifs]
    print(filename)


if __name__ == '__main__':
    for key, value in AjoutsIteratifs.items():
        AjoutsIteratifs[key] = sum(value) / len(value)

    valeursCles = sorted(list(set((list(map(int, valeursCles))))))
    valeursCles = list(map(str, valeursCles))
    maxTempsAjoutsIteratifs = math.ceil(max(AjoutsIteratifs.values()))

    max = maxTempsAjoutsIteratifs
    fig, axs = plt.subplots(1)  # Utilisez 1 au lieu de 2 pour avoir une seule sous-figure
    moyennesAjoutsIteratifs = []

    for elt in valeursCles:
        moyennesAjoutsIteratifs.append(AjoutsIteratifs[elt])

    axs.plot(valeursCles, moyennesAjoutsIteratifs, color='red')
    axs.axis([valeursCles[0], valeursCles[-1], 0, max + 0.5])

    plt.show()

