import pygame

from src.character import Character
from src.bullet import Bullet

class Enemy(Character):

    def __init__(self, game, 
                x, 
                y, 
                target,
                width, 
                height, 
                color, 
                velocity, 
                healthPoints, 
                damage, 
                bulletsPerShot,
                tile,
                bulletTile,
                score):
        Character.__init__(self, game, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot, tile)
        self.target = target
        self.shootRateTick = 30
        self.bulletTile = bulletTile
        self.score = score

    def shoot(self):
        if self.shootRateTick > 0:
            self.shootRateTick -= 1
            return
        self.game.shotSound.play()
        bullet = Bullet(self.game, self.centerX, self.borderBottom + 10, self.centerX, self.game.screenHeight, 100, owner=self, color=self.bulletTile)
        self.game.gameObjects.append(bullet)
        self.shootRateTick = 120
    
    def die(self):
        self.game.blowSound.play()
        Character.die(self)
        self.game.score += self.score

    def update(self):
        if self.healthPoints <= 0:
            self.die()
        self.draw()
        self.shoot()
        self.move(0, self.velocity)        
    
    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)