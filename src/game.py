import pygame
import socket as Socket
import json as JSON
from threading import Thread
from random import randint

from src.config import config
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.entities.bonus import Bonus
from src.entities.bonusType import BonusType

pygame.init()

class Game:

    @property
    def application(self):
        return self.__application

    @property
    def display(self):
        return self.application.display
    
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
    
    # Preloads all the necessary constants 
    # before game starts
    def loadConfig(self):
        self.gameFont = pygame.font.Font(None, 30)
        self.gameObjects = []
        self.difficultyGrade = 1
        self.score = 0
        self.explosionFrames = []
        self.bonusTiles = []

        self.__screenWidth = config["game"]["width"]
        self.__screenHeight = config["game"]["height"]
        self.__caption = config["game"]["caption"]
        self.difficultyTick = config["game"]["difficultyTick"]
        self.spawnEnemyTick = config["game"]["spawnEnemyTick"]

        backgroundImage = pygame.image.load("src/tiles/background.png")
        self.hpTile = pygame.image.load("src/tiles/playerHP.png")
        self.damageTile = pygame.image.load("src/tiles/playerDamage.png")
        self.player1Tile = pygame.image.load("src/tiles/player1.png")
        self.player2Tile = pygame.image.load("src/tiles/player2.png")
        self.enemyTile = pygame.image.load("src/tiles/enemy.png")
        self.enemyHPTile = pygame.image.load("src/tiles/enemyHP.png")
        self.enemyDamageTile = pygame.image.load("src/tiles/enemyDamage.png")
        self.playerShotTile = pygame.image.load("src/tiles/playerShot.png")
        self.enemyShotTile = pygame.image.load("src/tiles/enemyShot.png")
        self.bonusHealthTile = pygame.image.load("src/tiles/bonus_health.png")
        self.bonusDamageTile = pygame.image.load("src/tiles/bonus_damage.png")
        sheet = pygame.image.load("src/tiles/explosion.png")
        for i in range(0, 11):
            self.explosionFrames.append(sheet.subsurface(96*i, 0, 96, 96))
        self.bonusTiles.append(self.bonusHealthTile)
        self.bonusTiles.append(self.bonusDamageTile)

        pygame.mixer.music.load("src/sounds/backgroundMusic.wav")
        self.shotSound = pygame.mixer.Sound("src/sounds/shotSound.wav")
        self.blowSound = pygame.mixer.Sound("src/sounds/blowSound.wav")

        self.background = pygame.transform.scale(backgroundImage, self.resolution)

    def __init__(self, application):
        self.loadConfig()
        self.__application = application
    
    def __onRecieve(self):
        while self.running:
            try:
                response = self.__socket.recv(1024).decode("utf8")
                if not response:
                    pass # Error handling
                json = JSON.loads(response)

                # Creating and replacing old game objects list with new one
                # to avoid entities "blinking" if delete list and refill it.
                _gameObjects = []
                for entity in json:
                    if entity["entityType"] == "player":
                        playerTile = self.player2Tile
                        if entity["id"] == self.id:
                            playerTile = self.player1Tile
                        player = Player(self, 
                                        x=entity["x"], 
                                        y=entity["y"], 
                                        width=entity["width"], 
                                        height=entity["height"], 
                                        velocity=entity["velocity"], 
                                        healthPoints=entity["health"], 
                                        damage=entity["damage"],
                                        tile=playerTile,
                                        bulletTile=self.playerShotTile)
                        _gameObjects.append(player)
                self.gameObjects = _gameObjects
            except Exception:
                pass
        
    def start(self):
        self.running = True

        self.__socket = Socket.socket()
        self.__socket.connect(("spacehunters.local", 33000))
        self.id = self.__socket.recv(1024).decode("utf8")
        self.__recieveThread = Thread(target=self.__onRecieve)
        self.__recieveThread.start()

        self.gameObjects = []
        self.difficultyTick = config["game"]["difficultyTick"]
        self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
        self.spawnBonusTick = 240
        self.difficultyGrade = 1
        self.score = 0
        self.loop()
    
    def loop(self):
        clock = pygame.time.Clock()

        # Infinitely plays background music
        pygame.mixer.music.play(-1)
        
        moveUp = False
        moveDown = False
        moveLeft = False
        moveRight = False
        while self.running:
            # All events are temporary and needs to be changed!
            for event in pygame.event.get():
                # Resets delta's for any event
                # In case of "keyUp"
                moveUp = False
                moveDown = False
                moveLeft = False
                moveRight = False

                # Terminal exiting from game
                if event.type == pygame.QUIT:
                    self.running = False
                    self.__sendEvent("exit")
                    self.__socket.close()
                    self.__recieveThread.join()
                    exit()
                keys = pygame.key.get_pressed()
                velocity = config["player"]["velocity"]
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    moveLeft = True
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    moveRight = True
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    moveUp = True
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    moveDown = True
                if keys[pygame.K_SPACE]:
                    self.__sendEvent("shoot")
            
            if moveLeft:
                self.__sendEvent("move_left")
            if moveRight:
                self.__sendEvent("move_right")
            if moveUp:
                self.__sendEvent("move_up")
            if moveDown:
                self.__sendEvent("move_down")

            # Drawing all the objects
            # Firstly drawing characters and only then
            # drawing HUD (to avoid overlay)
            self.display.blit(self.background, (0, 0))
            #player.move(deltaX, deltaY)
            for object in self.gameObjects:
                object.update()
            #self.displayStats(player)
            pygame.display.update()

            clock.tick(config["game"]["fps"])

    def __sendEvent(self, event):
        request = {}
        request["event"] = event
        request["id"] = self.id
        self.__socket.send(JSON.dumps(request).encode("utf8"))

    def displayStats(self, player):
        # Displays current player's score
        scoreString = "Score: " + str(self.score)
        scoreStringWidth, scoreStringHeigt = self.gameFont.size(scoreString)
        score = self.gameFont.render(scoreString, False, (250, 250, 250))
        self.display.blit(score, (self.screenWidth - scoreStringWidth - 10, self.screenHeight - scoreStringHeigt - 5))
        
        # Displays current difficulty and sets
        # its position relatively to Score
        difficultyString = "Level: " + str(int(self.difficultyGrade))
        _, difficultyStringWidth = self.gameFont.size(difficultyString)
        difficulty = self.gameFont.render(difficultyString, False, (250, 250, 250))
        self.display.blit(difficulty, (self.screenWidth - scoreStringWidth - 10, self.screenHeight - scoreStringHeigt - 30))

        # Displays current enemy's HP and damage
        enemyHealthString = str(int(config["enemy"]["healthPoints"] + 2 * self.difficultyGrade)) + "x"
        enemyHealthWidth, enemyHealthHeight = self.gameFont.size(enemyHealthString)
        enemyHealth = self.gameFont.render(enemyHealthString, False, (250, 250, 250))
        self.display.blit(enemyHealth, (10, 15))
        self.display.blit(self.enemyHPTile, (enemyHealthWidth + 15, 10))
        enemyDamageString = str(int(config["enemy"]["damage"] * self.difficultyGrade))
        enemyDamageWidth, enemyDamageHeight = self.gameFont.size(enemyDamageString)
        enemyDamage = self.gameFont.render(enemyDamageString, False, (250, 250, 250))
        self.display.blit(enemyDamage, (10, enemyHealthHeight + 25))
        self.display.blit(self.enemyDamageTile, (enemyDamageWidth + 15, enemyHealthHeight + 20))

        # If player's health more than 5
        # simply displays it's like value (6x)
        # otherwise displays Player icons equals to HP
        if player.healthPoints > 5:
            hpString = str(player.healthPoints) + "x"
            textWidth, _ = self.gameFont.size(hpString)
            healthPointsString = self.gameFont.render(hpString, False, (250, 250, 250))
            self.display.blit(healthPointsString, (10, self.screenHeight - 25))
            self.display.blit(self.hpTile, (15 + textWidth, self.screenHeight - 30))
        else:
            for i in range(0, player.healthPoints):
                self.display.blit(self.hpTile, (10 + i*35, self.screenHeight - 30))
        damageString = str(player.damage)
        textWidth, _ = self.gameFont.size(damageString)
        damage = self.gameFont.render(damageString, False, (250, 250, 250))
        self.display.blit(damage, (10, self.screenHeight - 60))
        self.display.blit(self.damageTile, (15 + textWidth, self.screenHeight - 70))
    
    def end(self):
        self.running = False
        self.__sendEvent("exit")
        self.__socket.close()
        self.__recieveThread.join()

        pygame.mixer.music.stop()
        self.gameOverScreen()
        self.gameObjects = []
    
    def gameOverScreen(self):
        clock = pygame.time.Clock()
        gameOverScreenTicks = 240
        gameOver = pygame.image.load("src/tiles/gameOver.png")
        imageWidth = int(self.application.screenWidth * 0.75)
        imageHeight = imageWidth // 3
        gameOverTile = pygame.transform.scale(gameOver, (imageWidth, imageHeight))
        horizontalPosition = (self.application.screenWidth - imageWidth) // 2
        verticalPosition = (self.application.screenHeight - imageHeight) // 2
        while gameOverScreenTicks:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.display.fill((0, 0, 0))
            self.display.blit(gameOverTile, (horizontalPosition, verticalPosition))
            font = pygame.font.Font(None, 54)
            scoreString = "Score: " + str(self.score)
            scoreWidth, _ = font.size(scoreString)
            score = font.render(scoreString, False, (0, 92, 236))
            scoreHorizontalPosition = self.screenWidth // 2 - (scoreWidth // 2)
            self.display.blit(score, (scoreHorizontalPosition, imageHeight + 10))
            gameOverScreenTicks -= 1
            pygame.display.update()
            clock.tick(config["game"]["fps"])


    def deleteEntity(self, obj):
        self.gameObjects.remove(obj)
    
    def cycleSpawnEnemy(self):
        if self.spawnEnemyTick > 0:
            self.spawnEnemyTick -= 1
        else:
            # Generates random horizontal position
            # considering it's width to avoid generating
            # object beyond Screen borders.
            x = randint(0, self.screenWidth - config["enemy"]["width"])
            y = 0
            self.gameObjects.append(Enemy(self, 
                                        x=x, 
                                        y=y, 
                                        width=config["enemy"]["width"], 
                                        height=config["enemy"]["height"], 
                                        velocity=config["enemy"]["velocity"], 
                                        healthPoints=int(config["enemy"]["healthPoints"] + 2 * self.difficultyGrade), 
                                        damage=int(config["enemy"]["damage"] * self.difficultyGrade), 
                                        tile=self.enemyTile,
                                        bulletTile=self.enemyShotTile,
                                        score=int(config["enemy"]["score"] * self.difficultyGrade),
                                        shotRateTick=int(config["enemy"]["shotRateTick"] - (self.difficultyGrade * 5))))
            self.spawnEnemyTick = config["game"]["spawnEnemyTick"]
    
    def cycleDifficulty(self):
        if self.difficultyTick > 0:
            self.difficultyTick -= 1
        else:
            self.difficultyGrade += 0.25
            self.difficultyTick = config["game"]["difficultyTick"]
    
    def cyclePlayerShot(self, player):
        if player.shotTick > 0:
            player.shotTick -= 1
    
    def cycleSpawnBonus(self):
        if self.spawnBonusTick > 0:
            self.spawnBonusTick -= 1
        else:
            x = randint(0, self.screenWidth - 20)
            y = 0
            bonusChoice = randint(0, 1)
            bonusType = None
            value = 0
            if bonusChoice == 1:
                bonusType = BonusType.damage
                value = 1
            else:
                bonusType = BonusType.health
                value = 5
            self.gameObjects.append(Bonus(self,
                                        x=x,
                                        y=y,
                                        velocity=5,
                                        type=bonusType,
                                        value=value,
                                        tile=self.bonusTiles[bonusChoice]))
            self.spawnBonusTick = randint(240, 480)