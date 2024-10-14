import copy

from part1Thomas import *


def ajoutTasListe(cle: Key, tas: list):
    """
    ajoutTasListe(cle: Key, tas: list[Key]) -> list[Key]

    Paramètres :
    cle (Key) : La clé à ajouter dans la liste.
    tas (list) : La liste qui représente le tas.
    Description :
    Cette fonction ajoute une clé à la liste et effectue la mise à jour pour maintenir la propriété de tas, on fait remonter la clé ajoutée si nécessaire en l'échangeant avec
    son parent.
    Retour :
    La liste mise à jour.
    """
    tas.append(cle)
    indice = len(tas) - 1
    while indice > 0 and cle.inf(tas[(indice - 1) // 2]):
        temp = tas[(indice - 1) // 2]
        tas[(indice - 1) // 2] = cle
        tas[indice] = temp
        indice = (indice - 1) // 2
    return tas


def verifieTas(tas: list, longueur):
    """
    verifieTas(tas: list[key]) -> bool:

    Paramètre :
    tas (list[Key]) : La liste qui représente le tas.
    Description :
    Vérifie si la liste représente un tas (arbre binaire avec la propriété de tas), on compare chaque père avec ses deux fils (si le tas est assez grand).
    Retour :
    True si la liste est un tas, False sinon.
    """
    for i in range(longueur):
        if (2 * i) + 1 < longueur:
            if not tas[i].inf(tas[(2 * i) + 1]) and not tas[i].eg(tas[2 * i + 1]):
                print(str(tas[i]) + "    <    " + str(tas[2 * i + 1]))
                return False
        if (2 * i) + 2 < longueur:
            if not tas[i].inf(tas[(2 * i) + 2]) and not tas[i].eg(tas[2 * i + 2]):
                print(str(tas[i]) + "    <    " + str(tas[2 * i + 2]))
                return False
    return True


def supprMinListe(tas: list):
    """
    supprMinListe(tas: list[Key]):

    Paramètre :
    tas (list[Key]) : La liste qui représente le tas.
    Description :
    Supprime le minimum de la liste et met à jour la liste pour maintenir la propriété de tas, on met le dernier à la racine et on le fait descendre petit à petit en échangeant
    avec le min(gauche,droite).
    Retour :
    Aucun.
    """
    indice = len(tas) - 1
    tas[0] = tas[indice]
    tas.pop(indice)
    indice = 0
    while (2 * indice) + 1 < len(tas) or (2 * indice) + 2 < len(tas):
        gauche = (2 * indice) + 1
        droite = (2 * indice) + 2
        if droite < len(tas) and tas[droite].inf(tas[gauche]):
            temp = tas[indice]
            tas[indice] = tas[droite]
            tas[droite] = temp
            indice = droite
        else:
            temp = tas[indice]
            tas[indice] = tas[gauche]
            tas[gauche] = temp
            indice = gauche


def ajoutsIteratifs(cles: list):
    """
    ajoutsIteratifs(cles: list[Key]) -> list[Key]:

    Paramètre :
    cles (list[Key]) : La liste des clés à ajouter dans le tas.
    Description :
    Ajoute itérativement les clés de la liste à un tas et renvoie le tas résultant.
    Retour :
    La liste représentant le tas résultant.
    """
    resultat = []
    for c in cles:
        ajoutTasListe(c, resultat)
    return resultat


def construction(tas: list):
    n = len(tas)
    # print(str(n) + " donc la moitié est : " + str(n // 2))
    for i in reversed(range(n // 2 + 1)):
        tasser(tas, i, n)


def tasser(tas: list, indice, longueur):
    """
    Paramètres :
    T (list[Key]) : La liste qui représente le tas.
    i (int) : L'indice à partir duquel effectuer la remise en tas.
    Description :
    Effectue l'opération de remise en tas à partir de l'indice donné dans la liste T en remontant l'élément.
    Retour :
    Aucun.
    """
    g = (2 * indice) + 1
    d = (2 * indice) + 2
    res = indice
    # print(tasToString(tas) + " indice :     " + str(res))
    if g < longueur and tas[g].inf(tas[res]):
        res = g
    if d < longueur and tas[d].inf(tas[res]):
        res = d
    if res != indice:
        tas[res], tas[indice] = tas[indice], tas[res]
        tasser(tas, res, longueur)





""" #premiere technique très naive
def union(tas: list, tas2: list):
    temp = tas
    temp2 = tas2
    res = []
    while not temp == [] and not temp2 == []:
        if temp2[0].inf(temp[0]):
            res.append(temp2[0])
            supprMinListe(temp2)
        else:
            res.append(temp[0])
            supprMinListe(temp)
    for i in range(len(temp)):  # On ajoute le reste si une des listes est plus longue que l'autre
        # Si elles étaient égales c'est pas grave puisque le test est O(1)
        res.append(temp[i])
    for i in range(len(temp2)):
        res.append(temp2[i])
    return res
"""




def union(tas: list, tas2: list):  # en moyenne c'est mieux avec ça, donc on le garde (voir graphiques)
    """
    union(tas: list[Key], tas2: list[Key]) -> list:

    Paramètres :
    tas (list[Key]) : La première liste qui représente un tas.
    tas2 (list[Key]) : La deuxième liste qui représente un tas.
    Description :
    On concatène les deux tas, puis on lance construction dessus.
    Hypothèse: concaténation se fait en O(1).
    Retour :
    La liste représentant le tas résultant.
    """
    res = tas + tas2
    construction(res)
    return res





def tasToString(list):
    """
    tasToString(list[Key]) -> str:

    Paramètre :
    list (list[Key]) : La liste qui représente le tas.
    Description :
    Convertit la liste en une chaîne de caractères représentant le tas.
    Retour :
    La représentation en chaîne de caractères du tas.
    """
    res = "["
    for k in list:
        res += str(k)
        res += ";"
    res += "]"
    return res


if __name__ == '__main__':
    liste1 = []
    liste2 = []
    ajoutTasListe(convertToKey(0), liste1)
    ajoutTasListe(convertToKey(6), liste1)
    ajoutTasListe(convertToKey(7), liste1)
    ajoutTasListe(convertToKey(10), liste1)
    ajoutTasListe(convertToKey(11), liste1)
    print(tasToString(liste1))
    ajoutTasListe(convertToKey(1), liste2)
    ajoutTasListe(convertToKey(2), liste2)
    ajoutTasListe(convertToKey(12), liste2)
    ajoutTasListe(convertToKey(8), liste2)
    liste3 = []
    liste3.append(convertToKey(8))
    liste3.append(convertToKey(4))
    liste3.append(convertToKey(3))
    liste3.append(convertToKey(1))
    liste3.append(convertToKey(0))

    u = union(liste1, liste2)
    print("après union")
    print(verifieTas(u, len(u)))
    print(tasToString(u))

    print("CONSTR")
    print('avant : ' + tasToString(liste3))
    construction(liste3)
    print(tasToString(liste3))
