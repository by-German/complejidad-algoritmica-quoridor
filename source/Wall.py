import pygame

class Wall:
    def __init__(self, x, y, origen, fin, horizontal):
        self.x = x
        self.y = y
        self.origen = origen
        self.fin = fin
        self.horizontal = horizontal

    def event(self, event):
        self.set_position(event)
    
    def draw(self, screen, color, tam):
        # parametros(x, y, ancho, alto)        
        if self.horizontal: 
            alto = tam / 4
            pygame.draw.rect(screen, color, (self.x, self.y - alto / 2, tam, alto))
        else: 
            ancho = tam / 4
            pygame.draw.rect(screen, color, (self.x - ancho / 2, self.y, ancho, tam))

    def update(self):
        pass    

    def set_position(self, event):
        # get position and recalculate ubication
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mx, my = pygame.mouse.get_pos()
        #     self.x, self.y = mx, my
        #     print(self.x, self.y)
        pass
