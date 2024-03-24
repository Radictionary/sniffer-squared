# Packet Fingerprinting Tool

This Python script utilizes the Scapy library to analyze packet capture (pcap) files and extract fingerprint information using the JA3 SSL/TLS fingerprinting technique. The script provides insights into the SSL/TLS handshake details of captured network traffic.

## Prerequisites

- Python 3.x
- Scapy library (`pip install scapy`)
- JA3 library (`pip install ja3`)

## TLS/SSL Fingerprinting
TLS/SSL fingerprinting, also known as SSL fingerprinting or TLS handshake fingerprinting, is a technique used to identify or profile SSL/TLS implementations based on the characteristics of their handshake messages. The SSL/TLS handshake is an initial exchange of messages between a client (e.g., a web browser) and a server (e.g., a web server) that establishes a secure communication channel.

## Usage

1. **Ensure Prerequisites**: Make sure you have the necessary prerequisites installed.
2. **Update Pcap File Path**: Update the `pcap_file` variable with the path to your pcap file.
3. **Run the Script**: Execute the following command in your terminal:
    ```
    python script_name.py
    ```
4. **View Output**: The script outputs information about the packets in the pcap file, including SSL/TLS fingerprint details.

## Functions

- `packet_format(pcap_file)`: Reads the pcap file and returns a list containing all packets.
- `get_ip_address()`: Retrieves the hostname and IP address of the local machine.
- `generate_fingerprint()`: Runs the JA3 tool to generate SSL/TLS fingerprint information from the packets.
- `main()`: The main function of the script. It processes the generated fingerprints and checks them against a list of known safe fingerprints. It then outputs information about each packet, indicating whether it is safe or not.

## Additional Notes

- Ensure appropriate permissions to read the pcap file and write to the output file.
- The script reads a list of known safe fingerprints from the `good_ja3_hashes.txt` file. Make sure this file exists and contains valid fingerprints for comparison.

Feel free to modify the script according to your specific requirements or integrate it into larger network analysis pipelines.