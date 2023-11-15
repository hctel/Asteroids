import pygame
from math import sin,cos
class Bullet:
    
    def __init__(self, pos, angle, speed, lifetime):
        self.__pos = pos
        self.__angle = angle
        self.__speed = speed
        self.__lifetime = lifetime
        self.__age = 0 
        self.__size = 4
    
    def draw(self, screen):
        if self.__age < self.__lifetime:
            self.__screen = screen 
            pygame.draw.circle(screen, (255,255,255), self.__pos, self.__size)
            self.__pos = (self.__pos[0] + self.__speed * (1/60) * cos(self.__angle) , self.__pos[1] + self.__speed * (1/60) * sin(self.__angle))
            if self.__pos[0] > 800:
                self.__pos = (0, self.__pos[1])
            if self.__pos[0] < 0:
                self.__pos = (800, self.__pos[1])
            if self.__pos[1] < 0:
                self.__pos = (self.__pos[0], 600)
            if self.__pos[1] > 600:
                self.__pos = (self.__pos[0], 0)
           
            self.__age += 1
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