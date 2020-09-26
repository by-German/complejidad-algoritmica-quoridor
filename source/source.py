import networkx as nx
import matplotlib.pyplot as plt

def grafo_tablero(n):
    count = 0
    G = nx.DiGraph()
    for x in range(n):
        for y in range(n):
            count += 1
            if not (y == n - 1): # enlace  horizontal
                G.add_edge(count, count + 1)
                G.add_edge(count + 1, count)
            if not (x == n - 1): # enlace vertical
                G.add_edge(count, count + n)
                G.add_edge(count + n, count)
            G.nodes[count]["id"] = count
            G.nodes[count]["peso"] = 1
    return G

n = 4
G = grafo_tablero(n)

nx.draw(G, with_labels = True)