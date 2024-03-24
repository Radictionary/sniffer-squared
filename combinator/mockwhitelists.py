
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
blacklist = []
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
                    and packet["srcAddr"] not in whitelist \
                    or  packet["srcAddr"] in blacklist
        final_packets.append(final_packet)
        
    return final_packets


def whitelist_server_handler(data):
    match (data["list"], data["mode"], data["ip"]):
        case ("whitelist", "add", ip):
            whitelist.append(ip)
        case ("whitelist", "remove", ip):
            whitelist.remove(ip)
        case ("blacklist", "add", ip):
            blacklist.append(ip)
        case ("blacklist", "remove", ip):
            blacklist.remove(ip)
    return dict(whitelist=whitelist, blacklist=blacklist)

async def main():
    await asyncio.gather(
        picklesocks.make_server(whitelist_server_handler, 3958),
    )

try:
    asyncio.run(main())
except zmq.error.Again as e:
    print(f"Error: resource unavailable. Check if Radin's code is running. \n{e}")