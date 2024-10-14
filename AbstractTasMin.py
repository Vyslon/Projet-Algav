from abc import abstractmethod


class TasMin:
    """
    Classe représentant un tas min
    """

    @abstractmethod
    def SupprMin(self):
        """
        Supprime la clé minimum du tas
        """
        ...

    @abstractmethod
    def Ajout(self, elt):
        """
        Ajoute le noeud en fin de tas avant de le faire remonter

        :param elt: Le noeud à ajouter
        :type elt: Node
        """
        ...

    @abstractmethod
    def AjoutsIteratifs(self, liste):
        """
        Remplit le tas à partir d'une liste de clés par appels consécutifs à Ajout

        :param liste: Liste de clés
        :type liste: list[Key]
        """
        ...
