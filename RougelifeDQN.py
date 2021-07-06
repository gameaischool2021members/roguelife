import time

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

from game.game import Game

# Will not run atm.
# TODO: add state encoder (grayscale, scale down, etc..) needed for replay buffer

env = DummyVecEnv([lambda: Game()])

model = DQN("CnnPolicy", env, verbose=1, buffer_size=1000)
model.learn(total_timesteps=100000, log_interval=100)

obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=False)
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.01)
    if done:
        print("Reset")
        obs = env.reset()
