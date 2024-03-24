#!/usr/bin/env python3

# Implementing ARP Spoof Attack Detection Using Scapy

# import modules
import scapy.all as scapy
import os
from pickledsocks import jsoncks
import asyncio


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
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:

	# originalmac will get old MAC whereas
		originalmac = mac(packet[scapy.ARP].psrc)
		# responsemac will get response of the MAC
		responsemac = packet[scapy.ARP].hwsrc
		if originalmac == responsemac:
			return True
		return False


async def main():
	send_result = {"id":0}
	packet = list(scapy.rdpcap("packet_pool/packets.pcap"))[-1]
	
	if process_sniffed_packet(packet):
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


