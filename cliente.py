import socketio
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
def play(data):
    print('play', data)

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
                path = graph.dijkstra(my_node, destino)
                print('PATH:', path)
                sio.emit('enviar', { 'path': list(path) , 'mensaje': mensaje, 'current_destination': path[path.index(my_node) + 1] })


@sio.event
def disconnect():
    print('disconnected from server')

my_node = input('Ingresa tu nodo: ')
sio.connect('http://localhost:5000')

sio.wait()
