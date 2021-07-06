# Generator: Takes in a set of parameters, and returns a world object
from .world import World, Character
import random
import noise

class WorldGenerator:
    def __init__(self, game):
        self.game = game

    def get_world(self):

        world = World(self.game)

        scale = 10
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        for i in range(world.width):
            for j in range(world.height):


                if world.spawn_point != (i, j) and random.uniform(0, 1) < .1:
                    world.map_rock[i][j] = 1

                world.map_grass[i][j] = noise.pnoise2(
                    i / scale, 
                    j / scale, 
                    octaves=octaves, 
                    persistence=persistence, 
                    lacunarity=lacunarity, 
                    repeatx=world.width, 
                    repeaty=world.height, 
                    base=0
                )
                if world.spawn_point != (i, j) and world.map_rock[i][j] != 1 and random.uniform(0, 1) < .1:
                    world.map_tree[i][j] = 1

        world.enemies = []
        for _ in range(5):
            pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            while world.map_tree[pos[0]][pos[1]] == 1:
                pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            world.enemies.append(Character(pos, world))

        return world

    