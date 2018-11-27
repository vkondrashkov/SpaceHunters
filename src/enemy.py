import pygame

from src.character import Character
from src.drawable import Drawable
from src.bullet import Bullet
from src.config import config

class Enemy(Character):

    enemyTile = pygame.image.load("enemy.png")

    def __init__(self, game, 
                x, 
                y, 
                target=None,
                width=config["enemy"]["width"], 
                height=config["enemy"]["height"], 
                color=config["colors"]["red"], 
                velocity=config["enemy"]["velocity"], 
                healthPoints=config["enemy"]["healthPoints"], 
                damage=config["enemy"]["damage"], 
                bulletsPerShot=config["enemy"]["bulletsPerShot"]):
        Character.__init__(self, game, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot)
        self.enemyTile = pygame.transform.scale(self.enemyTile, (self.width, self.height))
        self.target = target
        self.shootRateTick = 0

    def shoot(self):
        if self.shootRateTick > 0:
            self.shootRateTick -= 1
            return
        bullet = Bullet(self.game, self.centerX, self.borderBottom + 10, self.centerX, config["game"]["height"], 100, owner=self, color=config["enemy"]["bulletColor"])
        self.game.gameObjects.append(bullet)
        self.shootRateTick = 120

    def draw(self):
        self.game.display.blit(self.enemyTile, (self.x, self.y))

    def update(self):
        if self.healthPoints <= 0:
            self.die()
        self.draw()
        self.shoot()
        self.move(0, config["enemy"]["velocity"])        
    
    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)