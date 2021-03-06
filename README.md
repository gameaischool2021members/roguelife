# Roguelife 💀
The game that both plays and develops itself

More elaborated, this project is about pitting AI agents against a procedural level generator. The level generator will adapt to the player over time. For illustration purposes, we have designed some rule-based agents who use very specific strategies, to see how the generator "responds" to that. For the full experiment, we want to run a learning agent (using a DQN), that will learn to exploit the environment, all while the environment learns to exploit the agent.

## Authors
- Jonathan Jørgensen
- Pedro M. Fernandes
- Even Klemsdal
- Niels NTG Poldervaart

## Architecture
![Architecture](doc/arch.png)

## Running
### Evolve Levels for the Rule Based Agents
- Run the run_all.sh script. This will evolve a population of difficult maps for each one of the Rule Based Agents.
### Train the RL Agent against the environment
- Run the run_dqn.py file with the --train argument and the name of the training session. Example: "python3 run_dqn.py --train Q01"

## Dependencies
```
pygame
numpy
gym
pillow
scipy
stable_baselines3
```

## Screenshots
<img src="./doc/screenshot1.png" width=30%/><img src="./doc/screenshot2.png" width=30%/><img src="./doc/screenshot3.png" width=30%/>

## Video
[Training Montage](https://drive.google.com/file/d/1-C4bBehG-3zYwyCrGEYSs35uZPIEWhg0/view)

## Presentation Slides
[Click here!](doc/roguelife_presentation.pdf)

