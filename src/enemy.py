from src.character import Character
from src.drawable import Drawable
from src.bullet import Bullet
from src.config import config

class Enemy(Character):
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
        self.target = target
        self.shootRateTick = 30

    def shoot(self):
        if self.shootRateTick > 0:
            self.shootRateTick -= 1
            return
        bullet = Bullet(self.game, self.centerX, self.borderBottom + 10, self.target.centerX, self.target.centerY, 100, owner=self)
        self.game.gameObjects.append(bullet)
        self.shootRateTick = 120

    def draw(self):
        Drawable.draw(self)
        self.shoot()
        self.move(0, config["enemy"]["velocity"])
    
    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)