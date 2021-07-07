# This file should contain rendering and input handling
import sys
import pygame as pg
import numpy as np
import random
import gym
import noise
from .gman import GraphicsManager
from PIL import Image
from .generator import WorldGenerator

class Game(gym.Env):
    A_NOP, A_UP, A_DOWN, A_LEFT, A_RIGHT, A_ATK = range(6)

    def __init__(self):
        self.framerate = 0
        self.width, self.height = (15, 15)
        self.scale = 32

        self.action_space = gym.spaces.Discrete(6)

        pg.init()
        self.screen = pg.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.gman = GraphicsManager(self.scale)

        self.clock = pg.time.Clock()


        initial_rock_density = 0.2
        initial_tree_density = 0.2
        rock_refinement_runs = 2
        tree_refinement_runs = 2
        rock_neighbour_depth = 1
        tree_neighbour_depth = 2
        rock_neighbour_number = 3
        tree_neighbour_number = 5

        base_clear_depth = 1

        self.world = WorldGenerator(self).get_world(initial_rock_density, initial_tree_density, rock_refinement_runs, tree_refinement_runs, rock_neighbour_depth, tree_neighbour_depth, rock_neighbour_number, tree_neighbour_number, base_clear_depth)

    def step(self, action):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.pump()
        
        reward, done = self.world.step(action)

        self.render()
        
        pil_image = Image.frombytes("RGBA", (self.scale * self.width, self.scale * self.height), pg.image.tostring(self.screen,"RGBA", False))
        
        return pil_image, reward, done, {}

    def render(self, mode='human'):
        # Background
        pg.draw.rect(self.screen, (24, 24, 24), (0, 0, self.width * self.scale, self.height * self.scale))
        
        for i in range(self.width):
            for j in range(self.height):
                pg.draw.rect(self.screen, (64, (128 + self.world.map_grass[i][j] * 128) % 256, 64), (i * self.scale, j * self.scale, self.scale, self.scale))
                if self.world.map_tree[i][j] == 1:
                    self.screen.blit(self.gman.sprites['tree'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
                if self.world.map_rock[i][j] == 1:
                    self.screen.blit(self.gman.sprites['rock'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
                if self.world.map_base[i][j] == 1:
                    self.screen.blit(self.gman.sprites['base'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
        
        self.screen.blit(self.gman.sprites['person'], (self.world.player.x * self.scale, self.world.player.y * self.scale), (0, 0, self.scale, self.scale))
        for enemy in self.world.enemies:
            self.screen.blit(self.gman.sprites['skeleton'], (enemy.x * self.scale, enemy.y * self.scale), (0, 0, self.scale, self.scale))

        for arrow in self.world.arrows:
            self.screen.blit(self.gman.sprites['arrow'], (arrow.x * self.scale, arrow.y * self.scale), (0, 0, self.scale, self.scale))
        
        pg.display.flip()
        
        self.clock.tick(int(self.framerate))
