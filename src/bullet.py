import pygame

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

    @property
    def damage(self):
        return self.__damage
    
    @property
    def tile(self):
        return self.__tile

    def __init__(self, 
                game, 
                x, 
                y, 
                destinationX,
                destinationY,
                velocity,
                damage=1,
                owner=None,
                width=5, 
                height=10, 
                color=None,
                tile=None):
        Movable.__init__(self, game, x, y, width, height, color, velocity)
        self.__tile = tile
        self.__deltaX = (destinationX - x) / 60
        self.__deltaY = (destinationY - y) / 60
        self.__owner = type(owner)
        self.__damage = damage
    
    def update(self):
        self.draw()
        self.move(self.deltaX, self.deltaY)
        self.checkCollision()

    def draw(self):
        scaledTile = pygame.transform.scale(self.tile, (self.width, self.height))
        self.game.display.blit(scaledTile, (self.x, self.y))

    def checkCollision(self):
        for entity in self.game.gameObjects:
            if entity == self:
                continue
            if type(entity) == self.owner:
                continue
            if type(entity) is Bullet:
                continue
            if (self.x >= entity.borderLeft and self.x <= entity.borderRight) and (self.y >= entity.borderTop and self.y <= entity.borderBottom):
                entity.hurt(self.damage)
                self.game.deleteEntity(self)
                