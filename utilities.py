import numpy as np

def get_weights(filename):
    w = np.genfromtxt(filename, dtype=str, delimiter=',')
    w_1 = [(ori, dest, float(peso)) for ori, dest, peso in w]
    w_2 = [(dest, ori, float(peso)) for ori, dest, peso in w]
    return w_1 + w_2

# def get_nodes(graph):


# def get_neighbors(nodo, grafo):


