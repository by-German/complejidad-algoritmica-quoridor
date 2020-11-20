import pygame
import networkx as nx
from collections import deque
import numpy as np
from dfs_bridge import Dfs
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
        if self.g_coord: self.player_init()
        self.g_coord = False

    def start(self, size):
        self.players[0].turn = True
        self.wallIsPlaced = False #
        self.bridges = []

    def update(self):
        self.console(True)
        self.players_path()
        self.wall_controller()
        self.turn_management()
        pass

    def console(self, active):
        if active:
            system("cls")
            for player in self.players:
                print("color", player.color, "destino: ", player.camino, "origen: ", player.origen, "TURNO:", player.turn)
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
        menor = len(player.camino) + 1 # bloquear al que tiene el camino mas corto
        p_b = None # jugador a bloquear ninguno
        for enemies in self.players: 
            if enemies.origen != player.origen and len(enemies.camino) < menor: # capturar solo enemigos
                menor = len(enemies.camino) 
                p_b = enemies
        if p_b == None: return False # caso p_b no cambie de valor, no se pondra muros            
        # caso contrario, se colocara un muro, para el jugador seleccionado si se cunplen las siguiente condiciones
        
        if len(p_b.camino) > 2 and self.G.has_edge(p_b.origen, p_b.camino[1]) and ((p_b.origen, p_b.camino[1]) not in self.bridges): # existe arista & no se encierra al jugador
            player.place_wall(self.G, origen = p_b.origen, fin = p_b.camino[1]) # se coloca el muro en el camino del jugador a bloquear
            self.wallIsPlaced = True
            # error en camino[2] en un punto, el jugador no tiene ese elemento, "al final del jeugo"
        
        # if len(p_b.camino) > 2:
        #     final, inicio = len(p_b.camino) - 1, len(p_b.camino) - 2
        #     if self.G.has_edge(p_b.camino[inicio], p_b.camino[final]) and ((p_b.camino[inicio], p_b.camino[final]) not in self.bridges):
        #         player.place_wall(self.G, origen = p_b.camino[inicio], fin = p_b.camino[final]) # se coloca el muro en el camino del jugador a bloquear
        #         self.wallIsPlaced = True

        return self.wallIsPlaced

    def wall_controller(self):
        if self.wallIsPlaced:
            self.bridges = Dfs.dfs_bridge(self.G.copy(), time = 0, bridges = [])
            print(self.bridges)
        self.wallIsPlaced = False

    def player_go_to(self, player, destino):
        player.x, player.y = self.G.nodes[destino]["pos"]

    def player_init(self):
        size = len(self.G)
        n = int(np.sqrt(size))
        destinos = [list(range(1, n + 1, 1)), list(range(size - n + 1, size + 1, 1)), list(range(n, size + 1, n)), list(range(1, size - n + 2, n))]
        temp = 1
        id = int(n / 2)
        for i, destino in enumerate(destinos):
            self.players[i].destino = destino
            self.players[i].G = self.G
            self.players[i].origen = destinos[i + temp][id]
            self.player_go_to(self.players[i], self.players[i].origen)
            temp *= -1
