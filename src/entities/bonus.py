import pygame

from src.entities.movable import Movable
from src.entities.player import Player
from src.entities.bonusType import BonusType

class Bonus(Movable):
    @property
    def tile(self):
        return self.__tile
    
    @property
    def deltaX(self):
        return self.__deltaX
    
    @property
    def deltaY(self):
        return self.__deltaY

    @property
    def value(self):
        return self.__value
    
    @property
    def type(self):
        return self.__type

    def __init__(self,
                game,
                x,
                y,
                velocity,
                type,
                tile,
                width=0,
                height=0,
                value=5,
                color=None):
        width, height = tile.get_rect().size
        Movable.__init__(self, game, x, y, width, height, color, velocity)
        self.__tile = tile
        self.__deltaX = 0
        self.__deltaY = velocity
        self.__type = type
        self.__value = value
    
    def update(self):
        self.draw()
        self.move(self.deltaX, self.deltaY)
        self.checkCollision()

    def draw(self):
        size = (self.width, self.height)
        scaledTile = pygame.transform.scale(self.tile, size)
        self.game.display.blit(scaledTile, (self.x, self.y))
    
    def checkCollision(self):
        for entity in self.game.gameObjects:
            if type(entity) != Player:
                continue

            # Gets player borders vertically and horizontally
            # and then checks whether bonus coordinates
            # are located between players's borders.
            playerBordersX = range(entity.borderLeft, entity.borderRight)
            playerBordersY = range(entity.borderTop, entity.borderBottom)
            if (self.x >= entity.borderLeft and self.x <= entity.borderRight) \
                and (self.y >= entity.borderTop and self.y <= entity.borderBottom):
                if self.type == BonusType.damage:
                    entity.damage += self.value
                elif self.type == BonusType.health:
                    entity.healthPoints += self.value
                self.game.deleteEntity(self)