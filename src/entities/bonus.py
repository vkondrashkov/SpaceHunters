import pygame

# Importing whole module to avoid
# circular importing via "from ... import ..."
import src.entities.player as player_mod
from src.entities.movable import Movable
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
        # Bonus' width and height calculates
        # from tiles' size, there is no necessary
        # to set it from constructor
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
        self.game.display.blit(self.tile, (self.x, self.y))
    
    def checkCollision(self):
        for entity in self.game.gameObjects:
            # Bonus collides only with player
            # so checking whether entity is player
            # continue otherwise
            if type(entity) != player_mod.Player:
                continue

            # Gets player borders vertically and horizontally
            # and then checks whether bonus coordinates
            # are located between players's borders.
            playerBordersX = range(entity.borderLeft, entity.borderRight)
            playerBordersY = range(entity.borderTop, entity.borderBottom)
            if (self.borderLeft in playerBordersX or self.borderRight in playerBordersX) \
                and (self.borderTop in playerBordersY or self.borderBottom in playerBordersY):
                if self.type == BonusType.damage:
                    entity.damage += self.value
                elif self.type == BonusType.health:
                    entity.healthPoints += self.value
                self.game.deleteEntity(self)