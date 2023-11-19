import pygame
from math import sin,cos
class Bullet:
    
    def __init__(self, pos, angle, speed, lifetime, surface):
        self.__pos = pos
        self.__angle = angle
        self.__speed = speed
        self.__lifetime = lifetime
        self.__age = 0 
        self.__size = 2
        self.__surface = surface
    
    def draw(self, screen):
        if self.__age < self.__lifetime:
            self.__screen = screen 
            pygame.draw.circle(screen, (255,255,255), self.__pos, self.__size)
            self.__pos = (self.__pos[0] + self.__speed * cos(self.__angle) , self.__pos[1] + self.__speed * sin(self.__angle))
        if self.__pos[0] > self.__surface.get_width():
            self.__pos = (0, self.__pos[1])
        if self.__pos[0] < 0:
            self.__pos = (self.__surface.get_width(), self.__pos[1])
        if self.__pos[1] < 0:
            self.__pos = (self.__pos[0], self.__surface.get_height())
        if self.__pos[1] > self.__surface.get_height():
            self.__pos = (self.__pos[0], 0)          
        self.__age += 1
            
        return self.__age < self.__lifetime
    def getPosX(self):
        if self.__age < self.__lifetime:
            return self.__pos[0]
        else:
            return -100
    def getPosY(self):
        if self.__age < self.__lifetime:
            return self.__pos[1]
        else:
            return -100