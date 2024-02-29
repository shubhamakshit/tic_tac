from flask import *
from flask_socketio import SocketIO
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
connections = {}

@app.route('/')
def main():
    return render_template('index.html',_id = uuid.uuid4())

@socketio.on('connect_to_client')
def handle_connect(data):
    print(f'received message: {data}'  )
    
@socketio.on('clicked')
def handle_click(data):
    socketio.emit('sync',data)

@app.route('/<id>')
def multi(id):
    if id in connections:
        if len(connections[id]) == 1:
            connections[id].append(1)
            _cid = 1
        else:
            return('too many connections')
    else:
        connections[id] = [0]
        _cid=0

    print(f'\n\n\n{connections}')
    return render_template('multi.html',_id=id,_cid=_cid)

if __name__ == '__main__':
    socketio.run(app,port=8000,debug=True)
