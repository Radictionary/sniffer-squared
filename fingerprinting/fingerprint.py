from scapy.all import *
from pickledsocks import jsoncks
import socket
import ja3
import subprocess
import ast
import asyncio
import websockets



#function to run linux commands like ja3
def run(command):
	return subprocess.getoutput(command)

def packet_format(pcap_file):
    # Path to the pcap file
    #pcap_file = "path/to/your/file.pcap"

    #store all the packets in a list
    # Read the pcap file and store the packets in a list
    packets = rdpcap(pcap_file)

    return packets


#get hostname and ip address
def get_ip_address():
    # Get the hostname of the machine
    hostname = socket.gethostname()

    # Get the IP address of the machine
    ip_address = socket.gethostbyname(hostname)

    return hostname, ip_address

#get the fingerprint from the packet
def generate_fingerprint(file):
    return run("ja3 --json packet_pool/test.pcap")

async def receive_data():
    uri = "ws://localhost:3957"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print("Received:", data)


def main():
    # Start receiving data
    data = asyncio.run(receive_data())

    print(data)

    packets = ast.literal_eval(generate_fingerprint())
    
    good_hashes = open("fingerprinting/good_ja3_hashes.txt", "r")


    for packet_info in packets:
        fingerprint = packet_info["ja3_digest"] #get the fingerprint from the packet
        if fingerprint not in good_hashes.read(): # check if the fingerprint is valid
            print("\nNOT SAFE, here is information on it:")
            packet_info = str(packet_info)[1:-1].split(",")
            for info in packet_info:
                print(info)
        else:
            print("\nSAFE, here is information on it:")
            packet_info = str(packet_info)[1:-1].split(",")
            for info in packet_info:
                print(info)
                 
main()
