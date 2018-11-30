import pygame

class MenuItem:
    font = pygame.font.Font(None, 48)

    @property
    def display(self):
        return self.__display
    
    @property
    def text(self):
        return self.__text

    def __init__(self, display, x, y, text, command):
        self.menuTile = pygame.image.load("src/tiles/menuItemBackground.png")
        self.x = x
        self.y = y
        self.__display = display
        self.__text = text
        self.execute = command
        self.isSelected = False

    # Method doesn't contain any body because
    # every Menu button has its own behavior
    def execute(self):
        pass

    def draw(self):
        color = None
        if self.isSelected == False:
            color = (250, 250, 250)
        else:
            # Calculates position and size of
            # background image for Menu button
            # according to the center of 
            # selected button's text.
            scaledTile = pygame.transform.scale(self.menuTile, (220, 48))
            width, height = scaledTile.get_rect().size
            menuTextWidth, _ = self.font.size(self.text)
            centerMenuText = (menuTextWidth // 2) + self.x
            x = centerMenuText - (width // 2)
            y = self.y - 10
            self.display.blit(scaledTile, (x, y))
            color = (54, 187, 245)
        menuItemText = self.font.render(self.text, False, color)
        self.display.blit(menuItemText, (self.x, self.y))