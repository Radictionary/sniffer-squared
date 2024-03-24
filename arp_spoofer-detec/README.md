# ARP Spoofer Detection Tool
This module implements Scapy to detect ARP spoofing, a key method used by packet sniffers.

## Prerequisites 
- Python 3
- Scapy

## ARP
ARP stands for Address Resolution Protocol. It is a protocol used in computer networks to map IP addresses to MAC addresses.
When a device wants to communicate with another device on the same network, it needs to know the MAC address of the destination device. However, devices communicate with each other using IP addresses. ARP helps to resolve this mismatch by translating IP addresses to MAC addresses using a table.

## ARP Spoofing
ARP spoofing, also known as ARP poisoning or ARP cache poisoning, is a technique used by malicious actors to intercept, modify, or redirect network traffic flowing between two devices in a local area network (LAN). This is done by editing the table to have a MAC address pointing to where the attacker wants it to so that they can get packets sent.

## Detection
Detecting ARP spoofing is done by sending a packet with an already incorrect MAC address. If a packet is returned with the same MAC address, this means that no computer took measures to edit the address, meaning that the packet was intercepted by a program that wanted the packet to be changed.

## Usage

1. **Ensure Prerequisites**: Make sure the necessary prerequisites are installed.
2. **Update Pcap File Path**: Update the `pcap_file` variable with the path to your pcap file. This is already streamlined.
3. **Run the Script**: The script is executed by the microservice handler.
4. **View Output**: The script outputs information about the packets that trigger the ARP detection.

## Functions

- mac(ipadd): Sends the edited packet to the suspicious IP address, and returns the answer packet's MAC address.
- sniff(interface): Live detection of packets, unused. Can be used for other purposes.
- process_sniffed_packet(packet): compares the packet with the response.

## Additional Notes
Ensure appropriate permissions to read the pcap file and write to the output file.
Feel free to modify the script according to your specific requirements or integrate it into larger network analysis pipelines.
