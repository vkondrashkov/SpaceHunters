import pygame

from src.config import config
from src.game import Game
from src.menu import Menu

class Application:

    @property
    def screenWidth(self):
        return self.__screenWidth
    
    @property
    def screenHeight(self):
        return self.__screenHeight
    
    @property
    def resolution(self):
        return (self.screenWidth, self.screenHeight)

    @property
    def display(self):
        return self.__display
    
    @property
    def caption(self):
        return self.__caption

    def __init__(self):
        self.__screenWidth = config["game"]["width"]
        self.__screenHeight = config["game"]["height"]
        self.__caption = config["game"]["caption"]
        display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.caption)
        self.__display = display
        

    def run(self):
        self.game = Game(self)
        self.menu = Menu(self)
        self.menu.run()
    

if __name__ == "__main__":
    app = Application()
    app.run()