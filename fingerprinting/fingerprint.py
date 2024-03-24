import asyncio
from scapy.all import *
import socket
import ja3
import subprocess
import ast
from pickledsocks import jsoncks



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
def generate_fingerprint():
    return run("ja3 --json packet_pool/packets.pcap")

async def main():
    send_result = {"id":0}
    packets = ast.literal_eval(generate_fingerprint())

    good_hashes = open("fingerprinting/good_ja3_hashes.txt", "r")


    packet_info = packets[-1]


    if packet_info["ja3"].split(",")[-1].split("-")[0] == "0": # check if handshake
    
        fingerprint = packet_info["ja3_digest"] #get the fingerprint from the packet
        if fingerprint not in good_hashes.read(): # check if the fingerprint is valid
            ids = open("packet_pool/id.txt", "r")
            send_result["id"] = ids.readlines()[-1].strip() #get correspondinf id
            print(send_result)
            print("NOT SAFE")
            try:
                await asyncio.wait_for(jsoncks.send(send_result, 3953), timeout=3)
            
            except asyncio.TimeoutError:
                print("time out")
            print("done did the send :3")


async def mainloop():
    while True:
        await main()

asyncio.run(mainloop())