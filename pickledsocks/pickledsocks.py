import zmq
import pickle

# Create a ZeroMQ context
context = zmq.Context()

def make_server(f, port):
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    while True:
        data = pickle.loads(socket.recv())
        result = pickle.dumps(f(data))
        socket.send(result)

def send(data, port):
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")
    socket.send(pickle.dumps(data))
    reply = pickle.loads(socket.recv())
    return reply