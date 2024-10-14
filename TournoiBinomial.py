from part1Thomas import *
import copy


class Tournoi:

    def __init__(self, key: Key = None, enfants=None, degre=0):
        """
            Description : Initialise un objet Tournoi.
            Paramètres :
            key : La clé associée au tournoi (par défaut, None).
            enfants : La liste des enfants du tournoi (par défaut, None).
            degre : Le degré du tournoi (par défaut, 0).
            """
        self.key = key
        self.enfants = enfants or []
        self.degre = degre



    def estVide(self):
        return self.key is None


def verifTournoi(tournoi : Tournoi):
    """
       Description : Vérifie si le tournoi et ses enfants forment un tournoi valide.
       Retour : True si le tournoi est valide, sinon False.
       Recursion infini,probleme avec les cles ?
       """
    res= True
    if tournoi.degre == 0:
        return True
    else:
        for child in tournoi.enfants:
            if child.key.inf(tournoi.key):
                return False
        for child in tournoi.enfants:
            res=  res and  verifTournoi(child)
        return res


def unionTournois(t1, t2):
    """
    Fonction unionTournois(t1, t2) :
    Description : Fusionne deux tournois en créant un nouveau tournoi avec le tournoi de clé minimale au sommet.
    Paramètres :
    t1 : Premier tournoi à fusionner.
    t2 : Deuxième tournoi à fusionner.
    Retour : Un nouveau tournoi résultant de la fusion de t1 et t2.
    """

    # if t1.degre != t2.degre:
    #       raise ValueError("pas le meme degre probleme")
    #      ce cas est enleve pour un soucis de compplexite, on n'est jamais dans ce cas là
    if t1.key.inf(t2.key):
        res = Tournoi(t1.key, t1.enfants, t1.degre + 1)
        res.enfants.insert(0, t2)
        return res
    else:
        res = Tournoi(t2.key, t2.enfants, t2.degre + 1)
        res.enfants.insert(0, t1)
        return res


if __name__ == '__main__':
    cle1 = convertToKey(5)
    t1 = Tournoi(key=cle1)
    t2 = Tournoi(convertToKey(4))
    t1t2 = unionTournois(t1, t2)
    t3 = Tournoi(convertToKey(2))
    t4 = Tournoi(convertToKey(3))
    t3t4 = unionTournois(t3, t4)
    t3t4 = unionTournois(t3t4, t3t4)
