"""
    Facilitate connections processes.

    Python programs communicate amongst themselves with `pickle` or `json`.
    They must communicate with non-python programs with `json`, because
    of course non-python processes cannot use `pickle`.
"""

import zmq.asyncio
import asyncio
import pickle
import json

from functools import partial, wraps
from typing import Any, Callable

# create a ZeroMQ context. 
context = zmq.asyncio.Context.instance()

def bytesify_output(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return bytes(f(*args, **kwargs), encoding="utf-8")
    return wrapper

def stringify_input(f):
    @wraps(f)
    def wrapper(input_, *args, **kwargs):
        return f(str(input_, encoding="utf-8"), *args, **kwargs)
    return wrapper

# modify the json functions so that they work with bytes.
# for some reason pickle & json are incompatible 
# because pickle.loads takes bytes & json.loads takes str
# (same for outputs of X.dumps)

json.dumps = bytesify_output(json.dumps)
json.loads = stringify_input(json.loads)

# ------------ important functions ------------

async def make_server(serializer, f: Callable, port: int):
    """
        f: a handler function which will receive the data from the port.
        port: the port.
    """
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    while True:
        data = serializer.loads(await socket.recv())
        result = serializer.dumps(f(data))
        await socket.send(result)

async def send(serializer, data: Any, port: int):
    """
        send data to server at port. data can be anything.
    """
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")
    await socket.send(serializer.dumps(data))
    reply = serializer.loads(await socket.recv())
    return reply


python_make_server = partial(make_server, pickle)
python_send = partial(send, pickle)


json_make_server = partial(make_server, json)
json_send = partial(send, json)


# if __name__ == "__main__":
#     # simple test program
#     import sys

#     is_server = sys.argv[1].strip() == 'y'
#     module = jsoncks

#     def get(data):
#         print(f"I got data: {data}")
#         return "I got your data!"
    
#     if is_server:
#         asyncio.run(module.make_server(get, 3952))
#     else:
#         asyncio.run(module.send("Hi server from client!", 3952))