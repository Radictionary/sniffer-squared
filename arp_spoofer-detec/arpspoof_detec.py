#!/usr/bin/env python3

# Implementing ARP Spoof Attack Detection Using Scapy

# import modules
import scapy.all as scapy
import os
from pickledsocks import jsoncks
import asyncio
import websockets


# code to get MAC Address
def mac(ipadd):
# requesting arp packets from the IP address
# if it's wrong then will throw error
	arp_request = scapy.ARP(pdst=ipadd)
	br = scapy.Ether(dst="255.255.255.255")
	arp_req_br = br / arp_request
	ans,unans = scapy.srp(arp_req_br, timeout = 5, verbose=True)
	return ans[0][1].hwsrc

# taking interface of the system as an argument
# to sniff packets inside the network
def sniff(interface):
	# store=False tells sniff() function 
	# to discard sniffed packets
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
# good to use for testing, however getting packets from socket instead


# defining function to process sniffed packet
def process_sniffed_packet(packet):
# if it is an ARP packet and if it is an ARP Response
	print("runnin")
	print(type(packet))
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:

	# originalmac will get old MAC whereas
		originalmac = mac(packet[scapy.ARP].psrc)
		# responsemac will get response of the MAC
		responsemac = packet[scapy.ARP].hwsrc
		if originalmac == responsemac:
			print("erm")
		else:
			print("ivan is short")


# get packet data, and sniff
async def receive_data():
    uri = "ws://127.0.0.1:3957"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print("Received:", data)

# Start receiving data
asyncio.run(receive_data())

data = jsoncks.send("give data", 3957)


