import pygame
from src.config import config
from src.movable import Movable
from src.drawable import Drawable

class Bullet(Movable):
    @property
    def deltaX(self):
        return self.__deltaX
    
    @property
    def deltaY(self):
        return self.__deltaY
    
    @property
    def owner(self):
        return self.__owner

    def __init__(self, 
                game, 
                x, 
                y, 
                destinationX,
                destinationY,
                velocity,
                owner=None,
                width=5, 
                height=10, 
                color=config["colors"]["white"]):
        Movable.__init__(self, game, x, y, width, height, color, velocity)
        self.__deltaX = (destinationX - x) / 60
        self.__deltaY = (destinationY - y) / 60
        self.__owner = type(owner)

    def draw(self):
        Drawable.draw(self)
        self.move(self.deltaX, self.deltaY)
        self.checkCollision()
    
    def checkCollision(self):
        for entity in self.game.gameObjects:
            if entity == self:
                continue
            if type(entity) == self.owner:
                continue
            if type(entity) is Bullet:
                if entity.owner is self.owner:
                    continue
            if (self.x >= entity.borderLeft and self.x <= entity.borderRight) and (self.y >= entity.borderTop and self.y <= entity.borderBottom):
                self.game.deleteEntity(entity)
                self.game.deleteEntity(self)