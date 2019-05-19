import pygame

from src.entities.character import Character
from src.entities.bullet import Bullet
from src.entities.explosion import Explosion

class Enemy(Character):

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
                bulletTile,
                score,
                shotRateTick):
        Character.__init__(self, game, 
                                x=x, 
                                y=y, 
                                width=width, 
                                height=height, 
                                velocity=velocity, 
                                healthPoints=healthPoints, 
                                damage=damage, 
                                tile=tile)
        # Shot rate tick, delay between enemy's shots
        self.shotRateTick = shotRateTick
        self.currentTick = shotRateTick // 4
        self.bulletTile = bulletTile
        self.score = score
    
    def update(self):
        self.draw()     
    