import pygame
from random import randint
from math import pi,cos,sin

class Asteroid:
    def __init__(self, size, pos, speed, surface):
        self.__size = size
        self.__pos = pos
        self.__speed = speed
        self.__size = size
        self.__surface = surface
        self.__notFrozen = 1
        self.__circle = True
    
    def setPolygon(self, sides):
        self.__circle = False
        self.__sides = sides
        self.__radiuses = [randint(self.__size/2,self.__size) for n in range(sides)]
        self.__angles = [n/(2*pi) for n in range(sides)]
        return self
            
    def __getPos(self):  
        a = []
        for n in range(self.__sides):  
            a.append(((self.__radiuses[n]*cos(self.__angles[n])+self.__pos[0]), 
                (self.__radiuses[n]*sin(self.__angles[n])+self.__pos[1])))
        return a
    def draw(self, screen):
        self.__screen = screen 
        if self.__circle:
            pygame.draw.circle(screen, (255,255,255), self.__pos, self.__size, 1)
        else:
            pygame.draw.polygon(screen, (255,255,255),  self.__getPos(), 1)
        self.__pos = (self.__pos[0] + self.__notFrozen*self.__speed[0]*0.06 , self.__pos[1] + self.__notFrozen*self.__speed[1]*0.06)
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
    def freeze(self):
        self.__notFrozen = 0
    def unFreeze(self):
        self.__notFrozen = 1