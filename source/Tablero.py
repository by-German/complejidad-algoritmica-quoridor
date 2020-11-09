import pygame
import networkx as nx
from collections import deque
# temp
from os import system

color = [(0,0,255), (0,255,0),(255,0,0), (0,255,255)]
clock = pygame.time.Clock()

class Tablero:
    def __init__(self, n = 9, players = []):
        self.g_coord = True
        self.n = n
        self.players = players
        self.G = nx.path_graph(n)
        self.G.remove_node(0)
        matriz = [[ 0 for column in range(n)] for fila in range(n)]
        count = 0
        for x in range(n):
            for y in range(n):
                count += 1
                if not (y == n - 1): self.G.add_edge(count, count + 1)
                if not (x == n - 1): self.G.add_edge(count + n, count)
                matriz[x][y] = count
                self.G.nodes[count]["id"] = count
                self.G.nodes[count]["color"] = "blanco"
        self.matriz = matriz

    def event(self, event):
        pass

    def draw(self, screen, size):
        self.screen = screen
        self.size = size
        self.tam = self.size[0] / self.n
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if count % 2 == 0: color = (255,255,255)
                else: color = (0,0,0)
                pygame.draw.rect(screen, color, (x * self.tam , y * self.tam, self.tam, self.tam))
                count += 1
                if self.g_coord:
                    midx = (x * self.tam) + (self.tam / 2)
                    midy = (y * self.tam) + (self.tam / 2)
                    self.G.nodes[count]["pos"] = (int(midx), int(midy)) # posicion en el medio del casillero
        self.g_coord = False

    def start(self, size):
        self.place__player_init(size)
        self.players[0].turn = True

    def update(self):
        self.players_path()
        self.turn_management()
        self.console(True)

    def console(self, active):
        if active:
            system("cls")
            for player in self.players:
                print("destino: ", player.destino, "origen: ", player.origen, "TURNO:", player.turn)
            print("......................")

    def turn_management(self):
        for i in range(len(self.players)):
            if self.players[i].turn == True:
                if i == len(self.players) - 1: # analizó a todos los jugadores
                    self.players[0].turn = True
                    self.players[i].turn = False
                    return
                self.players[i + 1].turn = True
                self.players[i].turn = False
                return

    def can_player_jump(self, destino, player):
        for enemies in self.players:
            if destino == enemies.origen: # si el destino es un enemigo, entonces puede saltar sobre el 
                # player.origen = enemies.origen # cuando salta se seguira moviendo pese a poner muros
                return True
        return False

    def players_path(self):
        for player in self.players:
            if player.turn:
                destino = player.next_movement(player.origen, player.destino, self.G.copy()) # se calcula el destino del jugador
                if self.can_player_jump(destino, player): # caso pueda saltar
                    for i in self.players: self.G.nodes[i.origen]["color"] = "negro" # poner a los enemigos en negro 
                    destino = player.next_movement(destino, player.destino, self.G.copy()) # se recalcula el destino del jugador en base al salto
                    for i in self.players: self.G.nodes[i.origen]["color"] = "blanco" # enemigos de color blanco
                if not self.players_walls(player): #  Se decide si bloquear o avanzar "en esa misma funcion se coloca el muro"
                    self.player_go_to(player, destino) # mueve al jugador visualmente
                    player.origen = destino # mueve al jugador en el grafo
                pygame.time.delay(500)

    def players_walls(self, player):
        # bloquear al que tiene el camino mas corto
        menor = len(player.camino)
        p_b = None # jugador a bloquear ninguno
        for enemies in self.players:
            if enemies.origen != player.origen and len(enemies.camino) < menor: # capturar solo enemigos
                menor = len(enemies.camino) 
                p_b = enemies
        if p_b == None: # caso p_b no cambie de valor, no se pondra muros
            return False
        # caso contrario, se colocara un muro, para el jugador seleccionado
        if len(p_b.camino) > 1 and self.G.has_edge(p_b.origen, p_b.camino[2]): 
            player.place_wall(self.G, origen = p_b.origen, fin = p_b.camino[2]) # se coloca el muro en el camino del jugador a bloquear
            return True 




    def player_go_to(self, player, destino):
        player.x, player.y = self.G.nodes[destino]["pos"]

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

