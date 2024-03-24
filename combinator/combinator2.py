
import asyncio
import websockets
import zmq
import json

from dataclasses import dataclass
from typing import Dict
from copy import copy

from pickledsocks import picklesocks

async def packet_generator():
    async with websockets.connect("ws://localhost:3957") as websocket:
        while True:
            raw = await websocket.recv()
            json_ = json.loads(str(raw))
            packets.append(json_)


whitelist = []
packets = []
unsafe_packets = set()

def safety_handler(name):
    def safety_data_server_handler(data):
        unsafe_packets.add(f"{name}-{data['packetNumber']}")
        return "success"
    return safety_data_server_handler


def send_to_backend_server(_):
    # doesn't matter what client sent
    final_packets = []

    for packet in packets:
        final_packet = copy(packet)
        final_packet["safety"] = {}
        for name in ["fingerprint", "ai", "dns", "arp"]:
            final_packet["safety"][name] =  \
                f"{name}-{packet['packetNumber']}" in unsafe_packets\
                    and packet["srcAddr"] not in whitelist
        final_packets.append(final_packet)
        
    return final_packets


def whitelist_server_handler(data):
    match (data["mode"], data["data"]):
        case ("add", ip):
            whitelist.append(ip)
        case ("remove", ip):
            whitelist.remove(ip)
    return "success"

async def main():
    await asyncio.gather(
        picklesocks.make_server(safety_handler("fingerprint"), 3953),
        picklesocks.make_server(safety_handler("ai"),          3954),
        picklesocks.make_server(safety_handler("dns"),         3955),
        picklesocks.make_server(safety_handler("arp"),         3956),
        picklesocks.make_server(send_to_backend_server, 3957),
        picklesocks.make_server(whitelist_server_handler, 3958),
        packet_generator(),
    )

try:
    asyncio.run(main())
except zmq.error.Again as e:
    print(f"Error: resource unavailable. Check if Radin's code is running. \n{e}")