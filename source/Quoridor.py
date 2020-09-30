import pygame
from Player import Player
from Tablero import Tablero

class Quoridor():
    def __init__(self, size, n = 9, n_players = 2):
        self.players = [Player(0, 0, n) for x in range(n_players)]
        self.tablero = Tablero(n, self.players)
        self.tablero.start(size)   

    def update(self):
        self.tablero.update()
        for player in self.players:
            player.update()

    def render(self, screen, size):
        self.tablero.draw(screen, size)
        for player in self.players:
            player.draw(screen) 


    def event_key(self, event):
        pass
        # self.tablero.event_key(event)
        # for player in self.players:
        #     player.event_key(event)           
    



