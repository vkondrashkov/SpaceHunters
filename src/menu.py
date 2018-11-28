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

        optionsString = "Options"
        optionsWidth, optionsHeight = self.font.size(optionsString)
        # Actually options button X and Y coordinate
        optionsVerticalOffset = startVerticalOffset + startHeight + 20
        optionsHorizontalOffset = (self.application.screenWidth // 2) - (optionsWidth // 2)
        self.optionsVerticalBorders = range(int(optionsVerticalOffset), int(optionsVerticalOffset + optionsHeight))
        self.optionsHorizontalBorders = range(int(optionsHorizontalOffset), int(optionsHorizontalOffset + optionsWidth))
        self.optionsButton = MenuItem(self.application.display, optionsHorizontalOffset, optionsVerticalOffset, optionsString, None)

        exitString = "Exit"
        exitWidth, exitHeight = self.font.size(exitString)
        # Actually exit button X and Y coordinate
        exitVerticalOffset = optionsVerticalOffset + optionsHeight + 20
        exitHorizontalOffset = (self.application.screenWidth / 2) - (exitWidth // 2)
        self.exitVerticalBorders = range(int(exitVerticalOffset), int(exitVerticalOffset + exitHeight))
        self.exitHorizontalBorders = range(int(exitHorizontalOffset), int(exitHorizontalOffset + exitWidth))
        self.exitButton = MenuItem(self.application.display, exitHorizontalOffset, exitVerticalOffset, exitString, None)

        self.menuItems.append(self.startButton)
        self.menuItems.append(self.optionsButton)
        self.menuItems.append(self.exitButton)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.startButton.isSelected = False
                self.optionsButton.isSelected = False
                self.exitButton.isSelected = False
                if event.type == pygame.QUIT:
                    exit()

                (mouseX, mouseY) = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouseX in self.startHorizontalBorders and mouseY in self.startVerticalBorders:
                        self.start()
                    if mouseX in self.optionsHorizontalBorders and mouseY in self.optionsVerticalBorders:
                        self.options()
                    if mouseX in self.exitHorizontalBorders and mouseY in self.exitVerticalBorders:
                        self.exit()

                if mouseX in self.startHorizontalBorders and mouseY in self.startVerticalBorders:
                    self.startButton.isSelected = True
                if mouseX in self.optionsHorizontalBorders and mouseY in self.optionsVerticalBorders:
                    self.optionsButton.isSelected = True
                if mouseX in self.exitHorizontalBorders and mouseY in self.exitVerticalBorders:
                    self.exitButton.isSelected = True
                
            self.draw()
            pygame.display.update()
            clock.tick(config["game"]["fps"])
    
    def options(self):
        pass
    
    def start(self):
        self.running = False
        self.application.game.start()

    def exit(self):
        exit()

    def draw(self):
        self.application.display.fill((0, 0, 0))
        title = self.font.render(self.titleString, False, (250, 250, 250))
        self.application.display.blit(title, (self.titleHorizontalOffset, self.titleVerticalOffset))
        for menuItem in self.menuItems:
            menuItem.draw()