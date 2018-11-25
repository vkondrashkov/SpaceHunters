from src.character import Character
from src.config import config
from src.bullet import Bullet

class Player(Character):
    def __init__(self, game, 
                x=(config["game"]["resolution"]["width"] - config["player"]["width"]) / 2, 
                y=config["game"]["resolution"]["height"] - config["player"]["height"] - 100, 
                width=config["player"]["width"], 
                height=config["player"]["height"], 
                color=config["colors"]["green"], 
                velocity=config["player"]["velocity"], 
                healthPoints=config["player"]["healthPoints"], 
                damage=config["player"]["damage"], 
                bulletsPerShot=config["player"]["bulletsPerShot"]):
        Character.__init__(self, game, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot)

    def shoot(self):
        bullet = Bullet(self.game, self.centerX, self.y - 10, self.centerX, 0, 100, owner=self)
        self.game.gameObjects.append(bullet)

    def move(self, deltaX, deltaY):
        Character.move(self, deltaX, deltaY)
         
        screenBounds = config["game"]["resolution"]["height"] / 2
        if self.y <= screenBounds and deltaY < 0:
            self.y = screenBounds