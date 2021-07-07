
from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent
import random 
import time

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
env = Game(evo_system=ea)
state = env.reset()

env = DummyVecEnv([lambda : env])

model = DQN("CnnPolicy", env, verbose=1, buffer_size=10000, learning_starts=5000, exploration_fraction=0.3)
model.learn(total_timesteps=100000, log_interval=4)

agent = RuleBasedAgent(env)


while True:
    state, _, done, _ = env.step(agent.act(state))
    
    if done:
        env.reset()
        agent = RuleBasedAgent(env)

"""
env = DummyVecEnv([lambda: Game()])

model = DQN("CnnPolicy", env, verbose=1, buffer_size=10000, learning_starts=5000, exploration_fraction=0.3)
model.learn(total_timesteps=100000, log_interval=4)

obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=False)
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.01)
    if done:
        print("Reset")
        obs = env.reset()
"""