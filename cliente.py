# TE DA EL VALOR MAS CORTO PERO NO SABEMOS COMO PARA
import socketio
from flooding import *
from link_state_routing import *
from utilities import *
import numpy as np
import time
import math 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

global graph
global flood
global vecinos
global recibidos
global totalN
global miID
global miMatrix
#global terminar
sio = socketio.Client()
recibidos = 0


@sio.event
def connect():
    print(bcolors.OKGREEN + '=== connection established ===' + bcolors.ENDC)
    sio.emit('signin', {
        'name': my_node
    })

@sio.event
def my_message(data):
    if (data['path'][-1] == my_node):
        print(bcolors.OKBLUE + '\t-> ' + data['path'][0] + ': ' + data['mensaje'] + bcolors.ENDC)
    else:
        print(bcolors.WARNING + ' -- Pasaron por mi -- ' + bcolors.ENDC)
        escribir_pasaron_por_mi(' -- Pasaron por mi -- ')
        print(bcolors.OKBLUE + '\tReenviando a: ' + str(data['path'][(data['path'].index(my_node) + 1)]) + bcolors.ENDC)
        sio.emit('enviar', { 'path': data['path'] , 'mensaje': data['mensaje'], 'current_destination': data['path'][(data['path'].index(my_node) + 1)] })

@sio.event
def flooding_cliente(data):
    global flood
    try:
        flood
    except NameError:
        flood = Flooding()

    hopCount = data['hopCount'] - 1
    destino = data['destination']
    mensaje = data['mensaje']
    sender = data['sender']
    print("Estado antes de comprobar",flood.nodeState)
    if flood.nodeState: #Si el estado es verdadero acepta el mensaje, sino ya lo emitio
        if my_node != destino: #Si no es el nodo destino
            print(bcolors.WARNING + ' -- Pasaron por mi -- ' + bcolors.ENDC)
            escribir_pasaron_por_mi(' -- Pasaron por mi -- ')
            print("Esto es antes de llegar el mensaje",flood.nodeState)
            flood.zombieBite() # Ya tengo el estado para ya no recibir nada
            print("Esto es despues de llegar el mensaje",flood.nodeState)
            if hopCount > 0: #Si aun tengo saltos y no soy el destino, debo volver a enviar el mensaje
                for element in vecinos:
                    print(bcolors.OKBLUE + '\tReenviando a: ' + element + bcolors.ENDC)
                    sio.emit('flooding',{'destination':destino, 'mensaje': mensaje, 'sender':sender,'currentNode':element, 'hopCount':hopCount})
        else:
            flood.zombieBite()
            print(bcolors.OKBLUE + '\t-> ' + sender + ': ' + mensaje + bcolors.ENDC)
            sio.emit('limpiezaFlooding',{'mensaje': 'limpiar'})

@sio.event
def limpiar(data):
    global flood
    flood.clean()

@sio.event
def change(data):
    global recibidos
    #global terminar
    recibidos +=1
    
    quienManda = data['quienSoy']
    #print("Los vecinos que te lo mandaron fueron",vecinos)
    #print("YO SOY", my_node,"Y RECIBO DE",quienManda)
    matriz = data['matrizinha']
    matriz = np.array(matriz).reshape(len(totalN), len(totalN))
    #print("\n----------------------------------------------------------------")
    #print(matriz)
    #print("----------------------------------------------------------------\n")
    
    for i in range(len(totalN)):
        for j in range(len(totalN)):
            f = np.Infinity
            if(matriz[i][j] != f and matriz[i][j] != 99):
                if(i != miID and j != miID):
                    #print(matriz[i][j],"en posicion",i,j)
                    columna = totalN.index(quienManda)
                    fila = i
                    nuevaS = matriz[i][j] + miMatrix[columna][columna] 
                    #print("LA suma calculada es", nuevaS)
                    #print("Se debe sustituir por",miMatrix[fila][columna],"? de la posicion",fila,columna)
                    #print("el menor es", min(nuevaS,miMatrix[fila][columna]))
                    miMatrix[fila][columna] = min(nuevaS,miMatrix[fila][columna])

    #print("***********************************************************************")
    #print(miMatrix)
    #print("***********************************************************************")


    #print(terminar,"esto es terminar")
    #print(len(totalN),"esto es cuantas iteraciones debe hacer")

    if(recibidos == len(vecinos)):
        
        #print("ya recibi de todos los vecinos *****************")
        matrix = np.array(miMatrix).tolist()
        
        time.sleep(0.01*totalN.index(my_node))
        sio.emit('dvr', { 'quienSoy':my_node,'matriz': matrix })
        recibidos = 0
            
        #terminar +=1
    
    #print("Esta cantidad de veces se sumo recibidos",recibidos)


    #if(terminar >= len(totalN)):
    #    print("entro aca?")

