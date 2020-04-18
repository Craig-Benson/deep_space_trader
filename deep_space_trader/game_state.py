import random

from deep_space_trader.planet import Planet
from deep_space_trader.items import ItemCollection

PLANET_STEP = 10

class State(object):
    def __init__(self, initial_planets=12):
        self.planets = []
        self.money = 1000
        self.travel_cost = 100
        self.exploration_cost = 1000
        self.capacity = 100
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
