import copy
import math
import time

from TasArbreMin import *
from part1Thomas import Key

import matplotlib.pyplot as plt
import os
import re
import textwrap
import timeit

cles_path = './cles_alea'

valeursCles = []


def FichierVersCles(filename):
    """
    Créer une liste à partir des clés stockées dans un fichier

    :param filename: nom du fichier
    :type filename: str
    :return: la liste des clés
    :rtype: list[Key]
    """
    listeCles = []
    with open(os.path.join(cles_path, filename), 'r') as file:
        for line in file:
            cle = textwrap.wrap(line[2:], 8)
            key = [int(elt, 16) for elt in cle]
            key = Key(key)
            listeCles.append(key)

    return listeCles


AjoutsIteratifs = {}
Construction = {}
Union = {}

for filename in os.listdir(cles_path):
    if os.path.isfile(os.path.join(cles_path, filename)):
        nbCles = re.split(r'[_.]', filename)[-2]
        valeursCles.append(nbCles)

        arbre1 = ArbreTasMin()
        arbre2 = ArbreTasMin()

        listeCles = FichierVersCles(filename)
        listeClesCp = copy.deepcopy(listeCles)
        debut = time.time()
        arbre2.Construction(listeClesCp)
        fin = time.time()
        tempsExecutionConstruction = fin - debut
        debut2 = time.time()
        arbre1.AjoutsIteratifs(listeCles)
        fin2 = time.time()
        tempsExecutionAjoutsIteratifs = fin2 - debut2

        # On fait une copie de chaque moitié de la liste de clés
        tailleListes = len(listeCles) // 2
        listeClesCp2 = copy.deepcopy(listeCles[:tailleListes])
        listeClesCp3 = copy.deepcopy(listeCles[tailleListes:])
        arbre3 = ArbreTasMin()
        arbre4 = ArbreTasMin()

        # On utilise les copies pour créer 2 tas qui n'ont pas de clés communes
        arbre3.Construction(listeClesCp2)
        arbre4.Construction(listeClesCp3)
        print(str(verifieArbre(arbre3)))
        print(str(verifieArbre(arbre4)))
        debut3 = time.time()
        tmp = ArbreTasMin.Union(arbre3, arbre4)
        fin3 = time.time()
        tempsExecutionUnion = fin3 - debut3

        if nbCles in AjoutsIteratifs:
            AjoutsIteratifs[nbCles].append(tempsExecutionAjoutsIteratifs)
        else:
            AjoutsIteratifs[nbCles] = [tempsExecutionAjoutsIteratifs]

        if nbCles in Construction:
            Construction[nbCles].append(tempsExecutionConstruction)
        else:
            Construction[nbCles] = [tempsExecutionConstruction]

        if nbCles in Union:
            Union[nbCles].append(tempsExecutionUnion)
        else:
            Union[nbCles] = [tempsExecutionUnion]

    print(filename)

for key, value in AjoutsIteratifs.items():
    AjoutsIteratifs[key] = sum(value) / len(value)

for key, value in Construction.items():
    Construction[key] = sum(value) / len(value)

for key, value in Union.items():
    Union[key] = sum(value) / len(value)

valeursCles = sorted(list(set((list(map(int, valeursCles))))))
valeursCles = list(map(str, valeursCles))
maxTempsAjoutsIteratifs = math.ceil(max(AjoutsIteratifs.values()))
maxTempsConstruction = math.ceil(max(Construction.values()))
maxTempsUnion = math.ceil(max(Union.values()))
max = max(max(maxTempsAjoutsIteratifs, maxTempsConstruction), maxTempsUnion)
fig, axs = plt.subplots(2)
moyennesAjoutsIteratifs = []
moyennesConstruction = []
moyennesUnion = []
for elt in valeursCles:
    moyennesAjoutsIteratifs.append(AjoutsIteratifs[elt])
    moyennesConstruction.append(Construction[elt])
    moyennesUnion.append(Union[elt])

axs[0].plot(valeursCles, moyennesAjoutsIteratifs, color='red')
axs[0].plot(valeursCles, moyennesConstruction, color='blue')
axs[1].plot(valeursCles, moyennesUnion, color='orange')
axs[0].axis([valeursCles[0], valeursCles[-1], 0, max + 1])
axs[1].axis([valeursCles[0], valeursCles[-1], 0, max + 1])
plt.show()
