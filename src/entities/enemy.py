import pygame

from src.entities.character import Character
from src.entities.bullet import Bullet
from src.entities.explosion import Explosion

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
        # Shot rate tick, delay between enemy's shots
        self.shotRateTick = shotRateTick
        self.currentTick = shotRateTick // 4
        self.bulletTile = bulletTile
        self.score = score

    def shoot(self):
        if self.currentTick > 0:
            self.currentTick -= 1
            return
        self.game.shotSound.play()
        bullet = Bullet(self.game, self.centerX, self.borderBottom + 10, self.centerX, self.game.screenHeight, 100, owner=self, tile=self.bulletTile, damage=self.damage)
        self.game.gameObjects.append(bullet)
        self.currentTick = self.shotRateTick
    
    def die(self):
        # Creates animated Explosion object at the
        # same positions as enemy was
        self.game.blowSound.play()
        explosion = Explosion(self.game, self.x, self.y, self.width, self.height, self.game.explosionFrames, 5)
        self.game.gameObjects.append(explosion)
        # Removes Enemy object from objects list
        Character.die(self)
        self.game.score += self.score

    def update(self):
        # if self.healthPoints <= 0:
            # self.die()
        # if self.y == self.game.screenHeight:
            # self.game.end()
        self.draw()
        # self.shoot()
        # self.move(0, self.velocity)        
    
    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)