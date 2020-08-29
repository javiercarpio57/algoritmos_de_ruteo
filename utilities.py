import numpy as np

def get_weights(filename):
    w = np.genfromtxt(filename, dtype=str, delimiter=',')
    w_1 = [(ori, dest, float(peso)) for ori, dest, peso in w]
    w_2 = [(dest, ori, float(peso)) for ori, dest, peso in w]
    return w_1 + w_2

def get_nodes(graph):
    nodes = []
    for node in graph:
        if node[0] not in nodes:
            nodes.append(node[0])
        if node[1] not in nodes:
            nodes.append(node[1])
    return nodes

def get_neighbors(nodo, graph):
    nodes = get_nodes(graph)

    vecinos = {}
    for node in nodes:
        vecinos[node] = []

    for conecciones in graph:
        for node in nodes:
            if node == conecciones[0] and conecciones[1] not in vecinos[node] and conecciones[1] != nodo:
                vecinos[node].append(conecciones[1])

    return vecinos[nodo]

        


