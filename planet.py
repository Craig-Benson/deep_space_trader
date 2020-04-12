import copy
import time
import random


def random_planet_number():
    return random.randrange(2, 399)

def random_planet_letter():
    return chr(random.randrange(97, 108))


class Planet(object):
    parts = [
        [
            'ho', 'ce', 'cu', 'he', 'hu', 'sa', 'cy', 'an', 'ir', 'kle', 'ke',
            'ka', 'la', 'ny', 'ky', 'dy', 'bar'
        ],
        [
            'ta', 'te', 'ti', 'to', 'tu', 'ba', 'be', 'bi', 'bo', 'bu', 'tis',
            'beur', 'bu', 'po', 'cu', 'ur', 'tu', 'da', 'de', 'di', 'do', 'du',
            'ter', 'der', 'ser', 'per'
        ],
        [
            'res', 'alia', 'gese', 'naise', 'bler', 'pler', 'eres', 'aeder',
            'upules', 'under', 'adia', 'adium', 'um', 'em', 'attis', 'atis',
            'cus', 'rus', 'tus', 'ius'
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
    def random(cls, num=1):
        if num == 1:
            return cls._random_planet()

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

            new = cls._random_planet()
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

for planet in Planet.random(num=100000):
    print(planet.full_name)