def get_path(destination, matrixF):
    global totalN
    
    to = totalN.index(destination)
    
    result = np.where(matrixF[to] == np.amin(matrixF[to]))
    
    letra = totalN[result[0][0]]
    return letra         

@sio.event
def final(data):
    global miMatrix
    print("Llegue al final mi matriz final es:")
    print(miMatrix)  
    opcion = ''
    menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
    while opcion != '0':
        opcion = input(menu)
        if opcion == '1':
            error = True
            while error:
                destino = input('Ingrese el destino ' + str(totalN) + ' : ')
                if destino in totalN:
                    error = False
            mensaje = input('Ingrese el mensaje que desea enviar: \n')
            resulta = get_path(destino, miMatrix)

            escribir(my_node, destino, '...', '...', my_node + ' ... ' + destino, mensaje)
            sio.emit('distanceF', {'destination':destino, 'mensaje':mensaje,'currentNode':resulta, 'origen': my_node })

@sio.event
def reciboDVR(data):
    global miMatrix
    if (data['destination'] == my_node):
        print(bcolors.OKBLUE + '\t-> ' + data['origen'] + ': ' + data['mensaje'] + bcolors.ENDC)
    else:
        resultado = get_path(data['destination'], miMatrix)
        print(bcolors.WARNING + ' -- Pasaron por mi -- ' + bcolors.ENDC)
        escribir_pasaron_por_mi(' -- Pasaron por mi -- ')

        print(bcolors.OKBLUE + '\tReenviando a: ' + str(resultado) + bcolors.ENDC)
        sio.emit('distanceF', {'destination':data['destination'], 'mensaje':data['mensaje'],'currentNode':resultado, 'origen':data['origen']  })

