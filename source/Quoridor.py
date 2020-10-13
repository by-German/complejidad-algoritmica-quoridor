import pygame
from Player import Player
from Tablero import Tablero
from Wall import Wall

color = [(0,0,255), (0,255,0),(255,0,0), (0,255,255)]

class Quoridor():
    def __init__(self, size, n = 9, n_players = 2):
        self.players = [Player(0, 0, n, color[x]) for x in range(n_players)]
        self.tablero = Tablero(n, self.players)
        self.tablero.start(size)   
        self.wall = Wall(tam = size[0] / n)

    def update(self):
        self.tablero.update()
        for player in self.players:
            player.update()
        # temp:
        self.wall.update()

    def render(self, screen, size):
        self.tablero.draw(screen, size)
        for player in self.players:
            player.draw(screen) 
        # se va dibujar dentro del tablero:
        self.wall.draw(screen, (255,255,0))
        


    def event(self, event):
        self.wall.event(event)
        # self.tablero.event_key(event)
        # for player in self.players:
        #     player.event_key(event)           
    



