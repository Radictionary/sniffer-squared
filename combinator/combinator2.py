
import asyncio
import websockets
import json

from dataclasses import dataclass
from typing import Dict
from copy import copy

from pickledsocks import picklesocks

@dataclass
class Packet:
    id: int
    source: str
    destination: str
    protocol: str
    safety: Dict[str, bool]
    raw: str

    @classmethod
    def from_dict(cls, json):
        return cls(**json)
    
    @classmethod
    async def packet_generator(cls):
        async with websockets.connect("ws://localhost:3957") as websocket:
            while True:
                raw = websocket.recv()
                json_ = json.loads(str(raw))
                packet = cls.from_dict(json_)
                packets.append(packet)


whitelist = []
packets = []
unsafe_packets = set()

def make_safety_data_server_handler(name):
    def safety_data_server_handler(data):
        unsafe_packets.add(f"{name}-{data['id']}")
        return "success"
    return safety_data_server_handler

fingerprint_safety_data_server = picklesocks.make_server(make_safety_data_server_handler("fingerprint"), 3953)
ai_safety_data_server          = picklesocks.make_server(make_safety_data_server_handler("ai"),          3954)
dns_safety_data_server         = picklesocks.make_server(make_safety_data_server_handler("dns"),         3955)
arp_safety_data_server         = picklesocks.make_server(make_safety_data_server_handler("arp"),         3956)


def send_to_backend_server(_):
    # doesn't matter what client sent
    final_packets = []
    for packet in packets:
        final_packets.append(copy(packet))
        for name in ["fingerprint", "ai", "dns", "arp"]:
            final_packets[name] =  \
                f"{name}-{packet['id']}" in unsafe_packets\
                    and packet["source"] not in whitelist
        
    return final_packets


main_send_to_backend_server = picklesocks.make_server(send_to_backend_server, 3957)


def whitelist_server(data):
    match (data["mode"], data["data"]):
        case ("add", ip):
            whitelist.append(ip)
        case ("remove", ip):
            whitelist.remove(ip)
    return "success"

whitelist_server = picklesocks.make_server(whitelist_server)

async def main():
    await asyncio.gather(
        fingerprint_safety_data_server,
        ai_safety_data_server,
        dns_safety_data_server,
        arp_safety_data_server,
        Packet.packet_generator,
        main_send_to_backend_server,
    )