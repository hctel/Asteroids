import pygame

class Asteroid:
    def __init__(self, size, pos, speed, surface):
        self.__size = size
        self.__pos = pos
        self.__speed = speed
        self.__size = size
        self.__surface = surface
        
    def draw(self, screen):
        self.__screen = screen 
        pygame.draw.circle(screen, (255,255,255), self.__pos, self.__size, 1)
        self.__pos = (self.__pos[0] + self.__speed[0]*0.06 , self.__pos[1] + self.__speed[1]*0.06)
        if self.__pos[0] > self.__surface.get_width():
            self.__pos = (0, self.__pos[1])
        if self.__pos[0] < 0:
            self.__pos = (self.__surface.get_width(), self.__pos[1])
        if self.__pos[1] < 0:
            self.__pos = (self.__pos[0], self.__surface.get_height())
        if self.__pos[1] > self.__surface.get_height():
            self.__pos = (self.__pos[0], 0)
            
    def getPosX(self):
        return self.__pos[0]
    def getPosY(self):
        return self.__pos[1]
    def getRadius(self):
        return self.__size