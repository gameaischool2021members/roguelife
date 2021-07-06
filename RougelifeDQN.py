import time

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

from game.game import Game

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
