import pygame
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

clock = pygame.time.Clock()

class Tablero:
    def __init__(self, n = 9, players = []):
        self.n = n
        self.players = players
        G = nx.DiGraph()
        matriz = [[ 0 for column in range(n)] for fila in range(n)]
        count = 0
        for x in range(n):
            for y in range(n):
                count += 1
                if not (y == n - 1):  # enlace  horizontal
                    G.add_edge(count, count + 1, peso=1)
                    G.add_edge(count + 1, count, peso=1)  
                if not (x == n - 1):  # enlace vertical
                    G.add_edge(count, count + n, peso=1)
                    G.add_edge(count + n, count, peso=1)
                matriz[x][y] = count
                G.nodes[count]["id"] = count
        self.G = G
        self.matriz = matriz
        print(self.matriz)
        
    def event_key(self, event):
        # self.event = event
        pass

    def draw(self, screen, size):
        self.screen = screen
        self.size = size
        self.tam = self.size[0] / self.n
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if count % 2 == 0:
                    color = (255,255,255)
                else: 
                    color = (0,0,0)
                pygame.draw.rect(screen, color, (x * self.tam , y * self.tam, self.tam, self.tam))
                count += 1

    def start(self, size):
        self.place__player_init(size)
        self.players[0].turn = True
        pass

    def update(self): 
        # self.place_player()
        self.players_path()
        self.turn_management()
        self.win()

    def turn_management(self):
        for i in range(len(self.players)):
            print(i)
            if self.players[i].turn == True:
                if i == len(self.players) - 1:
                    print("sadas")
                    self.players[0].turn = True
                    self.players[i].turn = False
                    return
                self.players[i + 1].turn = True
                self.players[i].turn = False
                return
        
    def win(self):
        for player in self.players:
            if player.origen == player.destino:
                # eliminarlo de la lista puede ser
                print("win player")

    def players_path(self): 
        for player in self.players:
            if player.turn:
                destino = player.next_movement(player.origen, player.destino)
                self.player_go_to(player, destino)
                player.origen = destino
                pygame.time.delay(1000)  

                # player.draw(self.screen)
                # pygame.display.flip()

    def place_player(self): # mover a los jugadors flechas
        if self.event.type == pygame.KEYDOWN or self.event.type == pygame.KEYUP:
            for player in self.players:
                if player.turn and self.event.key == pygame.K_UP:
                    self.move_player_key(player, mov_y = - player.mov_y)

                if player.turn and self.event.key == pygame.K_DOWN:
                    self.move_player_key(player, mov_y = player.mov_y)

                if player.turn and self.event.key == pygame.K_RIGHT:
                    self.move_player_key(player, mov_x = player.mov_x)

                if player.turn and self.event.key == pygame.K_LEFT:
                    self.move_player_key(player, mov_x = - player.mov_x)

    def player_go_to(self, player, destino):
        if destino == player.origen - 1:
            self.move_player_key(player, mov_x = - player.mov_x)
        elif destino == player.origen + 1:
            self.move_player_key(player, mov_x = player.mov_x)    
        elif destino < player.origen:
            self.move_player_key(player, mov_y = - player.mov_y)
        elif destino > player.origen:
            self.move_player_key(player, mov_y = player.mov_y)

    def move_player_key(self, player, mov_x = 0, mov_y = 0):
        player.x += mov_x
        player.y += mov_y
        # player.turn = False



    def place__player_init(self, size):
        self.size = size
        pos = [int(self.n / 2), int(self.n / 2), 0, self.n - 1]
        des = [
            self.matriz[0][int(self.n / 2)],
            self.matriz[int(self.n - 1)][int(self.n / 2)],
            self.matriz[int(self.n / 2)][int(self.n - 1)],
            self.matriz[int(self.n / 2)][0]
        ]
        x = y =  self.size[0] / self.n # tamaño pantalla / numero cuadros
        col = 0
        fil = -1
        for player in self.players:
            player.G = self.G
            player.x = int(x - (x / 2)) # posicion en la col 0
            player.y = int(y - (y / 2)) # psicicion en la fil 0
            player.mov_x = player.x * 2
            player.mov_y = player.y * 2
            player.destino = des[col]
            print("destino: ", player.destino)
            self.pos_player(player, pos[fil], pos[col]) # index col and fil = 0
            col += 1
            fil -= 1

    def pos_player(self, player, fil, col):
        player.x +=  player.mov_x * col
        player.y +=  player.mov_y * fil
        player.origen = self.matriz[fil][col]
        
        