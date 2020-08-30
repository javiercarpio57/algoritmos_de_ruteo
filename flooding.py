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

    # def checkState(self,node):
    #     indexNode = self.nodes.index(node)
    #     if(self.nodeCount[indexNode] == 0): #Si el hopCount es 0 ya no debe seguir enviando
    #         self.nodeState[indexNode] = False
    #         if(node == self.TargetNode): #En caso que si llego al nodo objetivo
    #             self.arrived = True
    #             return True
    #     else:
    #         if(self.nodeState[indexNode]):
    #             self.nodeCount[indexNode] -= 1
    #             if(node == self.TargetNode): #En caso que si llego al nodo objetivo
    #                 self.arrived = True
    #                 return True
    #             else: #Si no ha llegdo debe reenviar el mensaje a los nodos vecinos
    #                 # neighboors = get_neighbors(node,self.graph) #Obtener vecinos para poder enviar mensaje

    #                 # self.nodeState[indexNode] = 0
    #                 # for element in neighboors:
    #                 #     self.resendMessage(element)
    #                 return False
                

    def clean(self):
        self.nodeState  = [True for i in range(self.hopCount)] #El estado de si el nodo aun debe enviar mensaje o descartarlo
        self.nodeCount = [self.hopCount for i in range(self.hopCount)] #Cantidad de saltos que lleva

    def resendMessage(self,node): #Si hay vecinos debe enviar el mensaje a nodos vecinos
        print('Envia mensaje')