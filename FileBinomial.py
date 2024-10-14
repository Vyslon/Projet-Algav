from TournoiBinomial import *


class FB:

    def __init__(self, tournois=None, taille=0, minDegre: Tournoi = None):
        """
            Description :
            La méthode d'initialisation de la classe FB crée une file binomiale à partir d'une liste de tournois (par défaut, une liste vide si aucun tournoi n'est spécifié).
        """
        self.taille = taille
        self.minDeg = minDegre
        self.tournois = tournois or []

    def EstVide(self):
        """
           EstVide(self) -> bool:

           Description :
           Vérifie si la file binomiale est vide en examinant si sa liste de tournois est vide.
           """
        return self.tournois == []

    def degre(self):
        """
           degre(self) -> int:
           Description :
           Calcule le degré total de la file binomiale en additionnant les valeurs 2^degre
            pour chaque tournoi dans la file.
        """
        res = 0
        for t in self.tournois:
            res += 2 ** (t.degre)
        return res

    def containsDegre(self, degre):
        """
           containsDegre(self, degre) -> bool:
           Description :
           Vérifie si la file binomiale contient un tournoi avec le degré spécifié.
           """
        for t in self.tournois:
            if (t.degre == degre):
                return True
        return False

    def verifFile(self):  # Verifiation de doublon
        """ verifFile(self) -> bool:
            Description :
            Vérifie si la file binomiale est correcte, c'est-à-dire s'il n'y a pas de doublons en termes de degrés dans les tournois.
            """
        if len(self.tournois) == 0:
            print(str(len(self.tournois)))
            return True
        if len(self.tournois) == 1:
            print(str(len(self.tournois)) + " de degré : " + str(self.tournois[0].degre))
            return True
        cpt = self.tournois[0].degre
        res = ""
        for i in range(1, len(self.tournois)):
            res += str(self.tournois[i].degre) + "? " + str(cpt)
            if self.tournois[i].degre >= cpt:
                print(res)
                return False
        return True

    def toString(self):
        res = ""
        for i in range(len(self.tournois)):
            res += " , " + str(self.tournois[i].degre)
        print(res)


def ajoutMin(file: FB, t: Tournoi):
    file.tournois.append(t)
    file.minDeg = t
    file.taille += 1
    return file


def ajout(file: FB, t: Tournoi):
    """
    ajout(file: FB, t: Tournoi) -> FB:
    Paramètres :
    file (FB) : La file binomiale à laquelle ajouter le tournoi.
    t (Tournoi) : Le tournoi à ajouter à la file.
    Description :
    On crée une file avec le tournoi à ajouter, puis on fusionne la file en paramètre et celle de taille 1.
    """
    tmp = ajoutMin(FB(), t)
    return unionFile(file, tmp)


def decapite(t: Tournoi):
    """
    decapite(t: Tournoi) -> FB:
    Paramètre :
    t (Tournoi) : Le tournoi dont les enfants seront ajoutés à une nouvelle file.
    Description :
    Ajoute les enfants du tournoi à une nouvelle file binomiale.
    """
    file = FB()
    for child in t.enfants:
        file = ajout(file, child)
    return file


def reste(file):
    """
    reste(file: FB) -> FB:
    Paramètre :
    file (FB) : La file binomiale à laquelle supprimer le tournoi de plus bas degré.
    Description :
    Supprime le tournoi de plus bas degré de la file binomiale.
    """
    file.tournois.pop(file.taille - 1)
    file.taille -= 1
    if file.taille > 0:
        file.minDeg = file.tournois[file.taille - 1]
    else:
        file.minDeg = None
    return file


def supprMin(file: FB):
    """
        reste(file: FB) -> FB:
        Paramètre :
        file (FB) : file binomiale non vide.
        Description :
        Supprime la racine du tournoi avec la plus petite clé de la file binomiale.
    """
    min = convertToKey((2 ** 128) - 1)
    indice = 0
    for i in range(file.taille):
        if file.tournois[i].key.inf(min):
            min = file.tournois[i].key
            indice = i
    arbre = decapite(file.tournois[indice])
    if (indice == 0):
        return arbre
    else:
        file.tournois.pop(indice)
        file.taille -= 1
        file.minDeg = file.tournois[file.taille - 1]
        return unionFile(file, arbre)


