import pygame

from abc import ABCMeta, abstractmethod
from src.entities.object import Object

class Drawable(Object):
    __metaclass__ = ABCMeta

    @property
    def display(self):
        return self.game.display
    
    @property
    def game(self):
        return self.__game
    
    @property
    def color(self):
        return self.__color

    @abstractmethod
    def __init__(self, 
                game, 
                x=0, 
                y=0, 
                width=0, 
                height=0, 
                color=None):
        Object.__init__(self, x, y, width, height)
        self.__game = game
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