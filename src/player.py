import pygame

from src.character import Character
from src.config import config
from src.bullet import Bullet

class Player(Character):
    gameConfig = config["game"]
    playerConfig = config["player"]

    playerTile = pygame.image.load("player.png")

    def __init__(self, game, 
                x=(gameConfig["width"] - playerConfig["width"]) / 2, 
                y=gameConfig["height"] - playerConfig["height"] - 100, 
                width=playerConfig["width"], 
                height=playerConfig["height"], 
                color=playerConfig["color"], 
                velocity=playerConfig["velocity"], 
                healthPoints=playerConfig["healthPoints"], 
                damage=playerConfig["damage"], 
                bulletsPerShot=playerConfig["bulletsPerShot"]):
        Character.__init__(self, game, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot)
        self.playerTile = pygame.transform.scale(self.playerTile, (self.width, self.height))


    def shoot(self):
        bullet = Bullet(self.game, self.centerX, self.y - 10, self.centerX, 0, 100, owner=self, damage=self.damage, color=self.playerConfig["bulletColor"])
        self.game.gameObjects.append(bullet)

    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)
        
        screenBounds = config["game"]["height"] / 2
        screenWidth = config["game"]["width"]
        screenHeight = config["game"]["height"]
        if self.y <= screenBounds and deltaY < 0:
            self.y = screenBounds
        if self.borderLeft <= 0 and deltaX < 0:
            self.x = 0
        if self.borderRight >= screenWidth and deltaX > 0:
            self.x = screenWidth - self.width
        if self.borderBottom >= screenHeight and deltaY > 0:
            self.y = screenHeight - self.height

    def draw(self):
        self.game.display.blit(self.playerTile, (self.x, self.y))

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
            if (self.borderLeft in entityBordersX or self.borderRight in entityBordersX) and (self.borderTop in entityBordersY or self.borderBottom in entityBordersY):
                self.game.deleteEntity(self)
                self.game.end() 