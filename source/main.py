import pygame, sys
from Quoridor import Quoridor

pygame.init()
print("hola")

size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Quoridor")
clock = pygame.time.Clock() # no  usar para medir los tiempos en el algortimo.

quoridor = Quoridor(size, 9, 4)

while True:
    quoridor.render(screen, size)
    pygame.display.flip()
    quoridor.update()
    for event in pygame.event.get():
        quoridor.event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
