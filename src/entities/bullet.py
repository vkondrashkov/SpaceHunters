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
        self.move(self.deltaX, self.deltaY)
        self.checkCollision()

    def draw(self):
        # Scale bullet's tile according to
        # it's size.
        size = (self.width, self.height)
        scaledTile = pygame.transform.scale(self.tile, size)
        self.game.display.blit(scaledTile, (self.x, self.y))

    def checkCollision(self):
        for entity in self.game.gameObjects:
            # In Objects list stored all entities
            # and current bullet also, so avoid it.
            if entity == self:
                continue

            # Every bullet has its owner, so
            # to avoid situation, where owner could be
            # died from it's own bullet avoid this case.
            if type(entity) == self.owner:
                continue

            # Also bullet can't hurt another bullet
            if type(entity) is Bullet:
                continue
            
            # Bullets can't collide with bonuses,
            # they have own collision behavior.
            if type(entity) is bonus_mod.Bonus:
                continue

            # Explosion entity is also object, we
            # can't hurt explosion, avoid this case also.
            if type(entity) is Explosion:
                continue
            
            # Gets entity borders vertically and horizontally
            # and then checks whether bullet coordinates
            # are located between entity's borders.
            entityBordersX = range(entity.borderLeft, entity.borderRight)
            entityBordersY = range(entity.borderTop, entity.borderBottom)
            if (self.borderLeft in entityBordersX or self.borderRight in entityBordersX) \
                and (self.borderTop in entityBordersY or self.borderBottom in entityBordersY):
                entity.hurt(self.damage)
                self.game.deleteEntity(self)
                