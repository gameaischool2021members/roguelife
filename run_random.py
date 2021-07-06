
from env.game import Game
import random 

env = Game()

while True:
    env.step(env.action_space.sample())