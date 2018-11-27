import pygame

from abc import ABCMeta, abstractmethod
from src.config import config
from src.movable import Movable

class Character(Movable):
    __metaclass__ = ABCMeta

    @property
    def damage(self):
        return self.__damage

    @abstractmethod
    def __init__(self, game, x=0, y=0, width=0, height=0, color=None, velocity=0, healthPoints=0, damage=0, bulletsPerShot=0):
        Movable.__init__(self, game, x, y, width, height, color, velocity)
        self.healthPoints = healthPoints
        self.__damage = damage
        self.__bulletsPerShot = bulletsPerShot
    
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
    def move(self, deltaX, deltaY):
        Movable.move(self, deltaX, deltaY)