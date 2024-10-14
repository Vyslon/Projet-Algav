import math
import random
from math import pow
from string import ascii_letters, digits


# On divise le nombre en boucle, si le reste est égal à 1 c'est que on est sur une de ses puissance de 2,
# Le truc c'est que on a pas besoin de completion pck je continue jusqu'à remplir tout le table a

class KeyBits:
    def __init__(self, first=None, second=None, third=None, fourth=None):
        self.first = first or []
        self.second = second or []
        self.third = third or []
        self.fourth = fourth or []

    def toString(self):
        firststr = ""
        secondstr = ""
        thirstr = ""
        fourthstr = ""
        for j in range(4):
            for i in range(32):
                if j == 0:
                    firststr += " ," + str(self.first[i])
                if j == 1:
                    secondstr += " ," + str(self.second[i])
                if (j == 2):
                    thirstr += " ," + str(self.third[i])
                if (j == 3):
                    fourthstr += " ," + str(self.fourth[i])
        print(firststr)
        print(secondstr)
        print(thirstr)
        print(fourthstr)

    def inf(self, cle2):  # Self < cle2
        for j in reversed(range(4)):
            for i in reversed(range(32)):
                if j == 0 and (self.first[i] != cle2.first[i]):
                    return cle2.first[i]
                elif j == 1 and (self.second[i] != cle2.second[i]):
                    return cle2.second[i]
                elif j == 2 and (self.third[i] != cle2.third[i]):
                    return cle2.third[i]
                elif j == 3 and (self.fourth[i] != cle2.fourth[i]):
                    return cle2.fourth[i]
        return False

    def eg(self, cle2):
        for j in reversed(range(4)):
            for i in reversed(range(32)):
                if self.first[i] != cle2.first[i] or self.second[i] != cle2.second[i] or self.third[i] != cle2.third[
                    i] or self.fourth[i] != cle2.fourth[i]:
                    return False
        return True

    def convertToNumber(self):
        res = 0
        power = 1
        for j in range(4):
            for i in range(32):
                if j == 0 and self.first[i]:
                    res += power
                if j == 1 and self.second[i]:
                    res += power
                if j == 2 and self.third[i]:
                    res += power
                if j == 3 and self.fourth[i]:
                    res += power
                power *= 2
        return res

def convertToKey(nombre):
    if nombre < 0:
        raise ValueError("L'entier doit être positif ou nul.")
    resultat = KeyBits()
    for j in range(4):
        for i in range(32):
            if j == 0:
                resultat.first.append(nombre % 2 == 1)
            if j == 1:
                resultat.second.append(nombre % 2 == 1)
            if (j == 2):
                resultat.third.append(nombre % 2 == 1)
            if (j == 3):
                resultat.fourth.append(nombre % 2 == 1)
            nombre = nombre // 2
    return resultat


if __name__ == '__main__':
    cle1 = convertToKey(100)
    cle2 = convertToKey(51532)
    print(cle2.eg(cle1))
    print(cle2.convertToNumber())
# print(cle1.inf(cle2))
