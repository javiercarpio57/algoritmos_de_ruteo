from utilities import *

class Flooding:
    def __init__(self,):
        # self.nodes = get_nodes(graph)
        # self.hopCount = len(get_nodes(graph)) #Para la cantidad de saltos que dare
        self.nodeState  = True #El estado de si el nodo aun debe enviar mensaje o descartarlo
        # self.nodeCount = [self.hopCount for i in range(self.hopCount)] #Cantidad de saltos que lleva
        # self.TargetNode = target
        # self.menssageNode = message
        self.arrived = False
        # self.graph = graph

    def zombieBite(self):
        self.nodeState = False

    def resendMessage(self,node): #Si hay vecinos debe enviar el mensaje a nodos vecinos
        print('Envia mensaje')