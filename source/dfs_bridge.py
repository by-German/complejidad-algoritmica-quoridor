import numpy as np

class Dfs:
    def __init__(self):
        pass

    @staticmethod
    def dfs_bridge(G, time = 0, bridges = []):
        for id, node in G.nodes(data = True): # node is atribute
            node['id'] = id
            node['vis'] = False
            node['p'] = None
            node['low'] = np.inf
            node['disc'] = np.inf

        for id, node in G.nodes(data = True): # node is atribute dict
            u = G.nodes[id]
            if u['vis'] == False:
                Dfs.DFS_visit_bridge(G, u, time, bridges)
        return bridges

    @staticmethod
    def DFS_visit_bridge(G, u, time, bridges):
        u['vis'] = True
        u['disc'] = time
        u['low'] = time
        time += 1

        for id in G.adj[u['id']]: # id de los vecinos
            v = G.nodes[id]
            if v['vis'] == False:
                v['p'] = u
                Dfs.DFS_visit_bridge(G, v, time, bridges)
                # verificar si 'v = G.nodes[id]' tiene una conexion a un ancestro de 'u = node'
                u['low'] = min(u['low'], v['low'])
                if v['low'] > u['disc']:
                    bridges.append((u['id'], v['id']))
            elif v != u['p']:
                u['low'] = min(u['low'], v['disc']) # Actualizar el valor bajo de u para llamadas a funciones principales
     