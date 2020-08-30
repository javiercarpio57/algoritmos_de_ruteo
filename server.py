import eventlet
import socketio
from utilities import *
import threading
import time


global nodos
global usuarios
nodos = int(input("Ingrese el numero de nodos: "))
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
    print('signin', data)
    connected_nodes[data['name']] = sid

    print(connected_nodes)

    if(nodos-usuarios == 0):
        pesos = get_weights("weights.csv")
        nodos = get_nodes(pesos)

        for nodo in nodos:
            sio.emit('play', { 'nodes': [nodo]}, to=connected_nodes[nodo])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    


