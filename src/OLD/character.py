import pygame

from abc import ABCMeta, abstractmethod
from src.config import config
from src.movable import Movable

class Character(Movable):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, display, x=0, y=0, width=0, height=0, color=None, velocity=0, healthPoints=0, damage=0, bulletsPerShot=0):
        Movable.__init__(self, display, x, y, width, height, color, velocity)
        self.__healthPoints = healthPoints
        self.__damage = damage
        self.__bulletsPerShot = bulletsPerShot
    
    @abstractmethod
    def die(self):
        pass
    
    @abstractmethod
    def hurt(self):
        pass

    @abstractmethod
    def shot(self):
        pass