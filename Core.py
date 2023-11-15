import pygame
import pygame_gui
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

manager = pygame_gui.UIManager((800, 600))

while True:
    # tick renvoie le temps écoulé depuis le dernier tick (en ms)
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # permet à pygame_gui de recevoir les events
        manager.process_events(event)

    # permet à pygame_gui de mettre à jour les animations (en s)
    manager.update(time_delta/1000)

    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))

    # affiche les widgets
    manager.draw_ui(screen)

    pygame.display.flip()