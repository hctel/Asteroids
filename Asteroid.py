import pygame

class Asteroid:
    def __init__(self, size, pos, speed):
        self.__size = size
        self.__pos = pos
        self.__speed = speed
        self.__size = size
        
    def draw(self, screen):
        self.__screen = screen 
        pygame.draw.circle(screen, (255,255,255), self.__pos, self.__size)
        pygame.draw.circle(screen, (0,0,0), self.__pos, self.__size-2)
        self.__pos = (self.__pos[0] + self.__speed[0] * (1/60) , self.__pos[1] + self.__speed[1] * (1/60))
        if self.__pos[0] > 800:
            self.__pos = (0, self.__pos[1])
        if self.__pos[0] < 0:
            self.__pos = (800, self.__pos[1])
        if self.__pos[1] < 0:
            self.__pos = (self.__pos[0], 600)
        if self.__pos[1] > 600:
            self.__pos = (self.__pos[0], 0)