import pygame

from abc import ABCMeta, abstractmethod
from src.config import config
from src.movable import Movable

class Character(Movable):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, game, x=0, y=0, width=0, height=0, color=None, velocity=0, healthPoints=0, damage=0, bulletsPerShot=0):
        Movable.__init__(self, game, x, y, width, height, color, velocity)
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

    @abstractmethod
    def move(self, deltaX, deltaY):
        Movable.move(self, deltaX, deltaY)

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