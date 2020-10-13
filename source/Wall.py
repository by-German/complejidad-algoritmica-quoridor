import pygame

class Wall:
    def __init__(self, tam):
        self.tam = tam
        self.x = 0
        self.y = 0

    def event(self, event):
        self.set_position(event)
    
    def draw(self, screen, color, horizontal = True):
        # ver como detectar el x e y.
        # parametros(x, y, ancho, alto)
        div_ancho, div_alto = 1, 1
        if horizontal: div_alto = 4    
        else: div_alto = 4
        pygame.draw.rect(screen, color, (self.x, self.y, self.tam / div_ancho, self.tam / div_alto))

    def update(self):
        pass    

    def set_position(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            self.x, self.y = mx, my
            print(self.x, self.y)
