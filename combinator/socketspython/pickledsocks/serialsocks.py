"""
    Facilitate connections processes.

    Python programs communicate amongst themselves with `pickle` or `json`.
    They must communicate with non-python programs with `json`, because
    of course non-python processes cannot use `pickle`.
"""

import zmq.asyncio
from typing import Any, Callable

# create a ZeroMQ context. 
context = zmq.asyncio.Context.instance()

# ------------ important functions ------------

async def make_server(dumper, loader, f: Callable, port: int):
    """
        f: a handler function which will receive the data from the port.
        port: the port.
    """
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    while True:
        data = loader(await socket.recv())
        result = dumper(f(data))
        await socket.send(result)

async def send(dumper, loader, data: Any, port: int):
    """
        send data to server at port. data can be anything.
    """
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")
    await socket.send(dumper(data))
    reply = loader(await socket.recv())
    return reply