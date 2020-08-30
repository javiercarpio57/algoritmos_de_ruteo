import socketio
from link_state_routing import *
from utilities import *

global graph

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('signin', {
        'name': my_node
    })

@sio.event
def my_message(data):
    print('Mensaje recibido ', data)
    # sio.emit('message', data)

@sio.event
def play(data):
    print('play', data)

    if data['algoritmo'] == '3':
        graph = Graph(data['nodes'])
        vecinos = get_neighbors(my_node, data['nodes'])

        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != '0':
            opcion = input(menu)

            if opcion == '1':
                destino = input('Ingrese el destino ' + str(vecinos) + ' : ')
                path = graph.dijkstra(my_node, destino)
                sio.emit('enviar', { 'path': list(path), 'current_destination': path[path.index(my_node) + 1] })


@sio.event
def disconnect():
    print('disconnected from server')

my_node = input('Ingresa tu nodo: ')
sio.connect('http://localhost:5000')

sio.wait()
