import eventlet
import socketio
from utilities import *
import threading


global nodos
global usuarios
nodos = int(input("Ingrese el numero de nodos: "))
usuarios = 0
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    global usuarios
    usuarios +=1
    
    print('connect ', sid)
    print("Se han conectado",usuarios,"usuarios faltan",nodos-usuarios)
    if(nodos-usuario == 0):
        pesos = get_weights("weights.csv")
        nodos = get_nodes(pesos)
        
        sio.emit()
@sio.event
def message(sid, data):
    print("entro")
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    


