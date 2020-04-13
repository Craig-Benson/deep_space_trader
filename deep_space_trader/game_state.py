from deep_space_trader.planet import Planet
from deep_space_trader.items import ItemCollection

PLANET_STEP = 10

class State(object):
    def __init__(self, initial_planets=12):
        self.planets = []
        self.money = 0
        self.capacity = 100
        self.items = ItemCollection()
        self.warehouse = ItemCollection()
        self.level = 1

        self.expand_planets()
        self.current_planet = self.planets[0]
        self.current_planet.visited = True

    def expand_planets(self):
        num_new = PLANET_STEP * self.level
        for _ in range(num_new):
            new = Planet.random()
            new.items = ItemCollection.random(value_multiplier=self.level,
                                              quantity_multiplier=self.level)
            self.planets.append(new)
