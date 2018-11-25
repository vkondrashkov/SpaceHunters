import pygame

from abc import ABCMeta, abstractmethod
from src.object import Object

class Drawable(Object):
    __metaclass__ = ABCMeta

    @property
    def display(self):
        return self.__display
    
    @property
    def color(self):
        return self.__color

    @abstractmethod
    def __init__(self, display, x=0, y=0, width=0, height=0, color=None):
        Object.__init__(self, x, y, width, height)
        self.__display = display
        self.__color = color
    
    @abstractmethod
    def draw(self):
        pygame.draw.rect(
            self.display,
            self.color,
            [
                self.x,
                self.y,
                self.width,
                self.height
            ]
        )