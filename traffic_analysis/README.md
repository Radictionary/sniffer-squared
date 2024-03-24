# AI Analysis README

## AI Tool

Uses Tensorflow to train the model from a dataset of both normal internet traffic and internet traffic during sniffing attacks.

## Usage

1. **Ensure Prerequisites**: Make sure you have the necessary prerequisites installed.
2. **Update Pcap File Path**: Update the `pcap_file` variable with the path to your pcap file. This is already streamlined. 
3. **Run the Script**: The script is executed by the microservice handler.
4. **View Output**: The script outputs information about the packets in the pcap file.

## Functions

- `get_protocol_name(protocol_number)`: Finds the protocol name correlated with the protocol number
- `process_pcap(pcap_file)`: Gathers all the necessary information from the pcap_file
- `encode()`: Uses one hot encoding on the pcap file
- `main()`: The main function of the script. Puts the data into the model and checks if the packet is malicious or not
