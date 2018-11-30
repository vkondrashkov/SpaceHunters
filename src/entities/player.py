import pygame

from src.entities.character import Character
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy

class Player(Character):
    def __init__(self, 
                game, 
                x, 
                y, 
                width, 
                height, 
                velocity, 
                healthPoints, 
                damage, 
                tile, 
                bulletTile):
        Character.__init__(self, game, 
                                x=x, 
                                y=y, 
                                width=width, 
                                height=height,
                                velocity=velocity, 
                                healthPoints=healthPoints, 
                                damage=damage, 
                                tile=tile)
        self.bulletTile = bulletTile
        self.playerTile = pygame.transform.scale(tile, (self.width, self.height))
        self.shotTick = 0


    def shoot(self):
        # Sets player's shot tick to avoid
        # infinitely shooting
        self.shotTick = 5
        self.game.shotSound.play()
        bullet = Bullet(self.game, self.centerX, self.y - 10, 
                        self.centerX, 0, 100, 
                        owner=self, damage=self.damage, tile=self.bulletTile)
        self.game.gameObjects.append(bullet)

    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)
        
        # Defines vertical and horizontal borders
        # for player in order to make "playground"
        heightBounds = self.game.screenHeight / 2
        if self.y <= heightBounds and deltaY < 0:
            self.y = heightBounds
        if self.borderLeft <= 0 and deltaX < 0:
            self.x = 0
        if self.borderRight >= self.game.screenWidth and deltaX > 0:
            self.x = self.game.screenWidth - self.width
        if self.borderBottom >= self.game.screenHeight and deltaY > 0:
            self.y = self.game.screenHeight - self.height

    def update(self):
        if self.healthPoints <= 0:
            self.die()
        self.checkCollision()
        self.draw()
    
    def die(self):
        self.game.blowSound.play()
        Character.die(self)
        self.game.end()
    
    def checkCollision(self):
        for entity in self.game.gameObjects:
            # Player's collision contacts only
            # with enemies, because bullets and
            # bonuses collision have own behavior.
            if type(entity) != Enemy:
                continue
            entityBordersX = range(entity.borderLeft, entity.borderRight)
            entityBordersY = range(entity.borderTop, entity.borderBottom)
            if (self.borderLeft in entityBordersX or self.borderRight in entityBordersX) \
                and (self.borderTop in entityBordersY or self.borderBottom in entityBordersY):
                self.game.deleteEntity(self)
                self.game.end() 