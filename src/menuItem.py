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
        self.x = x
        self.y = y
        self.__display = display
        self.__text = text
        self.execute = command
        self.isSelected = False

    def execute(self):
        pass

    def draw(self):
        color = None
        if self.isSelected == False:
            color = (250, 250, 250)
        else:
            color = (250, 250, 0)
        menuItemText = self.font.render(self.text, False, color)
        self.display.blit(menuItemText, (self.x, self.y))