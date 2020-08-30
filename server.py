import eventlet
import socketio
from utilities import *
import threading
import time

global nodos
global usuarios
global algoritmo
global todos_nodos

nodos = int(input("Ingrese el numero de nodos: "))
algoritmo = input('Ingrese el numero del algoritmo que quiere usar:\n1. Flooding\n2. Distance vector routing\n3. Link state routing\n')
usuarios = 0

connected_nodes = {}

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    global usuarios
    global nodos
    usuarios +=1
    
    print("Se han conectado",usuarios,"usuarios faltan",nodos-usuarios)

@sio.event
def message(sid, data):
    print("entro")
    print('message ', data)

@sio.event
def signin(sid, data):
    global nodos
    global algoritmo
    global todos_nodos

    print('signin', data)
    connected_nodes[data['name']] = sid

    print(connected_nodes)
    if(nodos-usuarios == 0):
        pesos = get_weights("weights.csv")
        todos_nodos = get_nodes(pesos)

        try:
            for nodo in todos_nodos:
                if str(algoritmo) == '3':
                    print('ALGORITMO:', algoritmo, type(algoritmo))
                    sio.emit('play', { 'nodes': pesos, 'algoritmo': algoritmo }, to=connected_nodes[nodo])
        except:
            print('Error pero no te preocupes')

@sio.event
def enviar(sid, data):
    sio.emit('my_message', { 'path': data['path'] }, to=connected_nodes[data['current_destination']])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    


