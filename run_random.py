
from game.game import Game
import random 
import time

env = Game()

while True:
    env.step(env.action_space.sample())