from scapy.all import *
import socket
import ja3
import subprocess
import ast
import asyncio
import websockets
import json



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
def generate_fingerprint(raw_packet_data):
    # Write the raw packet data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(raw_packet_data)
    
    command = "ja3", " --json" + " -s /fingerprinting/" + str(temp_file)
    return run(command)

async def receive_data():
    uri = "ws://localhost:3957/packets"  # Replace this with the URL of your WebSocket server

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Continuously receive and process data from the WebSocket server
        async for message in websocket:
            # Process the received message
            process_data(message)


def process_data(message):
    # Your data processing logic here
    message_dict = json.loads(message)["Message"]
    print("Received:", message_dict)
    packet_id, packet_data = message_dict["packetNumber"], message_dict["packetData"]
    print("packet data", packet_data)

    packets = ast.literal_eval(generate_fingerprint(packet_data))
    
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

def main():
    # Start receiving data
    asyncio.run(receive_data())
                 
main()
