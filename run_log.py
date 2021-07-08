
from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3
import random 
import random 
import time
import sys

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.1,
        'max' : 0.4
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.1,
        'max' : 0.4
    },
    'rock_refinement_runs' : {
        'dtype' : int,
        'min' : 1,
        'max' : 3
    },
    'tree_refinement_runs' : {
        'dtype' : int,
        'min' : 1,
        'max' : 3
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
        'min' : 4,
        'max' : 8
    },
    'tree_neighbour_number' : {
        'dtype' : int,
        'min' : 4,
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
state = env.reset()

agent_classes = {
    'R01' : RuleBasedAgent0,
    'R02' : RuleBasedAgent1,
    'R03' : RuleBasedAgent2,
    'R04' : RuleBasedAgent3
}


if len(sys.argv) == 4 and sys.argv[1] == '--run':
    agent_class = agent_classes[sys.argv[2]]
    agent = agent_class(env)
    i = 0
    while True:
        state, _, done, _ = env.step(agent.act(state))

        if done:
            env.reset()
            i += 1
            agent = agent_class(env)
            if i > 2000:
                env.worldgen.save_log(sys.argv[3])
                quit()