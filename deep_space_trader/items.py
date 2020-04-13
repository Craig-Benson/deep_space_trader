import copy
import random


class ItemType(object):
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value


common_item_types = [
    ItemType("steel", 10),
    ItemType("copper", 15),
    ItemType("silver", 15)
]

medium_rare_item_types = [
    ItemType("gold", 20),
    ItemType("silicon", 25),
    ItemType("uranium", 35),
    ItemType("plutonium", 40),
]

rare_item_types = [
    ItemType("antimatter", 185)
]

common_quantity_range = (10, 100)
medium_rare_quantity_range = (1, 20)
rare_quantity_range = (1, 5)


class Items(object):
    def __init__(self, itemtype, quantity, value=None):
        self.type = itemtype
        self.quantity = quantity

        if value is None:
            self.value = itemtype.base_value
        else:
            self.value = value

    @classmethod
    def random(cls, value_multiplier=1.0, quantity_multiplier=1.0):
        prob = random.randrange(0, 100)
        choices = None
        quantity_range = None

        if prob >= 95:
            # 5% chance of a rare item
            choices = rare_item_types
            quantity_range = rare_quantity_range
        elif prob >= 75:
            # 25% chance of a rare or medium rare item
            choices = medium_rare_item_types
            quantity_range = medium_rare_quantity_range
        else:
            # otherwise, a common item
            choices = common_item_types
            quantity_range = rare_quantity_range

        itemtype = random.choice(choices)
        quantity = random.randrange(quantity_range[0], quantity_range[1] + 1)
        quantity *= quantity_multiplier
        
        value = random.randrange(int(itemtype.base_value / 2), int(itemtype.base_value * 2))
        value *= value_multiplier

        return Items(itemtype, quantity, value)


class ItemCollection(object):
    def __init__(self, items=[]):
        self.items = {}

        for item in items:
            if item.type.name not in self.items:
                self.items[item.type.name] = item

            self.items[item.type.name].quantity += item.quantity

    def add_items(self, itemname, other, quantity=1):
        if itemname not in other.items:
            return

        if itemname not in self.items:
            self.items[itemname] = copy.deepcopy(other.items[itemname])
            self.items[itemname].quantity = 0

        num = min(quantity, other.items[itemname].quantity)
        self.items[itemname].quantity += num
        other.items[itemname].quantity -= num

        if other.items[itemname].quantity == 0:
            del other.items[itemname]

    def count(self):
        ret = 0
        for name in self.items:
            ret += self.items[name].quantity

        return ret

    @classmethod
    def random(cls, num=None, value_multiplier=1.0, quantity_multiplier=1.0):
        if num is None:
            num = random.randrange(2, 25)

        items = [Items.random(value_multiplier, quantity_multiplier) for _ in range(num)]
        return ItemCollection(items)
