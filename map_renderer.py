from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3
import random 
import random 
import time
import pygame





initial_rock_density = 0.5

initial_tree_density = 0.0

rock_refinement_runs = 2

tree_refinement_runs = 3

rock_neighbour_depth = 1

tree_neighbour_depth = 2

rock_neighbour_number = 4

tree_neighbour_number = 4

base_clear_depth = 1

enemies_crush_trees = True





gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : initial_rock_density,
        'max' : initial_rock_density
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : initial_tree_density,
        'max' : initial_tree_density
    },
    'rock_refinement_runs' : {
        'dtype' : int,
        'min' : rock_refinement_runs,
        'max' : rock_refinement_runs
    },
    'tree_refinement_runs' : {
        'dtype' : int,
        'min' : tree_refinement_runs,
        'max' : tree_refinement_runs
    },
    'rock_neighbour_depth' : {
        'dtype' : int,
        'min' : rock_neighbour_depth,
        'max' : rock_neighbour_depth
    },
    'tree_neighbour_depth' : {
        'dtype' : int,
        'min' : tree_neighbour_depth,
        'max' : tree_neighbour_depth
    },
    'rock_neighbour_number' : {
        'dtype' : int,
        'min' : rock_neighbour_number,
        'max' : rock_neighbour_number
    },
    'tree_neighbour_number' : {
        'dtype' : int,
        'min' : tree_neighbour_number,
        'max' : tree_neighbour_number
    },
    'base_clear_depth' : {
        'dtype' : int,
        'min' : base_clear_depth,
        'max' : base_clear_depth
    },
    'enemies_crush_trees' : {
        'dtype' : bool
    }
}




ea = EvoAlg(gen_param_specs)
env = Game(evo_system=ea)
state = env.reset()
agent = RuleBasedAgent2(env)


state, _, done, _ = env.step(agent.act(state))

while True:
	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:

			if event.key == ord(' '):

				ea = EvoAlg(gen_param_specs)
				env = Game(evo_system=ea)
				state = env.reset()
				agent = RuleBasedAgent2(env)


				state, _, done, _ = env.step(agent.act(state))





