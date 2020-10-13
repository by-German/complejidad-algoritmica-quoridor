import pygame
from collections import deque


class Player:
	def __init__(self, fila, columna, n, color):
		self.x = fila
		self.y = columna
		self.n = n
		self.turn = False 
		self.origen = 0
		self.destino = 0
		self.color = color
		
	def event_key(self, event):

		pass
	
	def draw(self, screen):
		tam = int(200 / self.n )
		pygame.draw.circle(screen, self.color, (self.x, self.y), tam)

	def update(self):

		pass


	def next_movement(self, origen, destino, G): # orgigen posicion jugador
		camino = []
		self.BFS(G, G.nodes[origen])
		self.hallar_camino(G, G.nodes[origen], G.nodes[destino], camino)
		if len(camino) == 1: # llego al destino
			return camino[0]
		return camino[1] #camino[:2] # return 2 next positions

	def BFS(self, G, s):
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
					nodo["padre"] = u # -> u = nodo
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