@sio.event
def play(data):
    print('play', data)
    global vecinos
    global flood
    vecinos = get_neighbors(my_node, data['nodes'])
    if data['algoritmo'] == '1':
        graph = Graph(data['nodes'])
        nodosss = get_nodes(data['nodes'])
        hopCount = len(nodosss)
        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != '0':
            opcion = input(menu)
            if opcion == '1':

                error = True
                while error:
                    destino = input('Ingrese el destino ' + str(nodosss) + ' : ')
                    if destino in nodosss:
                        error = False
                mensaje = input('Ingrese el mensaje que desea enviar: \n')
                flood = Flooding()
                flood.zombieBite()

                escribir(my_node, destino, '...', '...', my_node + ' ... ' + destino, mensaje)

                for element in vecinos:
                    sio.emit('flooding',{'destination':destino, 'mensaje': mensaje,'sender':my_node, 'currentNode':element, 'hopCount':hopCount})
                


    if data['algoritmo'] == '2':
        # OBTENER GRAFO
        global totalN
        global miID
        global miMatrix
        #global terminar
        
        totalN = data['todos_nodos']
        grafo = data['nodes']
        #terminar = 1
        # OBTENER LOS VECINOS DE MI NODO 
        vecinos = get_neighbors(my_node, data['nodes'])
        #print("Mis vecinos")
        #print(vecinos)
        # OBTENER TODOS LOS NODOS
        nodesGG = data['todos_nodos']
        #print("Todos los nodos del grafo")
        #print(nodesGG)
        # OBTENER QUIENES NO SON MIS VECINOS
        notVecinos = set(nodesGG) - set(vecinos) - set(my_node)
        #print("Estos no son mis vecinos")
        #print(notVecinos)
        # OBTENER EN QUE POSICION ESTA MI NODO
        matrix = np.zeros((len(nodesGG),len(nodesGG)))
        for i in range(len(nodesGG)): 
            for j in range(len(nodesGG)): 
                matrix[i][j] = 99
        miID = nodesGG.index(my_node)
        #print("La posicion de mi nodo", nodesGG.index(my_node))
        # LLENAR POSICIONES DE NODOS NO VALIDOS CON INFINITOS
        matrix[nodesGG.index(my_node)] = np.Infinity
        matrix[:, nodesGG.index(my_node)] = np.Infinity
        # LLENAR POSICIONES DE NODOS NO ALCANZABLES CON INFINITOS
        if(len(notVecinos) > 0):
            for i in notVecinos:
                matrix[:,nodesGG.index(i)] = np.Infinity
        # MATRIZ LISTA PARA LA ITERACION 1
        #print("Matriz con sus bloqueos")
        #print(matrix)

        #print(grafo)
        for i in grafo:
            if(i[0]==my_node):
                indice = nodesGG.index(i[1])
                #print("Colocar",i[1],"en la posicion",indice,",",nodesGG.index(i[1]),"el valor",i[2])
                matrix[indice][indice] = i[2]
        # MATRIZ LISTA PARA LA ITERACION 1
        #print("Matriz con sus valor 1")
        #print(matrix)
        miMatrix = matrix
        matrix = np.array(matrix).tolist()
        
        #for i in vecinos:
        time.sleep(0.01*nodesGG.index(my_node))
        sio.emit('dvr', { 'quienSoy':my_node,'matriz': matrix})
        

    if data['algoritmo'] == '3':
        graph = Graph(data['nodes'])
        vecinos = get_neighbors(my_node, data['nodes'])
        todos_nodos = get_nodes(data['nodes'])

        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != '0':
            opcion = input(menu)
            if opcion == '1':
                error = True
                while error:
                    destino = input('Ingrese el destino ' + str(todos_nodos) + ':')
                    if destino in todos_nodos:
                        error = False
                
                mensaje = input('Ingrese el mensaje que desea enviar: \n')
                path, costo = graph.dijkstra(my_node, destino)

                escribir(my_node, destino, len(list(path)), costo, path, mensaje)

                print('PATH:', path)
                sio.emit('enviar', { 'path': list(path) , 'mensaje': mensaje, 'current_destination': path[path.index(my_node) + 1] })
            elif opcion == '0':
                file.close()

def escribir_pasaron_por_mi(mensaje):
    file = open('log_' + my_node + '.txt', "a")
    file.write(mensaje + '\n')
    file.close()                

def escribir(fuente, destino, saltos, distancia, listado_nodos, mensaje):
    file = open('log_' + my_node + '.txt', "a")
    file.write('===============================================\n')
    file.write('NODO FUENTE: ' + fuente + '\n')
    file.write('NODO DESTINO: ' + destino + '\n')
    file.write('SALTOS RECORRIDOS: ' + str(saltos) + '\n')
    file.write('DISTANCIA: ' + str(distancia) + '\n')
    file.write('LISTADO DE NODOS USADOS: ' + ' --> '.join(listado_nodos) + '\n')
    file.write('MENSAJE: ' + mensaje + '\n')
    file.close()
    

@sio.event
def disconnect():
    print('disconnected from server')

url = input('Ingresa la url del servidor: ')
my_node = input('Ingresa el nombre del nodo: ')

#http://localhost:5000
sio.connect(url)

sio.wait()
