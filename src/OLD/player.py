from src.character import Character
from src.config import config

class Player(Character):
    def __init__(self, display, 
                x=(config["game"]["resolution"]["width"] - config["player"]["width"]) / 2, 
                y=config["game"]["resolution"]["height"] - config["player"]["height"] - 100, 
                width=config["player"]["width"], 
                height=config["player"]["height"], 
                color=config["colors"]["green"], 
                velocity=config["player"]["velocity"], 
                healthPoints=config["player"]["healthPoints"], 
                damage=config["player"]["damage"], 
                bulletsPerShot=config["player"]["bulletsPerShot"]):
        Character.__init__(self, display, x, y, 
                                width, height, color, 
                                velocity, healthPoints, 
                                damage, bulletsPerShot)