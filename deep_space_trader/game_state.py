import random

from deep_space_trader.planet import Planet
from deep_space_trader.items import ItemCollection
from deep_space_trader import constants as const


class State(object):
    def __init__(self, initial_planets=const.INITIAL_PLANET_COUNT):
        self.planets = []
        self.money = const.INITIAL_MONEY
        self.travel_cost = const.INITIAL_TRAVEL_COST
        self.capacity = const.INITIAL_ITEM_CAPACITY
        self.store_items = []
        self.items = ItemCollection()
        self.warehouse = ItemCollection()
        self.level = 1

        self.expand_planets(initial_planets)
        self.current_planet = self.planets[0]
        self.current_planet.visited = True

        self.previous_planet = None

    def change_current_planet(self, planetname):
        for p in self.planets:
            if p.full_name == planetname:
                self.previous_planet = self.current_planet
                self.current_planet = p
                self.current_planet.visited = True
                return

    def expand_planets(self, num_new=None):
        if num_new is None:
            num_new = random.randrange(1, 10)

        new_planets = Planet.random(num=num_new)
        for new in new_planets:
            new.items = ItemCollection.random(value_multiplier=self.level,
                                              quantity_multiplier=self.level)

        self.planets+= new_planets
