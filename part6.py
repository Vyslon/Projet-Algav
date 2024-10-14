from time import time
import random

from ABR import ABR, ajoutABR, contientABR
from TasMinimum import *
from FileBinomial import *
from MD5 import md5
from part1Thomas import Key, convertToKey, bytesToKey
from TasArbreMin import *
import matplotlib.pyplot as plt

import os
import re

shakespeare_path = './Shakespeare'


class ListeMots:
    """
    Classe permettant de stocker des mots, contient une liste ET une table de hachage, la liste permet de conserver
    l'ordre d'ajout des mots, la table de hachage permet de vérifier si on a déjà ajouté le mot en O(1)

    Attributes:
        listeOrdreApparence: liste des mots ajoutés (sans doublon) par ordre d'apparence
        tableHachageMots: table de hachage contenant tous les mots ajoutés (pour vérifier s'ils ont déjà été ajoutés)
    """
    def __init__(self):
        self.listeOrdreApparence = []
        self.tableHachageMots = {}

    def Ajout(self, element):
        """
        Ajoute un mot à la liste et à la tabla de hachage

        :param element: mot à ajouter
        :type element: str
        """
        if element not in self.tableHachageMots:
            self.listeOrdreApparence.append(element)
            self.tableHachageMots[element] = True

    def motsParOrdreApparence(self):
        """
        Getter
        Renvoie les mots par ordre d'apparence

        :return: liste des mots par ordre d'apparence
        :rtype: list[str]
        """
        return self.listeOrdreApparence


def FichierVersMots(fichier):
    """
    Renvoie la liste de tous les mots contenus dans un fichier (avec doublons)

    :param fichier: nom du fichier
    :type fichier: str
    :return: la liste des mots
    :rtype: list[str]
    """
    print("Traitement de : " + fichier)
    listeMots = []
    with open(os.path.join(shakespeare_path, fichier), 'r') as file:
        for line in file:
            for mot in line.split():
                listeMots.append(mot)
    return listeMots


listeMots = ListeMots()
listeCles = []

# On range tous les mots des oeuvres de shakespeare dans listeMots (il n'y a pas de doublons)
for filename in os.listdir(shakespeare_path):
    if os.path.isfile(os.path.join(shakespeare_path, filename)):
        listeMotsFichierActuel = FichierVersMots(filename)
        for mot in listeMotsFichierActuel:
            listeMots.Ajout(mot)

# On stocke dans notre structure arborescente de recherche le haché MD5 de chaque mot
arbre = ABR(None, None, None)
for elt in listeMots.listeOrdreApparence:
    maCle = bytesToKey(md5(elt).encode('utf-8'))
    listeCles.append(maCle)
    arbre = ajoutABR(arbre, maCle)

# On vérifie que l'ABR contient bien tous les mots
for elt in listeMots.listeOrdreApparence:
    maCle = bytesToKey(md5(elt).encode('utf-8'))
    if not contientABR(arbre, maCle):
        print("Problème")

# Tas : Ajout
tas1 = ArbreTasMin()
debut = time()
tas1.AjoutsIteratifs(listeCles)

fin = time()
timeTasAjout = fin - debut

# Tas : SupprMin
debut = time()
for elt in listeCles:
    tas1.SupprMin()

fin = time()
timeTasSupprMin = fin - debut

# Ici, on créer une copie de listeCles car on va modifier cette liste dans Construction
listeClesCp = copy.deepcopy(listeCles)
# Tas : Construction
debut = time()
tas2 = ArbreTasMin()
tas2.Construction(listeClesCp)

fin = time()
timeTasConstruction = fin - debut

# Ici, on scinde on fait une copie de chaque moitié de la liste des clés pour pouvoir faire l'union
# des tas construits à partir de ces moitiés
tailleListes = len(listeMots.listeOrdreApparence) // 2
listeClesCp2 = copy.deepcopy(listeCles[:tailleListes])
listeClesCp3 = copy.deepcopy(listeCles[tailleListes:])
random.shuffle(listeClesCp2)
random.shuffle(listeClesCp3)

