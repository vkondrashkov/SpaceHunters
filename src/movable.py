import pygame

from abc import ABCMeta, abstractmethod
from src.drawable import Drawable
from src.config import config

class Movable(Drawable):
    __metaclass__ = ABCMeta

    @property
    def velocity(self):
        return self.__velocity

    @abstractmethod
    def __init__(self, game, x=0, y=0, width=0, height=0, color=None, velocity=0):
        Drawable.__init__(self, game, x, y, width, height, color)
        self.__velocity = velocity
    
    @abstractmethod
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
        
        screenWidth = config["game"]["width"]
        screenHeight = config["game"]["height"]
        if self.y < 0 or self.y > screenHeight:
            self.game.deleteEntity(self)
        