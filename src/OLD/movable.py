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
    def __init__(self, display, x=0, y=0, width=0, height=0, color=None, velocity=0):
        Drawable.__init__(self, display, x, y, width, height, color)
        self.__velocity = velocity
    
    @abstractmethod
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
        
        screenWidth = config["game"]["resolution"]["width"]
        screenHeight = config["game"]["resolution"]["height"]
        leftBorder = self.x
        rightBorder = self.x + self.width
        topBorder = self.y
        bottomBorder = self.y + self.height
        if leftBorder <= 0 and deltaX < 0:
            self.x = 0
        if rightBorder >= screenWidth and deltaX > 0:
            self.x = screenWidth - self.width
        if topBorder <= 0 and deltaY < 0:
            self.y = 0
        if bottomBorder >= screenHeight and deltaY > 0:
            self.y = screenHeight - self.height