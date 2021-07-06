# Generator: Takes in a set of parameters, and returns a world object
from .world import World

class WorldGenerator:
    def __init__(self, game):
        self.game = game

    def get_world(self):
        return World(self.game)

    