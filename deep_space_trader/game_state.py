from deep_space_trader.planet import Planet


class State(object):
    def __init__(self, initial_planets=12):
        self.planets = Planet.random(num=initial_planets)
        self.money = 0
        self.capacity = 100
        self.items = []
