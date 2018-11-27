from abc import ABCMeta, abstractmethod

class Object:
    __metaclass__ = ABCMeta

    @property
    def borderTop(self):
        return int(self.y)

    @property
    def borderBottom(self):
        return int(self.y + self.height)

    @property
    def borderLeft(self):
        return int(self.x)

    @property
    def borderRight(self):
        return int(self.x + self.width)

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

    @property
    def centerX(self):
        return self.x + self.__width / 2
    
    @property
    def centerY(self):
        return self.y + self.__height / 2

    @abstractmethod
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height
    
    @abstractmethod
    def update(self):
        pass