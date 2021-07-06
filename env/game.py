import pygame as pg
import numpy as np
import random
import gym
import noise
from .gman import GraphicsManager
from PIL import Image

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
        self.spawn_point = (self.width // 2, self.height // 2)
        self.player = Character(self.spawn_point, self)
        self.arrows = []

        self.map_grass = np.zeros((self.width, self.height))
        self.map_tree = np.zeros((self.width, self.height))
        self.generate_world()

        self.enemies = []
        for _ in range(5):
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            while self.map_tree[pos[0]][pos[1]] == 1:
                pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            self.enemies.append(Character(pos, self))

    def step(self, action):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.pump()
        
        if action == self.A_ATK:
            self.arrows.append(Arrow((self.player.x, self.player.y), self.player.facing, self))    
        else:
            self.player.move(action)

        for arrow in self.arrows:
            arrow.move()
        self.arrows = list(filter(lambda x: x.active, self.arrows))
        
        n_enemies = len(self.enemies)
        for enemy in self.enemies:
            enemy.move(random.choice([Game.A_UP, Game.A_DOWN, Game.A_LEFT, Game.A_RIGHT]))
        self.enemies = list(filter(lambda x: x.active, self.enemies))
        reward = n_enemies - len(self.enemies)
        
        self.render()
        
        pil_image = Image.frombytes("RGBA", (self.scale * self.width, self.scale * self.height), pg.image.tostring(self.screen,"RGBA", False))
        done = False
        
        return pil_image, reward, done, {}

    def render(self, mode='human'):
        # Background
        pg.draw.rect(self.screen, (24, 24, 24), (0, 0, self.width * self.scale, self.height * self.scale))
        
        for i in range(self.width):
            for j in range(self.height):
                pg.draw.rect(self.screen, (64, (128 + self.map_grass[i][j] * 128) % 256, 64), (i * self.scale, j * self.scale, self.scale, self.scale))
                if self.map_tree[i][j] == 1:
                    self.screen.blit(self.gman.sprites['tree'], (i * self.scale, j * self.scale), (0, 0, self.scale, self.scale))
        
        self.screen.blit(self.gman.sprites['person'], (self.player.x * self.scale, self.player.y * self.scale), (0, 0, self.scale, self.scale))
        for enemy in self.enemies:
            self.screen.blit(self.gman.sprites['skeleton'], (enemy.x * self.scale, enemy.y * self.scale), (0, 0, self.scale, self.scale))

        for arrow in self.arrows:
            self.screen.blit(arrow.get_sprite(), (arrow.x * self.scale, arrow.y * self.scale), (0, 0, self.scale, self.scale))
        
        pg.display.flip()
        
        self.clock.tick(int(self.framerate))
    
    def generate_world(self):
        # Simple perlin noise

        scale = 10
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        for i in range(self.width):
            for j in range(self.height):
                self.map_grass[i][j] = noise.pnoise2(
                    i / scale, 
                    j / scale, 
                    octaves=octaves, 
                    persistence=persistence, 
                    lacunarity=lacunarity, 
                    repeatx=self.width, 
                    repeaty=self.height, 
                    base=0
                )
                if self.spawn_point != (i, j) and random.uniform(0, 1) < .1:
                    self.map_tree[i][j] = 1
    
    def is_pos_free(self, pos):
        return self.map_tree[pos[0]][pos[1]] != 1

class Character:
    DIR_S, DIR_W, DIR_N, DIR_E = range(4)

    def __init__(self, init_pos, world):
        self.x, self.y = init_pos
        self.facing = self.DIR_S
        self.world = world
        self.active = True

    def move(self, action):
        if action == Game.A_NOP:
            return
        target_pos = (self.x, self.y)

        if action == Game.A_UP:
            if self.facing == self.DIR_N:
                target_pos = (self.x, (self.y - 1) % self.world.height)
            else:
                self.facing = self.DIR_N

        if action == Game.A_DOWN:
            if self.facing == self.DIR_S:
                target_pos = (self.x, (self.y + 1) % self.world.height)
            else:
                self.facing = self.DIR_S
        
        if action == Game.A_LEFT:
            if self.facing == self.DIR_W:
                target_pos = ((self.x - 1) % self.world.width, self.y)
            else:
                self.facing = self.DIR_W

        if action == Game.A_RIGHT:
            if self.facing == self.DIR_E:
                target_pos = ((self.x + 1) % self.world.width, self.y)
            else:
                self.facing = self.DIR_E
            
        if self.world.is_pos_free(target_pos):
            self.x, self.y = target_pos

class Arrow:
    DIR_S, DIR_W, DIR_N, DIR_E = range(4)

    def __init__(self, init_pos, init_dir, world):
        self.x, self.y = init_pos
        self.facing = init_dir
        self.world = world
        self.active = True

    def move(self):
        if self.facing == Arrow.DIR_S: 
            self.y += 1
        if self.facing == Arrow.DIR_W:
            self.x -= 1
        if self.facing == Arrow.DIR_N:
            self.y -= 1
        if self.facing == Arrow.DIR_E:
            self.x += 1

        if self.x not in range(0, self.world.width) or \
           self.y not in range(0, self.world.height) or \
           self.world.map_tree[self.x][self.y] == 1:
            self.active = False
        
        for enemy in self.world.enemies:
            if self.x == enemy.x and self.y == enemy.y:
                enemy.active = False
                self.active = False
            

    def get_sprite(self):
        if self.facing == Arrow.DIR_S: 
            return pg.transform.rotate(self.world.gman.sprites['arrow'], 180)
        if self.facing == Arrow.DIR_W:
            return pg.transform.rotate(self.world.gman.sprites['arrow'], 90)
        if self.facing == Arrow.DIR_N:
            return self.world.gman.sprites['arrow']
        if self.facing == Arrow.DIR_E:
            return pg.transform.rotate(self.world.gman.sprites['arrow'], 270)
