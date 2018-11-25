import pygame
from random import randint

from src.config import config
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy

class Game:
    gameObjects = []

    @property
    def display(self):
        return self.__display

    def __init__(self, display):
        self.__display = display
        self.spawnEnemyTick = 60

    def start(self):
        clock = pygame.time.Clock()
        player = Player(self)
        self.gameObjects.append(player)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                deltaX = 0
                deltaY = 0
                keys = pygame.key.get_pressed()
                velocity = config["player"]["velocity"]
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    deltaX = -velocity
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    deltaX = velocity
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    deltaY = -velocity
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    deltaY = velocity
                if keys[pygame.K_SPACE]:
                    player.shoot()
            if self.spawnEnemyTick > 0:
                self.spawnEnemyTick -= 1
            else:
                self.gameObjects.append(Enemy(self, randint(0, 590), 0, target=player))
                self.spawnEnemyTick = 120
            self.display.fill(config["colors"]["black"])
            player.move(deltaX, deltaY)
            for object in self.gameObjects:
                object.draw()
            pygame.display.update()
            clock.tick(config["game"]["fps"])

    def deleteEntity(self, obj):
        self.gameObjects.remove(obj)
            