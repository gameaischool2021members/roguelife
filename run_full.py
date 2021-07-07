
from game.game import Game
from evo.evo import EvoAlg
import random 
import time

env = Game()

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 1.0
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 1.0
    }
}

ea = EvoAlg(gen_param_specs)
init_pop = ea.get_initial_population()
while True:
    # Mock fitness
    fit_pop = [(x, 0) for x in init_pop]
    ea.get_new_generation(fit_pop)
    env.step(env.action_space.sample())
