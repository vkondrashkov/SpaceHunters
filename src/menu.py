import pygame

from src.config import config
from src.menuItem import MenuItem

class Menu:
    font = pygame.font.Font(None, 48)

    @property
    def application(self):
        return self.__application

    def __init__(self, application):
        self.__application = application
        self.menuItems = []
        backgroundImage = pygame.image.load("src/tiles/menuBackground.png")
        self.background = pygame.transform.scale(backgroundImage, self.application.resolution)

        # Generating title and all the menu buttons
        self.titleString = "SpaceHunters"
        titleWidth, titleHeight = self.font.size(self.titleString)
        # Actually title X and Y coordinate
        # Store title offsets to display it later
        self.titleVerticalOffset = (self.application.screenHeight // 3)
        self.titleHorizontalOffset = (self.application.screenWidth // 2) - (titleWidth // 2)
        self.titleVerticalBorders = range(int(self.titleVerticalOffset), int(self.titleVerticalOffset + titleHeight))
        self.titleHorizontalBorders = range(int(self.titleHorizontalOffset), int(self.titleHorizontalOffset + titleWidth))
        
        startString = "Start"
        startWidth, startHeight = self.font.size(startString)
        # Actually start button X and Y coordinate
        startVerticalOffset = self.titleVerticalOffset + titleHeight + 50
        startHorizontalOffset = (self.application.screenWidth // 2) - (startWidth // 2)
        self.startVerticalBorders = range(int(startVerticalOffset), int(startVerticalOffset + startHeight))
        self.startHorizontalBorders = range(int(startHorizontalOffset), int(startHorizontalOffset + startWidth))
        self.startButton = MenuItem(self.application.display, startHorizontalOffset, startVerticalOffset, startString, None)

        tutorialString = "Tutorial"
        tutorialWidth, tutorialHeight = self.font.size(tutorialString)
        # Actually tutorial button X and Y coordinate
        tutorialVerticalOffset = startVerticalOffset + startHeight + 20
        tutorialHorizontalOffset = (self.application.screenWidth // 2) - (tutorialWidth // 2)
        self.tutorialVerticalBorders = range(int(tutorialVerticalOffset), int(tutorialVerticalOffset + tutorialHeight))
        self.tutorialHorizontalBorders = range(int(tutorialHorizontalOffset), int(tutorialHorizontalOffset + tutorialWidth))
        self.tutorialButton = MenuItem(self.application.display, tutorialHorizontalOffset, tutorialVerticalOffset, tutorialString, None)

        exitString = "Exit"
        exitWidth, exitHeight = self.font.size(exitString)
        # Actually exit button X and Y coordinate
        exitVerticalOffset = tutorialVerticalOffset + tutorialHeight + 20
        exitHorizontalOffset = (self.application.screenWidth / 2) - (exitWidth // 2)
        self.exitVerticalBorders = range(int(exitVerticalOffset), int(exitVerticalOffset + exitHeight))
        self.exitHorizontalBorders = range(int(exitHorizontalOffset), int(exitHorizontalOffset + exitWidth))
        self.exitButton = MenuItem(self.application.display, exitHorizontalOffset, exitVerticalOffset, exitString, None)

        self.menuItems.append(self.startButton)
        self.menuItems.append(self.tutorialButton)
        self.menuItems.append(self.exitButton)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.startButton.isSelected = False
                self.tutorialButton.isSelected = False
                self.exitButton.isSelected = False
                if event.type == pygame.QUIT:
                    exit()

                (mouseX, mouseY) = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouseX in self.startHorizontalBorders and mouseY in self.startVerticalBorders:
                        self.start()
                    if mouseX in self.tutorialHorizontalBorders and mouseY in self.tutorialVerticalBorders:
                        self.tutorial()
                    if mouseX in self.exitHorizontalBorders and mouseY in self.exitVerticalBorders:
                        self.exit()

                if mouseX in self.startHorizontalBorders and mouseY in self.startVerticalBorders:
                    self.startButton.isSelected = True
                if mouseX in self.tutorialHorizontalBorders and mouseY in self.tutorialVerticalBorders:
                    self.tutorialButton.isSelected = True
                if mouseX in self.exitHorizontalBorders and mouseY in self.exitVerticalBorders:
                    self.exitButton.isSelected = True
                
            self.draw()
            pygame.display.update()
            clock.tick(config["game"]["fps"])
    
    def tutorial(self):
        clock = pygame.time.Clock()
        tutorialScreenTicks = 240
        tutorial = pygame.image.load("src/tiles/tutorial.png")
        imageWidth = int(self.application.screenWidth * 0.75)
        imageHeight = int(imageWidth * 0.75)
        tutorialTile = pygame.transform.scale(tutorial, (imageWidth, imageHeight))
        horizontalPosition = (self.application.screenWidth - imageWidth) // 2
        verticalPosition = (self.application.screenHeight - imageHeight) // 2
        while tutorialScreenTicks > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    tutorialScreenTicks = 0
            self.application.display.fill((0, 0, 0))
            self.application.display.blit(tutorialTile, (horizontalPosition, verticalPosition))
            tutorialScreenTicks -= 1
            pygame.display.update()
            clock.tick(config["game"]["fps"])
    
    def start(self):
        self.application.game.start()

    def exit(self):
        self.running = False

    def draw(self):
        self.application.display.blit(self.background, (0, 0))
        title = self.font.render(self.titleString, False, (250, 250, 250))
        self.application.display.blit(title, (self.titleHorizontalOffset, self.titleVerticalOffset))
        for menuItem in self.menuItems:
            menuItem.draw()