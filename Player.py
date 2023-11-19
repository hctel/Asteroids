import pygame
from math import sin,cos,sqrt
from pygame import mixer
from Bullet import *

class Player:
    def __init__(self, pos, surface):
        self.__pos = pos
        self.__speed = (1,1)
        self.__vmax = 750
        self.__rot = 0
        self.__rotate = 0 
        self.__accel = 0
        self.__accelRate = 8.5
        self.__maxRotateRate = 7.5
        self.__rotateAccel = 1.25
        self.__rotateDecel = 0.7
        self.__rotateSpeed = 0
        self.__surface = surface
        mixer.init()
        mixer.music.load("brr.wav")
        mixer.music.set_volume(.5)
        self.__pew = mixer.Sound("pew.mp3")
        
    def draw(self, screen):
        self.__screen = screen 
        
        pygame.draw.polygon(screen, (255,255,255), ((7.5*cos(2.61799+self.__rot)+self.__pos[0],7.5*sin(2.61799+self.__rot)+self.__pos[1]), (7.5*cos(3.66519+self.__rot)+self.__pos[0],7.5*sin(3.66519+self.__rot)+self.__pos[1]), (10*cos(self.__rot)+self.__pos[0],10*sin(self.__rot)+self.__pos[1])), 1)
        
        self.__pos = (self.__pos[0] + self.__speed[0] * (1/60) , self.__pos[1] + self.__speed[1] * (1/60))
        
        
        if self.__pos[0] > self.__surface.get_width():
            self.__pos = (0, self.__pos[1])
        if self.__pos[0] < 0:
            self.__pos = (self.__surface.get_width(), self.__pos[1])
        if self.__pos[1] < 0:
            self.__pos = (self.__pos[0], self.__surface.get_height())
        if self.__pos[1] > self.__surface.get_height():
            self.__pos = (self.__pos[0], 0)
            
            
        self.__rot = self.__rot + self.__rotateSpeed*(1/60)
            
        prev_speed = self.__speed
        self.__speed = (self.__speed[0] + self.__accelRate*self.__accel*cos(self.__rot), self.__speed[1] + self.__accelRate*self.__accel*sin(self.__rot))
        if self.__speed[0] > self.__vmax or self.__speed[0] < -self.__vmax:
            self.__speed = (prev_speed[0], self.__speed[1])
        if self.__speed[1] > self.__vmax or self.__speed[1] < -self.__vmax:
            self.__speed = (self.__speed[0], prev_speed[1])
        
        if self.__rotate == 0:
            if self.__rotateSpeed > 0:
                self.__rotateSpeed = self.__rotateSpeed + self.__rotateDecel*(-1)*self.__rotateSpeed/6.5
            elif self.__rotateSpeed < 0:
                self.__rotateSpeed = self.__rotateSpeed + self.__rotateDecel*(1)*abs(self.__rotateSpeed)/6.5
            
        prev_rotateSpeed = self.__rotateSpeed
        self.__rotateSpeed = self.__rotateSpeed + self.__rotateAccel*self.__rotate
        if self.__rotateSpeed > self.__maxRotateRate or self.__rotateSpeed < -self.__maxRotateRate:
            self.__rotateSpeed = prev_rotateSpeed
            
    def rotateCW(self):
        self.__rotate = -1
        self.__rot -= 0.05
    def rotateCCW(self):
        self.__rotate = +1
        self.__rot += 0.05
        
    def accelFW(self):
        self.__accel = 1
        mixer.music.play(loops=-1, start=0_0, fade_ms=0)
    def accelBW(self):
        self.__accel = -1
        mixer.music.play(loops=-1, start=0_0, fade_ms=0)
        
    def stopRotate(self):
        self.__rotate = 0
    def stopAccel(self):
        self.__accel = 0
        mixer.music.stop()
        
    def shoot(self):
        self.__pew.play()
        return Bullet(self.__pos, self.__rot, 0.005*self.totalSpeed+10, 100, self.__surface)
    
    def getPosX(self):
        return self.__pos[0]
    def getPosY(self):
        return self.__pos[1]
      
    def getSpeed(self):
        return self.__rotateSpeed
      
    @property    
    def totalSpeed(self):
        return sqrt(self.__speed[0]**2 + self.__speed[1]**2)