from abc import ABCMeta, abstractmethod

class Object:
    __metaclass__ = ABCMeta

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

    @abstractmethod
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height