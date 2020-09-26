import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def grafo_tablero(n):
    count = 0
    G = nx.DiGraph()
    for x in range(n):
        for y in range(n):
            count += 1
            if not (y == n - 1): # enlace  horizontal
                G.add_edge(count, count + 1, peso = 1)
                G.add_edge(count + 1, count, peso = 1)
            if not (x == n - 1): # enlace vertical
                G.add_edge(count, count + n, peso = 1)
                G.add_edge(count + n, count, peso = 1)
            G.nodes[count]["id"] = count
    return G

############################### implementacion BFS ##########################
def BFS(G, s):
    for _, u in G.nodes(data = True):
        u["color"] = "blanco"
        u["distancia"] = None # infinito
        u["padre"] = None
    s["color"] = "gris"
    s["distancia"] = 0
    s["padre"] = None
    Q = deque()
    Q.append(s) # enqueue
    while not (Q == deque([])):
        u = Q.popleft()
        for _, v in G.edges(u["id"]):
            nodo = G.nodes[v]
            if nodo["color"] == "blanco":
                nodo["color"] = "gris"
                nodo["distancia"] = u["distancia"] + 1
                nodo["padre"] = u # u["id"]
                Q.append(nodo)
        u["color"] = "negro"

############################### implementacion DFS ##########################
def DFS_visit(G, u):
    global tiempo
    tiempo += 1
    u["inicio"] = tiempo
    u["color"] = "gris"
    for _, v_id in G.out_edges(u["id"]): # todos los verices que salen de u[id] "devuelve el nombre"
        v = G.nodes[v_id] # v sera el nodo con el identificador del nombre "diccionario de los atributos de v"
        if v["color"] == "blanco":
            v["padre"] = u
            DFS_visit(G, v)
    u["color"] = "negro"
    tiempo += 1
    u["fin"] = tiempo

def DFS(G):
    global tiempo
    for _, u in G.nodes(data = True): # _: id, u: data
        u["color"] = "blanco"
        u["padre"] = None
    tiempo = 0
    for _, u in G.nodes(data = True):
        if u["color"] == "blanco":
            DFS_visit(G, u)


################### Implementacion de Print-Path ##########################
def hallar_camino(G, s, v, camino):
    if v["id"] == s["id"]:
        camino.append(s["id"])
    elif v["padre"] == None:
        print("No existe camino de {} a {}".format(s["id"], v["id"]))
    else:
        hallar_camino(G, s, v["padre"], camino)
        camino.append(v["id"])



################### Implementacion de Dijkstra ##########################
def Dijkstra(Grafo, inicio, meta):
    shrt = {}  # Grabar el costo para llegar al nodo, shrt de shortpath
    trk_pre = {}  # Graba el camino que nos llevo al nodo, trk de track
    nddesc = Grafo  # itera el grafo completo
    inf = 999999  # Solamente un numero grande, que sera mas grande que los pesos de los nodos
    path = []  # grabar el camino de regreso al nodo, el mas optimo

    for node in nddesc:
        shrt[node] = inf
    shrt[inicio] = 0

    while nddesc:
        min_dist = None
        for node in nddesc:
            if min_dist is None:
                min_dist = node
            elif shrt[node] < shrt[min_dist]:
                min_dist = node
            opciones = Grafo[min_dist].items()
            for hijos, peso in opciones:
                if peso + shrt[min_dist] < shrt[hijos]:
                    shrt[hijos] = peso + shrt[min_dist]
                    trk_pre[hijos] = min_dist
            nddesc.pop(min_dist)
    NodoActual = meta()
    while NodoActual != inicio:
        try:

            NodoActual = trk_pre[NodoActual]
        except KeyError:
            path.insert(0, NodoActual)
            print("El camino es no viable")
            break
    path.insert(0, inicio)

######################## Entorno de Pruebas ##########################

n = 4
G = grafo_tablero(n)

nx.draw(G, with_labels = True)
global tiempo
tiempo = 0
#DFS(G)


camino = []
origen = G.nodes[1] # posicion del jugador
destino = G.nodes[7]

BFS(G, origen)

hallar_camino(G, origen, destino, camino)
print(camino)


for i in G:
    print(G[i])
    
Dijkstra(Grafo=G,inicio="1", meta="12")