import pygame
from collections import deque
from Wall import Wall
##
import itertools as itr
import heapq as hq
import numpy as np


class Player:
	def __init__(self, fila, columna, n, color, nro_walls):
		self.x = fila
		self.y = columna
		self.n = n
		self.turn = False 
		self.origen = 0
		self.destino = 0
		self.color = color
		self.wall = []
		self.can_move = True
		# temp
		self.camino = []

	def event_key(self, event):

		pass
	
	def draw(self, screen, size):
		self.tam = size[0] / self.n
		# dibujo del jugador
		tam = int(200 / self.n )
		pygame.draw.circle(screen, self.color, (self.x, self.y), tam)

		# temp: dibujo del wall
		for wall in self.wall:
			wall.draw(screen, self.color, self.tam)
	
	def update(self):
		pass

	def next_movement(self, origen, destinos, G): # orgigen posicion jugador
		self.camino = []
		# self.BFS(G, G.nodes[origen])
		# self.camino = self.road_manager(G, origen, destinos)
		self.camino = self.a_star_multiple(G, origen, destinos)
		if len(self.camino) == 0: return self.origen
		return self.camino[0]

	def BFS(self, G, s):
		s["color"] = "gris"
		s["distancia"] = 0
		s["p"] = None
		Q = deque()
		Q.append(s)  # enqueue
		while not (Q == deque([])):
			u = Q.popleft()
			for _, v in G.edges(u["id"]):
				nodo = G.nodes[v]
				if nodo["color"] == "blanco":
					nodo["color"] = "gris"
					nodo["distancia"] = u["distancia"] + 1
					nodo["p"] = u # -> u = nodo
					Q.append(nodo)
			u["color"] = "negro"
		return

	def road_manager(self, G, origen, destinos) -> list:
		caminos = [[] for _ in range(len(destinos))]
		for id, destino in enumerate(destinos): self.hallar_camino(G, G.nodes[origen], G.nodes[destino], caminos[id])
		camino = caminos[0]
		for id, road in enumerate(caminos):
			if len(camino) > len(road): camino = road
		return camino

	def hallar_camino(self, G, s, v, camino):
		if v["id"] == s["id"]:
			# camino.append(s["id"]) # agrega el ultimo camino faltante
			pass
		elif v["p"] == None: 
			print("No existe camino de {} a {}".format(s["id"], v["id"]))
		else:
			self.hallar_camino(G, s, v["p"], camino)
			camino.append(v["id"]) # agrega todos los caminos 
		return

	def place_wall(self, G, origen, fin):
		xi, yi = G.nodes[origen]["pos"]
		xf, yf = G.nodes[fin]["pos"]
		if xi == xf: ## nodos vericales -> Muro horizontal
			y = abs(yf + yi) // 2 # la resta es para que encaje en la generacion
			self.wall.append(Wall(xi - (self.tam // 2), y, origen, fin, horizontal = True))
		elif yi == yf: ## hotizotal
			x = abs(xf + xi) // 2
			self.wall.append(Wall(x, yi - (self.tam // 2), origen, fin, horizontal = False))
		G.remove_edge(origen, fin) # se remueve el muro -- > se quita la arista en el grafo

	def a_star(self, G, inicial, final):
		push = hq.heappush
		pop = hq.heappop
		contar = itr.count()
		cola = [(0, next(contar), inicial, 0, None)]
		en_cola = {}
		explorados = {}
		while cola:
			_, __, actual, dist, padre = pop(cola)

			if actual == final:
				camino = [actual]
				nodo = padre
				while nodo is not None:
					camino.append(nodo)
					nodo = explorados[nodo]
				camino.reverse()
				return camino

			if actual in explorados:
				if explorados[actual] is None:
					continue
				qcosto, h = en_cola[actual]
				if qcosto < dist:
					continue

			explorados[actual] = padre

			for vecino, w in G[actual].items():
				ncosto = dist + 1
				if vecino in en_cola:
					qcosto, h = en_cola[vecino]
					if qcosto <= ncosto:
						continue
				else:
					h = 0
				en_cola[vecino] = ncosto, h
				push(cola, (ncosto + h, next(contar), vecino, ncosto, actual))

		print("Camino no disponible")


	def a_star_multiple(self, G, inicial, finales):
		minimo = np.inf
		min_path = []
		for final in finales:
			path = self.a_star(G,inicial,final)
			if len(path) < minimo:
				min_path = path
				minimo = len(path)
		if len(min_path):
			min_path = min_path[1:]
		return min_path




	def remove_wall(self, G):
		# self.wall.pop()
		# G.add_edge(self.wall.orgien, self.wall.fin)
		# self.wall.
	 	# podemos retornar la posicion para poner el wall o sino aqui mismo ponerlo
		pass