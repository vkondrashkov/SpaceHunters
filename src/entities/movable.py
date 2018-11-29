import pygame

from abc import ABCMeta, abstractmethod
from src.entities.drawable import Drawable

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
        
        # To avoid memory leaks deletes 
        # all objects that reached Screen 
        # borders by vertical coordinate.
        if self.y < 0 or self.y > self.game.screenHeight:
            self.game.deleteEntity(self)
        