tas3 = ArbreTasMin()
tas3.Construction(listeClesCp2)
tas4 = ArbreTasMin()
tas4.Construction(listeClesCp3)
# Tas : Union
debut = time()
tas5 = ArbreTasMin()
tas5 = ArbreTasMin.Union(tas3, tas4)

fin = time()
timeTasUnion = fin - debut
# FileBinomiale : Ajout
debut = time()
file1 = ajoutIteratif(FB(), listeCles)

fin = time()
timeFBAjout = fin - debut

# FileBinomiale : SupprMin
debut = time()
while file1.tournois:
    file1 = supprMin(file1)

print(str(file1.tournois))

fin = time()
timeFBSupprMin = fin - debut

# FileBinomiale : Construction
debut = time()
file2 = FB()
file2 = ajoutIteratif(file2, listeCles)

fin = time()
timeFBConstruction = fin - debut

# Ici, on coupe la liste des mots en 2 et on construit un tas pour chaque moitié puis, on fera l'union des 2

FB3 = ajoutIteratif(FB(), listeCles[:tailleListes+1])
FB4 = FB()
FB4 = ajoutIteratif(FB4, listeCles[tailleListes-1:])
# FB : Union
print("degre de FB3 : " + str(FB3.degre()))
print("degre de FB4 : " + str(FB4.degre()))
debut = time()
FB5 = unionFile(FB3, FB4)
fin = time()
print("degre de FB5 : " + str(FB5.degre()))

timeFBUnion = fin - debut

# Tas liste : Ajout
tas1Liste = ArbreTasMin()
debut = time()
tas1Liste = ajoutsIteratifs(listeCles)

fin = time()
timeTasAjoutListe = fin - debut

# Tas liste : SupprMin
debut = time()
for elt in listeCles:
    supprMinListe(tas1Liste)

fin = time()
timeTasSupprMinListe = fin - debut

tas2Liste = copy.copy(listeCles)
# Tas liste : Construction
debut = time()
construction(tas2Liste)

fin = time()
timeTasConstructionListe = fin - debut

# Ici, on scinde on fait une copie de chaque moitié de la liste des clés pour pouvoir faire l'union
# des tas construits à partir de ces moitiés
tailleListes = len(listeMots.listeOrdreApparence) // 2
listeClesCp2Liste = copy.deepcopy(listeCles[:tailleListes])
listeClesCp3Liste = copy.deepcopy(listeCles[tailleListes:])
random.shuffle(listeClesCp2Liste)
random.shuffle(listeClesCp3Liste)
# Tas liste : Union
debut = time()
tas3Liste = union(listeClesCp2Liste, listeClesCp3Liste)

fin = time()
timeTasUnionListe = fin - debut

largeurBarres = 0.2

# Enfin, on créer le graphique, en bleu on a les opérations sur tas binaire (implémentation avec arbre)
# et en vert, les opérations sur file binomiale
y1 = [timeTasAjout, timeTasSupprMin, timeTasConstruction, timeTasUnion]
x1 = range(len(y1))

y2 = [timeFBAjout, timeFBSupprMin, timeFBConstruction, timeFBUnion]
x2 = [i + largeurBarres for i in x1]

y3 = [timeTasAjoutListe, timeTasSupprMinListe, timeTasConstructionListe, timeTasUnionListe]
x3 = [i + largeurBarres * 2 for i in x1]

plt.bar(x1, y1, width=largeurBarres, color='blue', edgecolor='black', linewidth=2)
plt.bar(x2, y2, width=largeurBarres, color='green', edgecolor=['black' for i in y1], linewidth=2)
plt.bar(x3, y3, width=largeurBarres, color='red', edgecolor=['black' for i in y1], linewidth=2)

plt.xticks([r + largeurBarres / 2 for r in range(len(y1))], ['Ajout', 'SupprMin', 'Construction', 'Union'])

plt.show()
