from scapy.all import *
import requests
from bs4 import BeautifulSoup
import os
from joblib import dump, load
import websockets
import asyncio


def get_protocol_name(protocol_number):
    if protocol_number == 6:
        return "tcp"
    elif protocol_number == 17:
        return "udp"
    return None


def process_pcap(pcap_file):
    # Initialize a list to store extracted information
    extracted_info = []

    d = {}
    with open("traffic_analysis\service-names-port-numbers.csv") as f:
        for line in f:
            try:
                key, val = line.strip().split(',')
                d[val] = key
            except ValueError:
                print(line.split(','))

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
            orig_port = str(packet[IP].sport)
        except IndexError:
            orig_port = '0'

        try:
            resp_port = str(packet[IP].dport)
        except IndexError:
            resp_port = '0'

        try:
            port = packet[IP].proto
            proto = get_protocol_name(port)
        except IndexError:
            proto = '0'

        try:
            try:
                port = str(packet[IP].proto)
            except IndexError:
                service = 'Unkown'
            service = d[port]
        except KeyError:
            service = 'Unkown'


        try:
            duration = str(float(packet.time))
        except IndexError:
            duration = '0'

        try:
            orig_bytes = str(packet[IP].len)
        except IndexError:
            orig_bytes = '0'

        resp_bytes = '0'
          
        if IP in packet:
            tcp_flags = packet[IP].flags
            # Determine connection state based on TCP flags
            if tcp_flags & 0x02 and not tcp_flags & 0x12:
                conn_state = "S0"
            elif tcp_flags & 0x02 and tcp_flags & 0x10:
                conn_state = "SF"
            elif tcp_flags & 0x08 and not tcp_flags & 0x11:
                conn_state = "OTH"
            elif tcp_flags & 0x04:
                conn_state = "D"
            else:
                conn_state = "OTH"
        else:
            # If TCP layer is not present, add a placeholder value
            conn_state = "OTH"


        # Process the history field value
        history = "NA"

        orig_pkts = '0'

        orig_ip_bytes = '0'

        resp_pkts = '0'

        resp_ip_bytes = '0'


        # Append the extracted information to the list
        extracted_info.append([orig_port, resp_port, proto, service, duration, orig_bytes, resp_bytes,
                        conn_state, history, orig_pkts, orig_ip_bytes, resp_pkts, resp_ip_bytes, '0'])

    return extracted_info


def encode():
    # Example usage
    pcap_file = "traffic_analysis/test.pcap"
    perstest = process_pcap(pcap_file)


    import numpy as np
    from sklearn.preprocessing import OneHotEncoder

    columns_to_onehot = [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

    data = np.array(perstest)

    onehot_encoder = OneHotEncoder(sparse_output=True)

    dataCopy = data.copy()

    addedCols = 0
    for column in columns_to_onehot:
        column_values = data[:, column]
        onehot_encoded = onehot_encoder.fit_transform(column_values.reshape(-1, 1)).toarray()
        dataCopy = np.delete(dataCopy, column + addedCols, axis=1)

        # Insert the new columns
        for i, encoded_column in enumerate(onehot_encoded.T):
            dataCopy = np.insert(dataCopy, column + addedCols, encoded_column, axis=1)

        addedCols += onehot_encoded.shape[1] - 1

    data = dataCopy

    return data



async def receive_data():
    uri = "ws://localhost:3957/packets"  # Replace this with the URL of your WebSocket server

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Continuously receive and process data from the WebSocket server
        async for message in websocket:
            # Process the received message
            process_data(message)

def process_data(message):
    print("Recieved: ", message)
    # Your data processing logic here
    message_dict = json.loads(message)["Message"]
    print("Received:", message_dict)
    packet_id, packet_data = message_dict["packetNumber"], message_dict["packetData"]
    print("packet data", packet_data)
    # Load the model from the file
    loaded_model = load('traffic_analysis/xgboost_model.joblib')

    perstest = encode()

    # Now use the loaded model to make predictions
    predictions = loaded_model.predict(perstest)

    ret = []
    for i in range(len(predictions)):
        if predictions[i]:
            ret.append(i + 1)
    return ret

def main():
    asyncio.run(receive_data())



print(main())