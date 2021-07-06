# Generator: Takes in a set of parameters, and returns a world object
from .world import World, Character
import random
import noise

class WorldGenerator:
    def __init__(self, game):
        self.game = game

    def get_position_neighbors(self, i, j, depth):

        neighbours = []

        if depth <= 0:
            print("Depth variable needs to be greater than 0")
            exit()


        for n_i in range(i - depth, i + depth):
            for n_j in range(j - depth, j + depth):

                if n_i < 0 or n_i > self.world.height:
                    continue
                if n_j < 0 or n_j > self.world.height:
                    continue

                neighbours.append([n_i, n_j])

        return neighbours


    def generate_rocks(self, world, initial_rock_density, rock_refinement_runs, rock_neighbour_depth, rock_neighbour_number):

        for i in range(world.width):
            for j in range(world.height):


                if world.spawn_point != (i, j) and random.uniform(0, 1) < initial_rock_density:
                    world.map_rock[i][j] = 1


        # for run in rock_refinement_runs:
        #     for i in range(world.width):
        #         for j in range(world.height):
        #             neighbours = 

        return


    def generate_trees(self, world, initial_tree_density, tree_refinement_runs, tree_neighbour_depth, tree_neighbour_number):

        for i in range(world.width):
            for j in range(world.height):
                if world.spawn_point != (i, j) and world.map_rock[i][j] != 1 and random.uniform(0, 1) < initial_tree_density:
                    world.map_tree[i][j] = 1


        return


    def get_world(self, initial_rock_density, initial_tree_density, rock_refinement_runs, tree_refinement_runs, rock_neighbour_depth, tree_neighbour_depth, rock_neighbour_number, tree_neighbour_number) :

        world = World(self.game)

        scale = 10
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        for i in range(world.width):
            for j in range(world.height):

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

        self.generate_rocks(world, initial_rock_density, rock_refinement_runs, rock_neighbour_depth, rock_neighbour_number)
        self.generate_trees(world, initial_tree_density, tree_refinement_runs, tree_neighbour_depth, tree_neighbour_number)
        




        

        world.enemies = []
        for _ in range(5):
            pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            while world.map_tree[pos[0]][pos[1]] == 1:
                pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            world.enemies.append(Character(pos, world))

        return world

    