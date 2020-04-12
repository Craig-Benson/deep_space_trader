
class ItemType(object):
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value


item_types = [
    ItemType("gold", 20),
    ItemType("silver", 15),
    ItemType("uranium", 35),
    ItemType("plutonium", 40),
    ItemType("silicon", 25)
]

class Items(object):
    def __init__(self, itemtype, quantity, value=None):
        self.type = itemtype
        self.quantity = quantity

        if value is None:
            self.value = itemtype.base_value
        else:
            self.value = value


class ItemCollection(object):
    def __init__(self, items=[]):
        self.items = {}

        if items:
            self.add_items(items)

    def add_items(self, items):
        for item in items:
            if item.type.name in self.items:
                self.items[item.type.name].quantity += item.quantity
            else:
                self.items[item.type.name] = item
