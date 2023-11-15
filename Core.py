import pygame
import pygame_gui
import sys
from Player import *

class Ball:
    def __init__(self, pos, radius):
        self.__pos = pos
        self.__radius = radius

    def set_pos(self, pos):
        self.__pos = pos

    def set_radius(self, radius):
        self.__radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.__pos, self.__radius)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((800, 600))


player = Player((400,300))

while True:
    
    time_delta = clock.tick(240)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rotateCW()
            elif event.key == pygame.K_RIGHT:
                player.rotateCCW()
            elif event.key == pygame.K_UP:
                player.accelFW()
            elif event.key == pygame.K_DOWN:
                player.accelBW()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stopRotate()
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.stopAccel()

      
        manager.process_events(event)


    manager.update(time_delta/1000)

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))

    manager.draw_ui(screen)
    player.draw(screen)
    pygame.display.flip()