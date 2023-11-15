import pygame
from math import sin,cos

class Player:
    def __init__(self, pos):
       self.__pos = pos
       self.__speed = (0,0)
       self.__rot = 0
       self.__rotate = 0 
       self.__accel = 1
        
    def draw(self, screen):
        self.__screen = screen 
        pygame.draw.polygon(screen, (255,255,255), ((7.5*cos(2.09439510239+self.__rot)+self.__pos[0],7.5*sin(2.09439510239+self.__rot)+self.__pos[1]), (7.5*cos(4.18879020479+self.__rot)+self.__pos[0],7.5*sin(4.18879020479+self.__rot)+self.__pos[1]), (10*cos(self.__rot)+self.__pos[0],10*sin(self.__rot)+self.__pos[1])))
        pygame.draw.polygon(screen, (0,0,0), ((5*cos(2.61799+self.__rot)+self.__pos[0],5*sin(2.61799+self.__rot)+self.__pos[1]), (5*cos(3.66519+self.__rot)+self.__pos[0],5*sin(3.66519+self.__rot)+self.__pos[1]), (7*cos(self.__rot)+self.__pos[0],7*sin(self.__rot)+self.__pos[1])))
        
        
        self.__pos = (self.__pos[0] + self.__speed[0] * (1/60) , self.__pos[1] + self.__speed[1] * (1/60))
        
        
        if self.__pos[0] > 800:
            self.__pos = (0, self.__pos[1])
        if self.__pos[0] < 0:
            self.__pos = (800, self.__pos[1])
        if self.__pos[1] < 0:
            self.__pos = (self.__pos[0], 600)
        if self.__pos[1] > 600:
            self.__pos = (self.__pos[0], 0)
            
            
        if self.__rotate == 1:
            self.__rot -= 0.05
        elif self.__rotate == -1:
            self.__rot += 0.05
            
        if self.__accel == 1:
            self.__speed = (self.__speed[0] + 5*(1/60)*cos(self.__rot), self.__speed[1] + 5*(1/60)*sin(self.__rot))
        if self.__accel == -1:
            self.__speed = (self.__speed[0] - 5*(1/60)*cos(self.__rot), self.__speed[1] - 5*(1/60)*sin(self.__rot))   
            
    def rotateCW(self):
        self.__rotate = 1
        self.__rot -= 0.05
    def rotateCCW(self):
        self.__rotate = -1
        self.__rot += 0.05
        
    def accelFW(self):
        self.__accel = 1
    def accelBW(self):
        self.__accel = -1
        
    def stopRotate(self):
        self.__rotate = 0
    def stopAccel(self):
        self.__accel = 0