# SERVER COMO ESTABA AYER
import eventlet
import socketio
from utilities import *
import threading
import time

global nodos
global usuarios
global algoritmo
global todos_nodos
global pesos
global contador

puerto = int(input("Ingrese puerto para escuchar en el servidor"))
nodos = int(input("Ingrese el numero de nodos: "))
algoritmo = input('Ingrese el numero del algoritmo que quiere usar:\n1. Flooding\n2. Distance vector routing\n3. Link state routing\n')
usuarios = 0
contador = 0

connected_nodes = {}
usuarioReady = {}

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
    global pesos
    global nodos
    global algoritmo
    global todos_nodos

    print('signin', data)
    connected_nodes[data['name']] = sid
    usuarioReady[data['name']] = {'ready': False, 'data':[],'final':False}

    print(connected_nodes)
    if(nodos-usuarios == 0):
        pesos = get_weights("weights.csv")
        todos_nodos = get_nodes(pesos)

        try:
            for nodo in connected_nodes.keys():
                if str(algoritmo) == '1':
                    print('ALGORITMO:', nodo)
                    sio.emit('play', { 'nodes': pesos, 'algoritmo': algoritmo }, to=connected_nodes[nodo])
                elif str(algoritmo) == '2':
                    print('ALGORITMO:', algoritmo, type(algoritmo))
                    sio.emit('play', { 'nodes': pesos,'todos_nodos': todos_nodos, 'algoritmo': algoritmo }, to=connected_nodes[nodo])
                elif str(algoritmo) == '3':
                    print('ALGORITMO:', nodo)
                    sio.emit('play', { 'nodes': pesos, 'algoritmo': algoritmo }, to=connected_nodes[nodo])
        except:
            print('Error pero no te preocupes')

@sio.event
def dvr(sid,data):
    global pesos
    global contador
    print("entro jejejejej")
    print(data['matriz'])
    print("mis vecinos a enviar son")
    #print(data['vecinos'])

    usuarioReady[data['quienSoy']]['ready'] = True
    usuarioReady[data['quienSoy']]['data'] = data['matriz']
    
    if(all(element['ready'] for element in usuarioReady.values()) and contador <= len(todos_nodos)-1):
        contador += 1
        print("dentro del if",contador)
        for key,info in usuarioReady.items():
            for vecino in get_neighbors(key,pesos):
                #print("Vecino es",vecino)
                #print("Key es",key)
                time.sleep(0.01)
                sio.emit('change', { 'matrizinha' : usuarioReady[key]['data'] , 'quienSoy': key }, to=connected_nodes[vecino])

        for i in connected_nodes:
            usuarioReady[i]['ready'] = False
    else:
        print("Aun no han mandado todos")
        

    if(contador == len(todos_nodos)):
        
        for key,info in usuarioReady.items():
            if(usuarioReady[key]['final'] == False):
                time.sleep(0.04)
                print("Ya todos cumplieron su iteracion")
                sio.emit('final', { }, to=connected_nodes[key])
                usuarioReady[key]['final'] = True

        print(usuarioReady)
        

@sio.event
def enviar(sid, data):
    sio.emit('my_message', { 'path': data['path'], 'mensaje': data['mensaje'] }, to=connected_nodes[data['current_destination']])

@sio.event
def disconnect(sid):
    global usuarios
    global nodos
    usuarios -=1
    print('disconnect ', sid)

@sio.event
def distanceF(sid, data):
    sio.emit('reciboDVR', {'destination':data['destination'], 'mensaje':data['mensaje'],'origen':data['origen'] },to=connected_nodes[data['currentNode']])


@sio.event
def flooding(sid,data):
    print("Enviando a "+data['currentNode'])
    sio.emit('flooding_cliente',{'destination':data['destination'],'mensaje':data['mensaje'], 'sender':data['sender'],'hopCount':data['hopCount']}, to=connected_nodes[data['currentNode']])

@sio.event
def limpiezaFlooding(sid,data):
    print('Limpiando nodos')
    sio.emit('limpiar',{})

if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', puerto)), app)
    


