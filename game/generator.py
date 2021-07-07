# Generator: Takes in a set of parameters, and returns a world object

from .world import World, Character
from .enemy import EnemyController, GridGraph

from scipy.ndimage.measurements import label

import random
import noise
import numpy as np

class WorldGenerator:
    def __init__(self, game):
        self.game = game

    def get_position_neighbours(self, world, matrix, i, j, depth):

        neighbours = []
        bordering_edges = False

        if depth <= 0:
            print("Depth variable needs to be greater than 0")
            exit()

        for n_i in range(i - depth, i + depth + 1):
            for n_j in range(j - depth, j + depth + 1):


                if n_i < 0 or n_i >= world.height:
                    bordering_edges = True
                    continue
                if n_j < 0 or n_j >= world.height:
                    bordering_edges = True
                    continue
                if n_i == i and n_j == j:
                    continue

                if matrix[n_i][n_j]:
                    neighbours.append([n_i, n_j])

        return neighbours, bordering_edges


    def generate_rocks(self, world, initial_rock_density, rock_refinement_runs, rock_neighbour_depth, rock_neighbour_number):

        for i in range(world.width):
            for j in range(world.height):

                if world.spawn_point != (i, j) and random.uniform(0, 1) < initial_rock_density:
                    world.map_rock[i][j] = 1

        for run in range(rock_refinement_runs):
            to_add = []
            to_remove = []
            for i in range(world.width):
                for j in range(world.height):
                    neighbors, bordering = self.get_position_neighbours(world, world.map_rock, i, j, rock_neighbour_depth)
                    if (len(neighbors) >= rock_neighbour_number) and world.spawn_point != (i, j):
                        to_add.append([i, j])
                    else:
                        to_remove.append([i,j])
            for cord in to_add:
                world.map_rock[cord[0]][cord[1]] = 1
            for cord in to_remove:
                world.map_rock[cord[0]][cord[1]] = 0

        return world


    def generate_trees(self, world, initial_tree_density, tree_refinement_runs, tree_neighbour_depth, tree_neighbour_number):

        for i in range(world.width):
            for j in range(world.height):

                if world.spawn_point != (i, j) and random.uniform(0, 1) < initial_tree_density and world.map_rock[i][j] != 1:
                    world.map_tree[i][j] = 3

        for run in range(tree_refinement_runs):
            to_add = []
            to_remove = []
            for i in range(world.width):
                for j in range(world.height):
                    neighbors, bordering = self.get_position_neighbours(world, world.map_tree, i, j, tree_neighbour_depth)
                    if (len(neighbors) >= tree_neighbour_number) and world.map_rock[i][j] != 1 and world.spawn_point != (i, j):
                        to_add.append([i, j])
                    else:
                        to_remove.append([i,j])
            for cord in to_add:
                world.map_tree[cord[0]][cord[1]] = 3
            for cord in to_remove:
                world.map_tree[cord[0]][cord[1]] = 0

        return world


    def generate_world_base_and_player(self, world, initial_rock_density, initial_tree_density, rock_refinement_runs, tree_refinement_runs, rock_neighbour_depth, tree_neighbour_depth, rock_neighbour_number, tree_neighbour_number, clear_depth):

        possibilities = []

        counter = 0

        while len(possibilities) == 0:
            world.map_tree = np.zeros((world.width, world.height))
            world.map_rock = np.zeros((world.width, world.height))
            self.generate_rocks(world, initial_rock_density, rock_refinement_runs, rock_neighbour_depth, rock_neighbour_number)
            self.generate_trees(world, initial_tree_density, tree_refinement_runs, tree_neighbour_depth, tree_neighbour_number)


            for i in range(world.width):
                for j in range(world.height):
                    rock_neighbors, bordering = self.get_position_neighbours(world, world.map_rock, i, j, clear_depth)
                    tree_neighbors, bordering = self.get_position_neighbours(world, world.map_tree, i, j, clear_depth)

                    if (len(rock_neighbors) == 0 and len(tree_neighbors) == 0) and (not bordering):
                            possibilities.append([i, j])

            structure = np.ones((3, 3), dtype=np.int)

            inv_map = 1 - world.map_rock

            labeled, ncomponents = label(inv_map, structure)

            if ncomponents > 1:
                possibilities = []



            counter += 1
            if initial_rock_density > 0.3 or counter > 200:
                initial_rock_density -= 0.01

            if counter > 10000:
                print("World generation parameters don't allow a base with a clear_depth of ", clear_depth)
                exit()


        chosen_one = random.choice(possibilities)

        world.map_base[chosen_one[0]][chosen_one[1]] = 10
        
        world.base_x, world.base_y = chosen_one 
        
        player_possibilities = []

        for n_i in range(chosen_one[1] - clear_depth, chosen_one[1] + clear_depth + 1):
            for n_j in range(chosen_one[0] - clear_depth, chosen_one[0] + clear_depth + 1):
                if n_i != i and n_j != j:
                    player_possibilities.append([n_i, n_j])

        chosen_one = random.choice(player_possibilities)

        world.player.y = chosen_one[0]
        world.player.x = chosen_one[1]


        return


    def get_world(self, initial_rock_density, initial_tree_density, rock_refinement_runs, tree_refinement_runs, rock_neighbour_depth, tree_neighbour_depth, rock_neighbour_number, tree_neighbour_number, base_clear_depth, enemies_crush_trees) :

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

        self.generate_world_base_and_player(world, initial_rock_density, initial_tree_density, rock_refinement_runs, tree_refinement_runs, rock_neighbour_depth, tree_neighbour_depth, rock_neighbour_number, tree_neighbour_number, base_clear_depth)
        

        

        world.enemies = []
        for _ in range(5):
            pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            while world.map_tree[pos[0]][pos[1]] or world.map_rock[pos[0]][pos[1]]:
                pos = (random.randint(0, world.width - 1), random.randint(0, world.height - 1))
            world.enemies.append(EnemyController(Character(pos, world), world, enemies_crush_trees))

        return world

    