import pygame
import networkx as nx
from collections import deque
# temp
from os import system

color = [(0,0,255), (0,255,0),(255,0,0), (0,255,255)]
clock = pygame.time.Clock()

class Tablero:
    def __init__(self, n = 9, players = []):
        self.n = n
        self.players = players
        self.G = nx.path_graph(n)
        self.G.remove_node(0)
        matriz = [[ 0 for column in range(n)] for fila in range(n)]
        count = 0
        for x in range(n):
            for y in range(n):
                count += 1
                if not (y == n - 1): self.G.add_edge(count, count + 1, peso=1)
                if not (x == n - 1): self.G.add_edge(count + n, count, peso=1)
                matriz[x][y] = count
                self.G.nodes[count]["id"] = count
                self.G.nodes[count]["color"] = "blanco" 
        self.matriz = matriz
        
    def event(self, event):
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

    def update(self): 
        self.players_path()
        if self.can_change_turn: 
            self.turn_management()
        self.console(False)

    def console(self, active):
        if active:
            system("cls")
            for player in self.players:
                print("destino: ", player.destino, "origen: ", player.origen, "TURNO:", player.turn)
            print("......................")

    def turn_management(self):
        for i in range(len(self.players)):
            if self.players[i].turn == True:
                if i == len(self.players) - 1: # analizo a todos los jugadores
                    self.players[0].turn = True
                    self.players[i].turn = False
                    return
                self.players[i + 1].turn = True
                self.players[i].turn = False
                return  

    def can_player_jump(self, destino):
        for enemies in self.players:
            if destino == enemies.origen:
                return False
        return True

    def players_path(self): 
        for player in self.players:
            if player.turn:
                destino = player.next_movement(player.origen, player.destino, self.G.copy())
                # if destino == pos.enemy -> lanzar bfs, en la pos del enemigo           
                self.player_go_to(player, destino)
                if player.origen != player.destino: # todos lleguen destino
                    # devuelve si encuentra un jugador em el destino: false
                    self.can_change_turn = self.can_player_jump(destino)
                    # to be: analizar dos movimientos decidir saltar
                player.origen = destino # mueve al jugador en el grafo
                pygame.time.delay(500)

    def player_go_to(self, player, destino):
        if destino == player.origen - 1:
            self.move_player(player, mov_x = - player.mov_x)
        elif destino == player.origen + 1:
            self.move_player(player, mov_x = player.mov_x)    
        elif destino < player.origen:
            self.move_player(player, mov_y = - player.mov_y)
        elif destino > player.origen:
            self.move_player(player, mov_y = player.mov_y)

    def move_player(self, player, mov_x = 0, mov_y = 0):
        player.x += mov_x
        player.y += mov_y

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
            self.pos_player(player, pos[fil], pos[col]) # index col and fil = 0
            col += 1
            fil -= 1

    def pos_player(self, player, fil, col):
        player.x +=  player.mov_x * col
        player.y +=  player.mov_y * fil
        player.origen = self.matriz[fil][col]   

