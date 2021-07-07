import gym

import time
from stable_baselines3 import DQN

env = gym.make("CartPole-v0")

model = DQN("MlpPolicy", env, verbose=1, learning_starts=10000, exploration_fraction=0.5)
model.learn(total_timesteps=50000, log_interval=100)


obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=False)
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.01)
    if done:
      print("Reset")
      obs = env.reset()