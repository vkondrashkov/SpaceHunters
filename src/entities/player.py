import pygame

from src.entities.character import Character
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy

class Player(Character):
    def __init__(self, 
                game, 
                x, 
                y, 
                width, 
                height, 
                velocity, 
                healthPoints, 
                damage, 
                tile, 
                bulletTile):
        Character.__init__(self, game, 
                                x=x, 
                                y=y, 
                                width=width, 
                                height=height,
                                velocity=velocity, 
                                healthPoints=healthPoints, 
                                damage=damage, 
                                tile=tile)
        self.bulletTile = bulletTile
        self.playerTile = pygame.transform.scale(tile, (self.width, self.height))
        self.shotTick = 0

    def update(self):
        self.draw()
    