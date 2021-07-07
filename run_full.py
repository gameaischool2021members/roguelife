
from game.game import Game
from evo.evo import EvoAlg
import random 
import time

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 0.3
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 0.3
    },
    'rock_refinement_runs' : {
        'dtype' : int,
        'min' : 0,
        'max' : 2
    },
    'tree_refinement_runs' : {
        'dtype' : int,
        'min' : 0,
        'max' : 2
    },
    'rock_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 2
    },
    'tree_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 2
    },
    'rock_neighbour_number' : {
        'dtype' : int,
        'min' : 3,
        'max' : 8
    },
    'tree_neighbour_number' : {
        'dtype' : int,
        'min' : 3,
        'max' : 8
    },
    'base_clear_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 1
    },
    'enemies_crush_trees' : {
        'dtype' : bool
    }
}

ea = EvoAlg(gen_param_specs)
env = Game(evo_system=ea)

while True:
    _, _, done, _ = env.step(env.action_space.sample())
    if done:
        env.reset()