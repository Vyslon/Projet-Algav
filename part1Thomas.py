import struct


class Key:
    """
    Classe représentant une clé de 128 bits

    Attributes:
        part1: Première partie de la clé (32 bits)
        part2: Deuxième partie de la clé (32 bits)
        part3: Troisième partie de la clé (32 bits)
        part4: Quatrième partie de la clé (32 bits)
    """
    def __init__(self, part1, part2=None, part3=None, part4=None):
        self.parts = [part1, part2, part3, part4]

        if part2 is None:
            self.parts = part1

    def __str__(self):
        """
        Créer une chaîne de caractères contenant les valeurs de toutes les parties de la clé

        :return: Chaîne de caractères contenant les valeurs de toutes les parties de la clé
        :rtype: str
        """
        return ''.join(map(str, self.parts))

    def toString(self):
        """
        Créer une chaîne de caractères contenant les valeurs de toutes les parties de la clé

        :return: Chaîne de caractères contenant les valeurs de toutes les parties de la clé
        :rtype: str
        """
        return ''.join(map(str, self.parts))


    def inf(self, key2):
        """
        On commence par le poid fort de la clé pour vérifier laquelle des clés est supérieure à l'autre,
        tant que les 2 parties des clés sont égales, la boucle continue, à la fin, si toutes les parties sont égales,
        on renvoi false (car c'est un inférieur strict)

        :param key2: clé à comparer à self
        :type key2: Key
        :return: Vrai si self est strictement inférieur à key2
        :rtype: bool
        """
        for index in range(4):
            if self.parts[index] < key2.parts[index]:
                return True
            elif self.parts[index] > key2.parts[index]:
                return False
        return False

    def eg(self, key2):
        """
        Indique si self est équivalent à key2
        Il suffit qu'une seule partie des 2 clés soit différente pour que les clés ne soient pas égales

        :param key2: clé à comparer à self
        :type key2: Key
        :return: Vrai si self est équivalent à key2
        :rtype: bool
        """
        for index in range(4):
            if self.parts[index] != key2.parts[index]:
                return False
        return True


def convertToKey(number):
    """
    Converti un entier en Key

    :param number: entier à transformer en Key
    :type number: int
    :return: La clé crée à partir de l'entier donné en argument
    :rtype: Key
    """
    hex_representation = hex(number)[2:]  # Retirez le préfixe '0x' de la représentation hexadécimale
    hex_representation = hex_representation.zfill(32)  # Assurez-vous que la longueur est de 32 caractères hexadécimaux
    parts = [int(hex_representation[i:i + 8], 16) for i in range(0, 32, 8)]
    return Key(*parts)


# Converti une séquence de bytes en Key (différent de convertToKey qui n'attend pas des bytes en entrée)
def bytesToKey(bytes):
    """"
    Converti une séquence de bytes en Key

    :param number: séquence de bytes à transformer en Key
    :type number: bytes
    :return: La clé crée à partir de la séquence de bytes donnée en argument
    :rtype: Key
    """
    bytes = bytes.hex()
    parts = [int(bytes[i:i + 8], 16) for i in range(0, 32, 8)]
    return Key(*parts)


if __name__ == '__main__':
    key = Key(0x00000000, 0x00000000, 0x00000000, 0x0000000)
    key3 = Key(0x12345671, 0x8765430, 0xABCDABC0, 0xDCBA4320)
    key2 = Key(0x12345678, 0x87654321, 0xABCDABCD, 0xDCBA4321)
    key4 = convertToKey(2001)
    key5 = convertToKey(2002)
    print(key4.inf(key5))
    print(key4)
