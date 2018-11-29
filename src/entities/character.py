import pygame

from abc import ABCMeta, abstractmethod
from src.entities.movable import Movable

class Character(Movable):
    __metaclass__ = ABCMeta
    
    @property
    def tile(self):
        return self.__tile

    @abstractmethod
    def __init__(self, 
                game, 
                x=0, 
                y=0, 
                width=0, 
                height=0, 
                velocity=0, 
                healthPoints=0, 
                damage=0, 
                color=None, 
                tile=None):
        Movable.__init__(self, game, x, y, width, height, color, velocity)
        self.healthPoints = healthPoints
        self.damage = damage
        self.__tile = tile

    @abstractmethod
    def die(self):
        self.game.deleteEntity(self)
    
    @abstractmethod
    def hurt(self, damage):
        self.healthPoints -= damage

    @abstractmethod
    def shot(self):
        pass
    
    @abstractmethod
    def draw(self):
        scaledTile = pygame.transform.scale(self.tile, (self.width, self.height))
        self.game.display.blit(scaledTile, (self.x, self.y))