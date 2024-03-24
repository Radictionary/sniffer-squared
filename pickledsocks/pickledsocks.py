import zmq
import pickle

from typing import Any, Callable

# Create a ZeroMQ context
context = zmq.Context()


def make_server(f: Callable, port: int):
    """
        f: a handler function which will receive the data from the port.
        port: the port.
    """
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    while True:
        data = pickle.loads(socket.recv())
        result = pickle.dumps(f(data))
        socket.send(result)

def send(data: Any, port: int):
    """
        send data to server at port. data can be anything.
    """
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")
    socket.send(pickle.dumps(data))
    reply = pickle.loads(socket.recv())
    return reply