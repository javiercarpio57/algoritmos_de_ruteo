import socketio
from flooding import *
from link_state_routing import *
from utilities import *

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

sio = socketio.Client()

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
    if flood.nodeState: #Si el estado es verdadero acepta el mensaje, sino ya lo emitio
        if my_node != destino: #Si no es el nodo destino
            print(bcolors.WARNING + ' -- Pasaron por mi -- ' + bcolors.ENDC)
            flood.zombieBite() # Ya tengo el estado para ya no recibir nada
            if hopCount > 0: #Si aun tengo saltos y no soy el destino, debo volver a enviar el mensaje
                for element in vecinos:
                    print(bcolors.OKBLUE + '\tReenviando a: ' + element + bcolors.ENDC)
                    sio.emit('flooding',{'destination':destino, 'mensaje': mensaje, 'sender':sender,'currentNode':element, 'hopCount':hopCount})
        else:
            flood.zombieBite()
            print(bcolors.OKBLUE + '\t-> ' + sender + ': ' + mensaje + bcolors.ENDC)


@sio.event
def play(data):
    print('play', data)
    global vecinos
    global flood
    vecinos = get_neighbors(my_node, data['nodes'])
    if data['algoritmo'] == '1':
        graph = Graph(data['nodes'])
        hopCount = len(get_nodes(data['nodes']))
        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != 0:
            opcion = input(menu)
            if opcion == '1':
                destino = input('Ingrese el destino ' + str(vecinos) + ' : ')
                mensaje = input('Ingrese el mensaje que desea enviar: \n')
                flood = Flooding()
                flood.zombieBite()
                for element in vecinos:
                        sio.emit('flooding',{'destination':destino, 'mensaje': mensaje,'sender':my_node, 'currentNode':element, 'hopCount':hopCount})
                


    if data['algoritmo'] == '3':
        graph = Graph(data['nodes'])
        vecinos = get_neighbors(my_node, data['nodes'])
        todos_nodos = get_nodes(data['nodes'])

        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != '0':
            opcion = input(menu)
            if opcion == '1':
                destino = input('Ingrese el destino ' + str(todos_nodos) + '\nTus vecinos: ' + str(vecinos) + '\n')
                
                mensaje = input('Ingrese el mensaje que desea enviar: \n')
                path, costo = graph.dijkstra(my_node, destino)

                escribir(my_node, destino, len(list(path)), costo, path, mensaje)

                print('PATH:', path)
                sio.emit('enviar', { 'path': list(path) , 'mensaje': mensaje, 'current_destination': path[path.index(my_node) + 1] })
            elif opcion == '0':
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
