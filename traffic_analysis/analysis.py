from scapy.all import *

def process_pcap(pcap_file):
    packets = rdpcap(pcap_file)  # Read PCAP file into memory
    for packet in packets:
        print(process_packet(packet))  # Processing each packet and printing the information

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
        try:
            orig_port = packet[IP].sport
        except KeyError:
            orig_port = '-'

        try:
            resp_port = packet[IP].dport
        except KeyError:
            resp_port = '-'

        try:
            proto = packet[IP].proto
        except KeyError:
            proto = '-'

        try:
            service = packet[TCP].dport
        except KeyError:
            service = '-'

        try:
            duration = packet[TCP].time
        except KeyError:
            duration = '-'

        try:
            orig_bytes = packet[TCP].len
        except KeyError:
            orig_bytes = '-'

        try:
            resp_bytes = packet[TCP].ack
        except KeyError:
            resp_bytes = '-'

        try:
            conn_state = packet.sprintf("%flags%") if TCP in packet else None
        except KeyError:
            conn_state = '-'

        try:
            history = packet.sprintf("%TCP.flags%") if TCP in packet else None
        except KeyError:
            history = '-'

        try:
            orig_pkts = packet[TCP].seq
        except KeyError:
            orig_pkts = '-'

        try:
            orig_ip_bytes = packet[TCP].window
        except KeyError:
            orig_ip_bytes = '-'

        try:
            resp_pkts = packet[TCP].options
        except KeyError:
            resp_pkts = '-'

        try:
            resp_ip_bytes = packet[TCP].urgptr
        except KeyError:
            resp_ip_bytes = '-'

        try:
            label = packet[IP].ttl
        except KeyError:
            label = '-'

        # Append the extracted information to the list
        extracted_info.append([orig_port, resp_port, proto, service, duration, orig_bytes, resp_bytes,
                               conn_state, history, orig_pkts, orig_ip_bytes, resp_pkts, resp_ip_bytes, label])

    return extracted_info

# Example usage
pcap_file = "packet_pool/test.pcap"
process_pcap(pcap_file)