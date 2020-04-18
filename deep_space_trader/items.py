import copy
import random

from deep_space_trader import constants as const


class ItemType(object):
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value


common_item_types = [
    ItemType("tin", const.PRICE_TIN),
    ItemType("steel", const.PRICE_STEEL),
    ItemType("copper", const.PRICE_COPPER),
    ItemType("silver", const.PRICE_SILVER),
]

medium_rare_item_types = [
    ItemType("gold", const.PRICE_GOLD),
    ItemType("silicon", const.PRICE_SILICON),
    ItemType("uranium", const.PRICE_URANIUM),
    ItemType("diamond", const.PRICE_DIAMOND),
    ItemType("tritium", const.PRICE_TRITIUM),
    ItemType("platinum", const.PRICE_PLATINUM),
    ItemType("plutonium", const.PRICE_PLUTONIUM)
]

rare_item_types = [
    ItemType("jade stone", const.PRICE_JADESTONE),
    ItemType("antimatter", const.PRICE_ANTIMATTER)
]


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
            quantity_range = const.RARE_QUANTITY_RANGE
        elif prob >= 75:
            # 25% chance of a rare or medium rare item
            choices = medium_rare_item_types
            quantity_range = const.MEDIUM_RARE_QUANTITY_RANGE
        else:
            # otherwise, a common item
            choices = common_item_types
            quantity_range = const.COMMON_QUANTITY_RANGE

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

    def add_items(self, itemname, other, quantity=1, delete_empty=True):
        if itemname not in other.items:
            return

        if itemname not in self.items:
            self.items[itemname] = copy.deepcopy(other.items[itemname])
            self.items[itemname].quantity = 0

        num = min(quantity, other.items[itemname].quantity)
        self.items[itemname].quantity += num
        other.items[itemname].quantity -= num

        if (other.items[itemname].quantity == 0) and delete_empty:
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
