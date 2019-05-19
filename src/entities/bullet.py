import pygame

from src.entities.movable import Movable
from src.entities.explosion import Explosion
# Importing whole module to avoid
# circular importing via "from ... import ..."
import src.entities.bonus as bonus_mod

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
    
    # Updates Object's states and
    # checks collision with other
    # objects every game tick.
    def update(self):
        self.draw()

    def draw(self):
        # Scale bullet's tile according to
        # it's size.
        size = (self.width, self.height)
        scaledTile = pygame.transform.scale(self.tile, size)
        self.game.display.blit(scaledTile, (self.x, self.y))
    