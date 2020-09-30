import pygame
from collections import deque

class Player:
	def __init__(self, fila, columna, n):
		self.x = fila
		self.y = columna
		self.G = 0
		self.n = n
		self.turn = False # OJITO AQUII
		self.mov_x = 0
		self.mov_y = 0
		self.origen = 0
		self.destino = 0
		# x_mid = x + (x / 2)
		# y_mid = y + (y / 2)

	def event_key(self, event):
		pass
	
	def draw(self, screen):
		color = (255,0,0)
		tam = int(200 / self.n )
		pygame.draw.circle(screen, color, (self.x, self.y), tam)

	def update(self):

		pass


	def next_movement(self, origen, destino): # orgigen posicion jugador
		camino = []
		G = self.G
		self.BFS(G, G.nodes[origen])
		self.hallar_camino(G, G.nodes[origen], G.nodes[destino], camino)
		if len(camino) == 1:
			return camino[0]
		return camino[1]

	def BFS(self, G, s):
		for _, u in G.nodes(data=True):
			u["color"] = "blanco"
			u["distancia"] = None  # infinito
			u["padre"] = None
		s["color"] = "gris"
		s["distancia"] = 0
		s["padre"] = None
		Q = deque()
		Q.append(s)  # enqueue
		while not (Q == deque([])):
			u = Q.popleft()
			for _, v in G.edges(u["id"]):
				nodo = G.nodes[v]
				if nodo["color"] == "blanco":
					nodo["color"] = "gris"
					nodo["distancia"] = u["distancia"] + 1
					nodo["padre"] = u  # u["id"]
					Q.append(nodo)
			u["color"] = "negro"
		return

	def hallar_camino(self, G, s, v, camino):
		if v["id"] == s["id"]:
			camino.append(s["id"])
		elif v["padre"] == None:
			print("No existe camino de {} a {}".format(s["id"], v["id"]))
		else:
			self.hallar_camino(G, s, v["padre"], camino)
			camino.append(v["id"])
		return