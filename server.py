import socketio
import eventlet

# create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid,environ):
    print('Se ha conectado',sid)
    my_message(sid, 'funciono')

@sio.event
def disconnect(sid):
    print('Se ha desconectado', sid)

@sio.event
def my_message(sid, data):
    sio.emit('Test', data)
    print('Send message ', data)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)