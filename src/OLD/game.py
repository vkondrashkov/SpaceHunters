import pygame

from src.config import config
from src.player import Player

class Game:
    def __init__(self, display):
        self.display = display

    def start(self):
        clock = pygame.time.Clock()
        player = Player(self.display)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                deltaX = 0
                deltaY = 0
                keys = pygame.key.get_pressed()
                velocity = config["player"]["velocity"]
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    deltaX = -velocity
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    deltaX = velocity
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    deltaY = -velocity
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    deltaY = velocity
            self.display.fill(config["colors"]["black"])
            player.move(deltaX, deltaY)
            player.draw()
            pygame.display.update()
            clock.tick(config["game"]["fps"])

            