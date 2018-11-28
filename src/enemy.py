import pygame

from src.character import Character
from src.bullet import Bullet
from src.explosion import Explosion

class Enemy(Character):

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
                bulletTile,
                score,
                shotRateTick):
        Character.__init__(self, game, 
                                x=x, 
                                y=y, 
                                width=width, 
                                height=height, 
                                velocity=velocity, 
                                healthPoints=healthPoints, 
                                damage=damage, 
                                tile=tile)
        self.shotRateTick = shotRateTick
        self.shootRateTick = 30
        self.bulletTile = bulletTile
        self.score = score

    def shoot(self):
        if self.shootRateTick > 0:
            self.shootRateTick -= 1
            return
        self.game.shotSound.play()
        bullet = Bullet(self.game, self.centerX, self.borderBottom + 10, self.centerX, self.game.screenHeight, 100, owner=self, tile=self.bulletTile, damage=self.damage)
        self.game.gameObjects.append(bullet)
        self.shootRateTick = self.shotRateTick
    
    def die(self):
        self.game.blowSound.play()
        explosion = Explosion(self.game, self.x, self.y, self.width, self.height, self.game.explosionFrames, 5)
        self.game.gameObjects.append(explosion)
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