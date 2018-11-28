import pygame

from src.drawable import Drawable

class Explosion(Drawable):
    @property
    def frames(self):
        return self.__frames

    @property
    def tick(self):
        return self.__tick

    def __init__(self,
                game,
                x,
                y,
                width,
                height,
                frames,
                tick):
        Drawable.__init__(self, game, x, y, int(width * 1.25), int(height * 1.25))
        self.__frames = frames
        self.__tick = tick
        self.currentTick = 0
    
    def update(self):
        self.currentTick += 1
        self.draw()
    
    def draw(self):
        index = self.currentTick // self.tick
        if index == len(self.frames):
            self.game.deleteEntity(self)
            return
        scaledTile = pygame.transform.scale(self.frames[index], (self.width, self.height))
        self.game.display.blit(scaledTile, (self.x, self.y))