import copy
import time
import random

from deep_space_trader.items import ItemCollection


def random_planet_number():
    return random.randrange(2, 399)

def random_planet_letter():
    return chr(random.randrange(97, 108))


class Planet(object):
    parts = [
        [
            'ho', 'ce', 'cu', 'he', 'hu', 'sa', 'cy', 'an', 'ir', 'kle', 'ke',
            'ka', 'la', 'ny', 'ky', 'dy', 'bar', 'blar', 'ger', 'yur', 'her',
            'zor', 'for', 'nor', 'wor', 'gor', 'noth', 'roth', 'nith', 'lith',
            'sith', 'dith', 'ith', 'oth', 'orb', 'urb', 'erb', 'zorb', 'zor',
            'zer', 'zerb', 'zera', 'terr', 'err'
        ],
        [
            'ta', 'te', 'ti', 'to', 'tu', 'ba', 'be', 'bi', 'bo', 'tis', 'ris',
            'beur', 'bu', 'po', 'cu', 'lur', 'mur', 'tu', 'da', 'de', 'di', 'do',
            'du', 'ter', 'der', 'ser', 'per', 'fu', 'fer', 'ler', 'zer', 'wi',
            'bre', 'dre', 'pre', 'tre', 're', 'fe', 'ge', 'ga', 'gu', 'du', 'mu',
            'nu', 'ru'
        ],
        [
            'res', 'lia', 'gese', 'naise', 'bler', 'pler', 'teres', 'tere',
            'pules', 'ner', 'yer', 'prer', 'padia', 'dium', 'dum', 'rem', 'tem',
            'tis', 'ratis', 'cus', 'rus', 'tus', 'rus', 'muth', 'yuth', 'reth',
            'roth', 'rath', 'bath', 'tath', 'path', 'padia', 'radia', 'anus',
            'nus', 'ban', 'tan', 'lan', 'dan', 'man', 'nan', 'xan', 'zan', 'pan'
        ],
    ]

    @classmethod
    def _random_planet(cls, long_name_prob=35, number_suffix_prob=35, letter_suffix_prob=35):
        if random.randrange(0, 100) < long_name_prob:
            # 3-part name
            indices = [0, 1, 2]
        else:
            # 2-part name
            indices = [0, 2]

        name = ""
        number = None
        letter = None

        for i in range(len(indices)):
            name += random.choice(cls.parts[indices[i]])

        if random.randrange(0, 100) < number_suffix_prob:
            number = random_planet_number()

            if random.randrange(0, 100) < letter_suffix_prob:
                letter = random_planet_letter()

        return Planet(name, number, letter)

    @classmethod
    def _planet_exists(cls, planet, existing):
        for p in existing:
            if p.full_name == planet.full_name:
                return True

        return False

    @classmethod
    def _unique_planet(cls, existing):
        new = cls._random_planet()
        while cls._planet_exists(new, existing):
            new = cls._random_planet()

        return new

    @classmethod
    def random(cls, num=1, existing=[]):
        max_group_size = 4
        last_planet_with_letter = None
        group_size = None
        ret = []

        for i in range(num):
            if last_planet_with_letter is not None:
                if group_size < max_group_size:
                    new = last_planet_with_letter.neighbour()
                    ret.append(new)
                    last_planet_with_letter = new
                    group_size += 1
                    continue
                else:
                    last_planet_with_letter = None
                    group_size = None

            new = cls._unique_planet(existing)
            if new.letter is not None:
                last_planet_with_letter = new
                group_size = 1
                max_group_size = random.randrange(1, 5)

            ret.append(new)

        return ret

    def __init__(self, name="", number=None, letter=None):
        self._name = name
        self._number = number
        self._letter = letter
        self._visited = False
        self._items = ItemCollection()

    def neighbour(self):
        name = self._name
        number = self._number
        letter = self._letter

        if letter:
            return Planet(name, number, chr(ord(letter) + 1))

        if number:
            return Planet(name, number + 1, letter)

        if random.randrange(0, 100)< 50:
            # Add letter
            letter = random_planet_letter()
        else:
            # Add number
            number = random_planet_number()

        return Planet(name, number, letter)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, val):
        self._items = val

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, val):
        self._visited = val

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def letter(self):
        return self._letter

    @property
    def full_name(self):
        ret = self._name
        if self._number is not None:
            ret += " %d" % self._number

        if self._letter is not None:
            ret += " %s" % self._letter

        return ret[0].upper() + ret[1:]
