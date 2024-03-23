import ja3
from scapy.all import * 
# Example usage: Sniffing packets and extracting JA3 fingerprints


def extract_ja3_fingerprint(packet):
    if packet.haslayer('Raw') and packet.haslayer('TLS'):
        tls_payload = packet['Raw'].load
        ja3_hash = ja3.ja3_hash(tls_payload)
        ja3_string = ja3.ja3_string(tls_payload)
        return ja3_hash, ja3_string
    return None, None


def process_packet(packet):
    ja3_hash, ja3_string = extract_ja3_fingerprint(packet)
    if ja3_hash and ja3_string:
        print("JA3 Hash:", ja3_hash)
        print("JA3 String:", ja3_string)

# Sniff network traffic and process packets
ja3.sniff(prn=process_packet, filter="tcp port 443", store=0)
