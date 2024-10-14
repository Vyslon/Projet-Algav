from part1Thomas import *


class ABR:
    def __init__(self, cle:Key, gauche= None, droite=None ):
        self.cle = cle
        self.gauche = gauche or None
        self.droite = droite or None

    def SAG(self):
        return self.gauche

    def SAD(self):
        return self.droite


def contientABR(arbre: ABR, cle:Key):
    """

    :param arbre: ABR
    :param cle: Key
    :return: true si l'arbre contient la clé, false sinon
    """
    if arbre is None:
        return False
    if arbre.cle.inf(cle): # clé du noeud < clé en param@
        return contientABR(arbre.SAD(), cle)
    if cle.inf(arbre.cle):
        return contientABR(arbre.SAG(), cle)
    else:
        return True  # Inutile en soit mais ici on laisse pour le test


def ajoutABR(arbre: ABR, cle: Key):
    """

    :param arbre:  ABR
    :param cle: Key
    :return: l'arbre après ajout de la clé au bon endroit, si la clé est déjà présente, l'arbre est inchangé
    """
    if arbre is None or arbre.cle is None:
        return ABR(cle, None, None)
    if arbre.cle.inf(cle):
        return ABR(arbre.cle, arbre.SAG(), ajoutABR(arbre.SAD(), cle))
    if cle.inf(arbre.cle):
        return ABR(arbre.cle, ajoutABR(arbre.SAG(), cle), arbre.SAD())
    else:
        return arbre  # Dans le cas où l'arbre contient déjà la clé


if __name__ == '__main__':
    arbre = ABR(convertToKey(545), ABR(convertToKey(450), None, None), ABR(convertToKey(900), None, None))
    arbre = ajoutABR(arbre, convertToKey(101))
    print(contientABR(arbre, convertToKey(101)))


