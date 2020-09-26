import networkx as nx
import matplotlib.pyplot as plt


def grafo_tablero(n):
    count = 0
    G = nx.DiGraph()
    for x in range(n):
        for y in range(n):
            count += 1
            if not (y == n - 1):  # enlace  horizontal
                G.add_edge(count, count + 1)
                G.add_edge(count + 1, count)
            if not (x == n - 1):  # enlace vertical
                G.add_edge(count, count + n)
                G.add_edge(count + n, count)
            G.nodes[count]["id"] = count
            G.nodes[count]["peso"] = 1
    return G


n = 4
G = grafo_tablero(n)


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


for i in G:
    print(G[i])
    
Dijkstra(Grafo=G,inicio="1", meta="12")