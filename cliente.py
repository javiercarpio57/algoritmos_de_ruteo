import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('signin', {
        'name': my_node
    })

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('message', data)

@sio.event
def play(data):
    print('play', data)

@sio.event
def disconnect():
    print('disconnected from server')

my_node = input('Ingresa tu nodo: ')
sio.connect('http://localhost:5000')

sio.wait()
