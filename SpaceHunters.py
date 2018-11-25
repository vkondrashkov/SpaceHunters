import pygame

from src.config import config
from src.game import Game

def main():
    configResolution = config["game"]["resolution"]
    resolution = (configResolution["width"], configResolution["height"])
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption(config["game"]["caption"])
    
    game = Game(display)
    game.start()

if __name__ == "__main__":
    main()