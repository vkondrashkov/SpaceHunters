import pygame

from src.character import Character
from src.bullet import Bullet

class Player(Character):
    playerTile = pygame.image.load("player.png")

    def __init__(self, game, x, y, width, height, 
                color, velocity, healthPoints, 
                damage, bulletsPerShot, tile,
                bulletTile):
        Character.__init__(self, game, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot, tile)
        self.bulletTile = bulletTile
        self.playerTile = pygame.transform.scale(self.playerTile, (self.width, self.height))


    def shoot(self):
        bullet = Bullet(self.game, self.centerX, self.y - 10, self.centerX, 0, 100, owner=self, damage=self.damage, color=self.bulletTile)
        self.game.gameObjects.append(bullet)

    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)
        
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
        Character.die(self)
        self.game.end()
    
    def checkCollision(self):
        for entity in self.game.gameObjects:
            if entity == self:
                continue
            if type(entity) is Bullet:
                continue
            entityBordersX = range(entity.borderLeft, entity.borderRight)
            entityBordersY = range(entity.borderTop, entity.borderBottom)
            playerBordersX = range(self.borderLeft, self.borderRight)
            playerBordersY = range(self.borderTop, self.borderBottom)
            if ((self.borderLeft in entityBordersX or self.borderRight in entityBordersX) \
                and (self.borderTop in entityBordersY or self.borderBottom in entityBordersY)):
                self.game.deleteEntity(self)
                self.game.end() 