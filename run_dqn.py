from game.game import Game
from evo.evo import EvoAlg
import random 
import time
import sys

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 0.5
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.0,
        'max' : 0.5
    },
    'rock_refinement_runs' : {
        'dtype' : int,
        'min' : 0,
        'max' : 5
    },
    'tree_refinement_runs' : {
        'dtype' : int,
        'min' : 0,
        'max' : 5
    },
    'rock_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 1
    },
    'tree_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 1
    },
    'rock_neighbour_number' : {
        'dtype' : int,
        'min' : 3,
        'max' : 3
    },
    'tree_neighbour_number' : {
        'dtype' : int,
        'min' : 3,
        'max' : 3
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
env = DummyVecEnv([lambda : Game(evo_system=ea)])

if len(sys.argv) == 3 and sys.argv[1] == '--train':
    model = DQN('CnnPolicy', env, verbose=1, buffer_size=10000, learning_starts=5000, exploration_fraction=0.3)
    model.learn(total_timesteps=1000, log_interval=4)
    model.save('saved_models/{}'.format(sys.argv[2]))

if len(sys.argv) == 3 and sys.argv[1] == '--run':
    model = DQN.load('saved_models/{}'.format(sys.argv[2]), env=env)
    obs = env.reset()

    while True:
        action, _ = model.predict(obs, deterministic=False)
        obs, reward, done, info = env.step(action)

        if done:
            obs = env.reset()
