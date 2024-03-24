from scapy.all import *
import requests
from bs4 import BeautifulSoup

def process_pcap(pcap_file):
    packets = rdpcap(pcap_file)  # Read PCAP file into memory
    for packet in packets:
        print(process_packet(packet))  # Processing each packet and printing the information


def get_protocol_name(protocol_number):
    if protocol_number == 6:
        return "tcp"
    elif protocol_number == 17:
        return "udp"
    return None


def process_packet(packet):
    # Initialize a list to store extracted information
    extracted_info = []

    # Open the PCAP file and process each packet
    '''id.orig_p: Source Port
    id.resp_p: Destination Port
    proto: Protocol
    service: Service Type
    duration: Duration of Connection
    orig_bytes: Original Packet Size
    resp_bytes: Response Packet Size
    conn_state: Connection State
    history: Connection History
    orig_pkts: Original Packets Count
    orig_ip_bytes: Original IP Bytes
    resp_pkts: Response Packets Count
    resp_ip_bytes: Response IP Bytes'''
    for packet in rdpcap(pcap_file):
        # Extract desired fields from each packet
        #print(packet.json())
        try:
            orig_port = packet[IP].sport
        except IndexError:
            orig_port = '-'

        try:
            resp_port = packet[IP].dport
        except IndexError:
            resp_port = '-'

        try:
            proto = get_protocol_name(packet[IP].proto)
        except IndexError:
            proto = '-'

        # try:
        #     service = packet[UDP].dport
        # except KeyError:
        service = '-'

        try:
            duration = packet.time
        except IndexError:
            duration = '-'

        try:
            orig_bytes = packet[IP].len
        except IndexError:
            orig_bytes = '-'

        resp_bytes = '-'
        # try:
        #     resp_bytes = packet[UDP].ack
        # except IndexError and AttributeError:
        #     resp_bytes = '-'

        try:
            conn_state = packet.sprintf("%flags%") if UDP in packet else None
        except IndexError:
            conn_state = '-'

        try:
            history = packet.sprintf("%TCP.flags%") if UDP in packet else None
        except IndexError:
            history = '-'

        # try:
        #     orig_pkts = packet[UDP].seq
        # except KeyError:
        orig_pkts = '-'

        # try:
        #     orig_ip_bytes = packet[UDP].window
        # except KeyError:
        orig_ip_bytes = '-'

        # try:
        #     resp_pkts = packet[UDP].options
        # except KeyError:
        resp_pkts = '-'

        # try:
        #     resp_ip_bytes = packet[UDP].urgptr
        # except KeyError:
        resp_ip_bytes = '-'


        # Append the extracted information to the list
        # extracted_info.append([orig_port, resp_port, proto, duration, orig_bytes, 
        #                        conn_state, history])
        extracted_info.append([orig_port, resp_port, proto, service, duration, orig_bytes, resp_bytes,
                        conn_state, history, orig_pkts, orig_ip_bytes, resp_pkts, resp_ip_bytes, '-'])

    return extracted_info

# Example usage
pcap_file = "packet_pool/test.pcap"
process_pcap(pcap_file)