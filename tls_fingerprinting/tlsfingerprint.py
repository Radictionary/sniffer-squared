import ja3
from scapy.all import *
import socket



def get_ip_address():
    # Get the hostname of the machine
    hostname = socket.gethostname()

    # Get the IP address of the machine
    ip_address = socket.gethostbyname(hostname)

    return hostname, ip_address

# Define a function to extract JA3 fingerprints from TLS handshake packets
def extract_ja3_fingerprint(packet):
    if packet.haslayer('TLS'):
        tls_payload = bytes(packet['TLS'])
        ja3_hash = ja3.ja3_hash(tls_payload)
        ja3_string = ja3.ja3_string(tls_payload)
        return ja3_hash, ja3_string
    return None, None

# Define a function to process packets and detect anomalies
def process_packet(packet):
    ja3_hash, ja3_string = extract_ja3_fingerprint(packet)
    # get ip information
    hostname, IP = get_ip_address()
    if ja3_hash and ja3_string:
        # Compare JA3 fingerprints with known good fingerprints
        hashes = open("good_ja3_hashes.tst","r")
        known_good_ja3_hashes = {k:v for [k,v] in hashes.split("\n").split(",")}
        if ja3_hash not in known_good_ja3_hashes.keys():
            # Anomaly detected: JA3 fingerprint not found in known good fingerprints
            print("Potential packet sniffer detected:")
            print("JA3 Hash:", ja3_hash)
            print("JA3 String:", ja3_string)
            print("hostname", hostname)
            print("Source IP:", packet[IP].src)
            print("Destination IP:", packet[IP].dst)
            print("Packet Info:", packet.summary())
            print("---------------------------------------------")


# Sniff network traffic and process packets
ja3.sniff(prn=process_packet, filter="tcp port 443", store=0)
