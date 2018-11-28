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
    playerTile = pygame.image.load("player.png")
    enemyTile = pygame.image.load("enemy.png")
    shotSound = pygame.mixer.Sound("shotSound.wav")
    blowSound = pygame.mixer.Sound("blowSound.wav")
    playerShotTile = pygame.image.load("playerShot.png")
    enemyShotTile = pygame.image.load("enemyShot.png")
    score = 0

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
    
    @property
    def caption(self):
        return self.__caption
    
    def loadConfig(self):
        self.__screenWidth = config["game"]["width"]
        self.__screenHeight = config["game"]["height"]
        backgroundImage = pygame.image.load("background.png")
        self.background = pygame.transform.scale(backgroundImage, self.resolution)
        self.__caption = config["game"]["caption"]
        self.hpTile = pygame.image.load("playerHP.png")
        self.playerTile = pygame.image.load("player.png")
        self.enemyTile = pygame.image.load("enemy.png")
        self.shotSound = pygame.mixer.Sound("shotSound.wav")
        self.blowSound = pygame.mixer.Sound("blowSound.wav")
        self.playerShotTile = pygame.image.load("playerShot.png")
        self.enemyShotTile = pygame.image.load("enemyShot.png")
        self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
        self.difficultyTick = 60

    def __init__(self):
        self.loadConfig()
        display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.caption)

        self.__display = display
        

    def start(self):
        self.running = True

        clock = pygame.time.Clock()
        player = Player(self,
                        x=(config["game"]["width"] - config["player"]["width"]) / 2, 
                        y=config["game"]["height"] - config["player"]["height"] - 100, 
                        width=config["player"]["width"], 
                        height=config["player"]["height"], 
                        velocity=config["player"]["velocity"], 
                        healthPoints=config["player"]["healthPoints"], 
                        damage=config["player"]["damage"], 
                        bulletsPerShot=config["player"]["bulletsPerShot"],
                        tile=self.playerTile,
                        bulletTile=self.playerShotTile)
        self.gameObjects.append(player)

        pygame.mixer.music.load("backgroundMusic.wav")
        pygame.mixer.music.play(-1)
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
            self.cycleSpawnEnemy()
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
        scoreString = "Score: " + str(self.score)
        scoreStringWidth, _ = self.gameFont.size(scoreString)
        score = self.gameFont.render(scoreString, False, (250, 250, 250))
        self.display.blit(score, (self.screenWidth - scoreStringWidth - 10, self.screenHeight - 25))
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
    
    def cycleSpawnEnemy(self):
        if self.spawnEnemyTick > 0:
            self.spawnEnemyTick -= 1
        else:
            x = randint(0, self.screenWidth - config["enemy"]["width"])
            y = 0
            self.gameObjects.append(Enemy(self, 
                                        x=x, 
                                        y=y, 
                                        width=config["enemy"]["width"], 
                                        height=config["enemy"]["height"], 
                                        velocity=config["enemy"]["velocity"], 
                                        healthPoints=config["enemy"]["healthPoints"], 
                                        damage=config["enemy"]["damage"], 
                                        bulletsPerShot=config["enemy"]["bulletsPerShot"],
                                        tile=self.enemyTile,
                                        bulletTile=self.enemyShotTile,
                                        score=config["enemy"]["score"]))
            self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
    
