import math
from part1Thomas import Key
from AbstractTasMin import TasMin
from collections import deque


class Node:
    def __init__(self, key, ancestor=None):
        self.key = key
        self.left = None
        self.right = None
        self.ancestor = ancestor


class ArbreTasMin(TasMin):
    """
    Classe représentant un tas min

    Attributes:
        root: Noeud à la racine du tas (contenant la clé min)
        taille: Nombre de noeuds dans le tas
    """
    def __init__(self, noeud=None):
        self.root = noeud  # root est un Node
        self.taille = 0 if noeud is None else 1

    def SupprMin(self):
        """
        Supprime la clé minimum du tas
        """
        self.root.key = None
        if self.root.left is None:
            self.taille -= 1
            pass
        elif self.root.right is None:
            # Ici, il n'y a pas de fils droit mais il y a un fils gauche, on remonte donc le fils gauche
            self.taille -= 1
            self.root.key = self.root.left.root.key
            self.root.left = None
        else:
            # On récupère le dernier noeud ajouté au tas
            dernierNoeud = self.DernierNoeud()
            self.taille -= 1
            self.root.key = dernierNoeud.key

            if dernierNoeud.ancestor.right is None:
                # dernierNoeud est le fils gauche de son père, son père n'a donc plus de fils gauche
                dernierNoeud.ancestor.left = None
            else:
                # dernierNoeud est le fils droit de son père, son père n'a donc plus de fils droit
                dernierNoeud.ancestor.right = None

            # On descend le noeud qu'on vient de remonter à la racine
            self.DescendreNoeud(self.root)

    def DernierNoeud(self):
        """
        Renvoie le dernier noeud ajouté au tas binaire et réduit de 1 la taille des arbres parcourus

        :return: Le dernier noeud ajouté au tas binaire
        :rtype: Node
        """
        if self.taille > 0:
            hauteur = int(math.log2(self.taille))
        else:
            hauteur = 0

        if self.taille == 0:
            return None
        elif hauteur == 1 and self.root.right is not None:
            # Ici, on est dans un tas de taille 3, on renvoie directement le fils droit qui est logiquement le dernier ajouté
            return self.root.right.root
        else:
            if self.root.left is None:
                return self.root
            elif self.root.right is None:
                return self.root.left.root
            elif self.root.left.taille == self.root.right.taille:
                # Le tas en fils gauche et le tas en fils droit sont de même taille, logiquement le dernier noeud ajouté est à droite
                self.root.right.taille -= 1
                return self.root.right.DernierNoeud()
            elif self.root.left.taille == (pow(2, hauteur) - 1):
                # Ici le tas en fils gauche est plein, ci-dessous, on va vérifié que le tas en fils droit a une hauteur
                # Inférieur (dans ce cas ou ira à gauche) ou égale (on ira à droite)
                if (int(math.log2(self.root.left.taille)) > int(math.log2(self.root.right.taille))):
                    self.root.left.taille -= 1
                    return self.root.left.DernierNoeud()
                else:
                    self.root.right.taille -= 1
                    return self.root.right.DernierNoeud()
            else:
                self.root.left.taille -= 1
                return self.root.left.DernierNoeud()

    def Ajout(self, elt):
        """
        Ajoute le noeud en fin de tas avant de le faire remonter

        :param elt: Le noeud à ajouter
        :type elt: Node
        """
        nouveauNoeud = self.AjoutEnFin(elt)
        self.RemonterNoeud(nouveauNoeud)

    def DescendreNoeud(self, elt):
        """
        Descend le noeud elt s'il n'est pas à sa place dans le tas

        :param elt: Le noeud à descendre dans le tas
        :type elt: Node
        """
        if elt.right is None:
            if elt.left is None:
                return
            else:
                if (elt.left.root.key.inf(elt.key)):
                    elt.key, elt.left.root.key = elt.left.root.key, elt.key
        else:
            if (elt.left.root.key.inf(elt.right.root.key)) and (elt.left.root.key.inf(elt.key)) :
                elt.key, elt.left.root.key = elt.left.root.key, elt.key
                self.DescendreNoeud(elt.left.root)
            elif (elt.right.root.key.inf(elt.left.root.key)) and (elt.right.root.key.inf(elt.key)):
                elt.key, elt.right.root.key = elt.right.root.key, elt.key
                self.DescendreNoeud(elt.right.root)

    def RemonterNoeud(self, elt):
        """
        Remonte le noeud elt s'il n'est pas à sa place dans le tas

        :param elt: Le noeud à remonter dans le tas
        :type elt: Node
        """
        if elt.ancestor is None:
            return

        if (elt.key.inf(elt.ancestor.key)):
            elt.key, elt.ancestor.key = elt.ancestor.key, elt.key
            self.RemonterNoeud(elt.ancestor)

    def AjoutEnFin(self, elt):
        """
        Ajoute la clé elt à la fin du tas

        :param elt: La clé à ajouter dans le tas
        :type elt: Key
        :return: Le noeud ajouté dans le tas
        :rtype: Node
        """
        if self.taille > 0:
            hauteur = int(math.log2(self.taille))
        else:
            hauteur = 0

        if self.taille == 0:
            self.root = Node(elt)
            self.taille += 1
            return self.root
        else:
            self.taille += 1
            if self.root.left is None:
                self.root.left = ArbreTasMin(Node(elt, self.root))
                return self.root.left.root
            elif self.root.right is None:
                self.root.right = ArbreTasMin(Node(elt, self.root))
                return self.root.right.root
            elif self.root.left.taille == self.root.right.taille:
                return self.root.left.AjoutEnFin(elt)
            elif self.root.left.taille == (pow(2, hauteur) - 1):
                return self.root.right.AjoutEnFin(elt)
            else:
                return self.root.left.AjoutEnFin(elt)

    def AjoutsIteratifs(self, liste):
        """
        Remplit le tas à partir d'une liste de clés par appels consécutifs à Ajout

        :param liste: Liste de clés
        :type liste: list[Key]
        """
        for elt in liste:
            self.Ajout(elt)

    def Construction(self, liste):
        """
        Construit le tas à partir d'une liste de clés

        :param liste: Liste de clés
        :type liste: list[Key]
        """
        tasNaif = self.ConstructionNaive(liste)
        self.taille = tasNaif.taille
        self.root = tasNaif.root
        hauteur = int(math.log2(len(liste)))
        nbNoeudsProfMax = len(liste) - (2 ** hauteur - 1)
        # taille - nb noeuds de prof h - 1
        #
        for i in range(len(liste[:-nbNoeudsProfMax]) - 1, -1, -1):
            self.DescendreNoeud(liste[i].root)

    def RemettreEnTas(self, liste, id):
        idG = 2 * id
        idD = 2 * id + 1
        tmp = id
        if idG < len(liste) and liste[idG].key.inf(liste[tmp].key):
            tmp = idG
        if idD < len(liste) and liste[idD].key.inf(liste[tmp].key):
            tmp = idD
        if tmp != id:
            liste[id].key, liste[tmp].key = liste[tmp].key, liste[id].key
            self.RemettreEnTas(liste, tmp)

    @staticmethod
    def ArbresVersListe(arbre1, arbre2):
        """
        Méthode proxy qui appelle VersListe

        :param arbre1: 1er arbre à transformer en liste
        :type arbre1: ArbreTasMin
        :param arbre2: 2ème arbre à transformer en liste
        :type arbre2: ArbreTasMin
        :return: Liste contenant toutes les clés des 2 arbres donnés en paramètre
        :rtype: list[Key]
        """
        return ArbreTasMin.VersListe(arbre1, arbre2, [])

    @staticmethod
    def VersListe(noeud1, noeud2, liste=None):
        """
        Parcours 2 arbres simultanément (plus efficace) pour récupèrer toutes les valeurs de clés et les mettre
        dans la liste

        :param noeud1: 1er arbre à transformer en liste
        :type noeud1: ArbreTasMin
        :param noeud2: 2ème arbre à transformer en liste
        :type noeud2: ArbreTasMin
        :param liste: accumulateur, liste des clés récupérées dans les arbres
        :type liste: list[Key]
        :return: Liste contenant toutes les clés des 2 arbres donnés en paramètre
        :rtype: list[Key]
        """
        if noeud1 is None and noeud2 is None:
            return []

        if noeud1 is not None:
            liste.append(noeud1.root.key)

        if noeud2 is not None:
            liste.append(noeud2.root.key)

        if noeud1 is not None:
            ArbreTasMin.ArbreVersListe(noeud1.root.left, liste)
            ArbreTasMin.ArbreVersListe(noeud1.root.right, liste)

        if noeud2 is not None:
            ArbreTasMin.ArbreVersListe(noeud2.root.left, liste)
            ArbreTasMin.ArbreVersListe(noeud2.root.right, liste)

        return liste

    @staticmethod
    def ArbreVersListe(noeud, liste=None):
        """
        Créer une liste à partir de toutes les clés d'un arbre

        :param noeud: arbre à transformer en liste
        :type noeud: ArbreTasMin
        :param liste: accumulateur, liste des clés de l'arbre
        :type liste: list[Key]
        """
        if noeud is None:
            return []

        liste.append(noeud.root.key)

        ArbreTasMin.ArbreVersListe(noeud.root.left, liste)
        ArbreTasMin.ArbreVersListe(noeud.root.right, liste)

    @staticmethod
    def Union(tas1, tas2):
        """
        Récupère les clés des 2 tas donnés en paramètre puis construit le tas en temps linéaire avec ces clés

        :param tas1: tas1 premier tas à fusionner
        :type tas1: ArbreTasMin
        :param tas2: tas2 second tas à fusionner
        :type tas2: ArbreTasMin
        :return: Tas résultant de l'union des tas donnés en arguments
        :rtype: ArbreTasMin
        """
        liste = ArbreTasMin.ArbresVersListe(tas1, tas2)
        tasRes = ArbreTasMin()
        tasRes.Construction(liste)
        return tasRes

    def ConstructionNaive(self, liste):
        """
        Méthode proxy appelant ConstruireDepuisNoeud

        :param liste: (Entrée/Sortie) liste de clés avec lesquelles construire le tas (les clés seront remplacées par
        des ArbreTasMin)
        :type liste: list[Key]
        :return: Tas construit depuis la liste de clés donnée en argument
        :rtype: ArbreTasMin
        """
        return self.ConstruireDepuisNoeud(liste, 0)

    def ConstruireDepuisNoeud(self, liste, index, ancestor=None):
        """
        Construit un tas naïvement à partir d'une liste de clés

        :param liste: (Entrée/Sortie) liste de clés avec lesquelles construire le tas (les clés seront remplacées par
         des ArbreTasMin)
        :type liste: list[Key]
        :param index: index du noeud à ajouter au tas
        :type index: int
        :param ancestor: noeud père du noeud à ajouter au tas
        :type ancestor: Node
        :return: Tas construit depuis la liste de clés donnée en argument
        :rtype: ArbreTasMin
        """
        if index < len(liste):
            arbre = ArbreTasMin(Node(liste[index]))
            arbre.taille = 1
            if ancestor is not None:
                arbre.root.ancestor = ancestor

            liste[index] = arbre
            arbre.root.left = self.ConstruireDepuisNoeud(liste, 2 * index + 1, arbre.root)
            arbre.root.right = self.ConstruireDepuisNoeud(liste, 2 * index + 2, arbre.root)
            if arbre.root.left is not None:
                arbre.taille += arbre.root.left.taille
            if arbre.root.right is not None:
                arbre.taille += arbre.root.right.taille
            return arbre

def verifieArbre(arbre):
    res = True
    if arbre is None:
        return res

    if arbre.root.left is not None:
        res = res and (arbre.root.key.inf(arbre.root.left.root.key) and verifieArbre(arbre.root.left))
        return res

    if arbre.root.right is not None:
        res = res and arbre.root.key.inf(arbre.root.right.root.key) and verifieArbre(arbre.root.right)

    return res
