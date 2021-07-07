
from game.game import Game
import random 
import time

env = Game()



while True:
    pil_image, reward, done, thing = env.step(env.action_space.sample())
    if done:
    	env.reset()