def uFret(F1: FB, F2: FB, T: Tournoi):
    """
    uFret(F1: FB, F2: FB, T: Tournoi) -> FB:
    Paramètres :
    F1 (FB) : Première file binomiale.
    F2 (FB) : Deuxième file binomiale.
    T (Tournoi) : Tournoi en retenue.
    Description :
    Réalise l'opération d'union de file binomiale avec retenue.
    """

    if T.estVide():  # pas de tournoi en retenue
        if F1.EstVide():
            return F2
        if F2.EstVide():
            return F1
        T1 = F1.minDeg
        T2 = F2.minDeg
        if T1.degre < T2.degre:
            return ajoutMin(unionFile(reste(F1), F2), T1)
        if T2.degre < T1.degre:
            return ajoutMin(unionFile(reste(F2), F1), T2)
        if T1.degre == T2.degre:
            return uFret(reste(F1), reste(F2), unionTournois(T1, T2))
    else:  # T tournoi en retenue
        if F1.EstVide():
            return unionFile(ajoutMin(FB(), T), F2)
        if F2.EstVide():
            return unionFile(ajoutMin(FB(), T), F1)
        T1 = F1.minDeg
        T2 = F2.minDeg
        if T.degre < T1.degre and T.degre < T2.degre:
            return ajoutMin(unionFile(F1, F2), T)
        if T.degre == T1.degre and T.degre == T2.degre:
            return ajoutMin(uFret(reste(F1), reste(F2), unionTournois(T1, T2)), T)
        if T.degre == T1.degre and T.degre < T2.degre:
            return uFret(reste(F1), F2, unionTournois(T1, T))
        if T.degre == T2.degre and T.degre < T1.degre:
            return uFret(reste(F2), F1, unionTournois(T2, T))


def unionFile(F1: FB, F2: FB):
    return uFret(F1, F2, Tournoi())


def ajoutIteratif(file: FB, liste: list[Key]):
    """
    ajoutIteratif(file: FB, liste: list[Key]) -> FB:
    Paramètres :
    file (FB) : La file binomiale à laquelle ajouter les clés.
    liste (list[Key]) : Liste de clés à ajouter sous forme de tournois à la file.
    Description :
    Ajoute itérativement des tournois formés à partir des clés de la liste à la file binomiale en utilisant ajout.
    """
    for k in liste:
        temp = ajoutMin(FB(), Tournoi(k))
        file = unionFile(file, temp)
    return file


if __name__ == '__main__':
    file = FB()
    file = ajoutMin(file, Tournoi(convertToKey(40)))
    print("file a un minDeg: " + str(file.minDeg is not None))
    file.toString()

    file2 = ajoutMin(FB(), Tournoi(convertToKey(20)))

    file2.toString()
    print("file2 a un minDeg: " + str(file2.minDeg is not None))
    test = unionFile(FB(), ajoutMin(FB(), Tournoi(convertToKey(2))))
    print("test  a un minDeg: " + str(test.minDeg is not None))

    uniontest = unionFile(file, file2)
    print("uniontest a un minDeg: " + str(uniontest.minDeg is not None))

    uniontest.toString()
    file3 = ajoutMin(FB(), Tournoi(convertToKey(101010)))
    uniontest2 = copy.deepcopy(uniontest)
    unionFile(uniontest2, file3)

    print("----------------------------------")

    file3 = ajoutIteratif(FB(),
                          [convertToKey(10), convertToKey(50), convertToKey(20), convertToKey(14), convertToKey(11),
                           convertToKey(1), convertToKey(2), ])
    file3.toString()
    print(str(len(file3.tournois)))
    file3 = supprMin(file3)
    file3.toString()
    print(str(len(file3.tournois)))
    file3 = supprMin(file3)
    file3.toString()
    print(str(len(file3.tournois)))
