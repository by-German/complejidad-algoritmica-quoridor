import pygame
from Quoridor import Quoridor

pygame.init()

size = (600, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock() # no  usar para medir los tiempos en el algortimo.

quoridor = Quoridor(size, 27, 4)

while True:
    for event in pygame.event.get():
        # quoridor.event_key(event)
        if event.type == pygame.QUIT:
            pygame.quit()
    quoridor.render(screen, size)
    pygame.display.flip()
    quoridor.update()



