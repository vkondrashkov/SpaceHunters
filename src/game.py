import pygame
from random import randint

from src.config import config
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy

pygame.init()

class Game:
    gameFont = pygame.font.Font(None, 30)
    gameObjects = []
    background = pygame.image.load("background.png")
    hpTile = pygame.image.load("playerHP.png")

    @property
    def display(self):
        return self.__display
    
    @property
    def screenWidth(self):
        return self.__screenWidth

    @property
    def screenHeight(self):
        return self.__screenHeight
    
    @property
    def resolution(self):
        return (self.screenWidth, self.screenHeight)

    def __init__(self):
        self.__screenWidth = config["game"]["width"]
        self.__screenHeight = config["game"]["height"]
        self.background = pygame.transform.scale(self.background, self.resolution)

        display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(config["game"]["caption"])

        self.__display = display
        self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
        self.difficultyTick = 60

    def start(self):
        self.running = True

        clock = pygame.time.Clock()
        player = Player(self)
        self.gameObjects.append(player)

        while self.running:
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
                if keys[pygame.K_SPACE]:
                    player.shoot()
            if self.spawnEnemyTick > 0:
                self.spawnEnemyTick -= 1
            else:
                x = randint(0, self.screenWidth - config["enemy"]["width"])
                y = 0
                self.gameObjects.append(Enemy(self, x, y, target=player))
                self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
            if self.difficultyTick > 0:
                self.difficultyTick -= 1
            else:
                self.difficultyTick = 60
            self.display.blit(self.background, (0, 0))
            player.move(deltaX, deltaY)
            for object in self.gameObjects:
                object.update()
            self.displayStats(player)
            pygame.display.update()
            clock.tick(config["game"]["fps"])

    def displayStats(self, player):
        if player.healthPoints > 5:
            hpString = str(player.healthPoints) + "x"
            textWidth, _ = self.gameFont.size(hpString)
            healthPointsString = self.gameFont.render(hpString, False, (250, 250, 250))
            self.display.blit(healthPointsString, (10, self.screenHeight - 25))
            self.display.blit(self.hpTile, (15 + textWidth, self.screenHeight - 30))
        else:
            for i in range(0, player.healthPoints):
                self.display.blit(self.hpTile, (10 + i*35, self.screenHeight - 30))

    def end(self):
        self.running = False
        self.gameObjects = []

    def deleteEntity(self, obj):
        self.gameObjects.remove(obj)
            