import socketio
from flooding import *
from link_state_routing import *
from utilities import *

global graph
global flood
global vecinos

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('signin', {
        'name': my_node
    })

@sio.event
def my_message(data):
    if (data['path'][-1] == my_node):
        print('Mensaje recibido: ', data['mensaje'])
    else:
        print('Pasaron por mi, SALI EN LA PORTADAAAAA')
        print('El siguiente nodo es: ' + str(data['path'][(data['path'].index(my_node) + 1)]))
        sio.emit('enviar', { 'path': data['path'] , 'mensaje': data['mensaje'], 'current_destination': data['path'][(data['path'].index(my_node) + 1)] })

@sio.event
def flooding_cliente(data):
    global flood
    try:
        flood
        print('llego A')
    except NameError:
        flood = Flooding()
    hopCount = data['hopCount'] - 1
    destino = data['destination']
    mensaje = data['mensaje']
    if flood.nodeState: #Si el estado es verdadero acepta el mensaje, sino ya lo emitio
        if my_node != destino: #Si no es el nodo destino
            print('He sido utilizado')
            flood.zombieBite() # Ya tengo el estado para ya no recibir nada
            if hopCount > 0: #Si aun tengo saltos y no soy el destino, debo volver a enviar el mensaje
                for element in vecinos:
                    sio.emit('flooding',{'destination':destino, 'mensaje': mensaje, 'currentNode':element, 'hopCount':hopCount})
        else:
            flood.zombieBite()
            print(mensaje)


@sio.event
def play(data):
    print('play', data)
    global vecinos 
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
                        sio.emit('flooding',{'destination':destino, 'mensaje': mensaje, 'currentNode':element, 'hopCount':hopCount})
                


    if data['algoritmo'] == '3':
        graph = Graph(data['nodes'])
        vecinos = get_neighbors(my_node, data['nodes'])

        opcion = ''
        menu = '========================\n0. Salir\n1. Enviar un mensaje\n'
        while opcion != '0':
            opcion = input(menu)
            if opcion == '1':
                destino = input('Ingrese el destino ' + str(vecinos) + ' : ')
                mensaje = input('Ingrese el mensaje que desea enviar: \n')
                path = graph.dijkstra(my_node, destino)                
                sio.emit('enviar', { 'path': list(path) , 'mensaje': mensaje, 'current_destination': path[path.index(my_node) + 1] })


@sio.event
def disconnect():
    print('disconnected from server')

my_node = input('Ingresa tu nodo: ')
sio.connect('http://localhost:5000')

sio.wait()
