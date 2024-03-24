
import asyncio

from functools import partial

from pickledsocks import picklesocks, jsoncks

# receive data from ports:
#     3953: tls handshakes
#     3954: kelly ai
#     3955: dns spoof
#     3956: arp spoof

# these lists are unnecessary but function as code comments
statuses = {
    "tls_handshake_packets": [], 
    "kelly_ai_packets": [], 
    "dns_spoof_packets": [], 
    "arp_spoof_packets": [],
}

packets = []

whitelist = ["127.0.0.1"]
ports = [3953, 3954, 3955, 3956]

def status_server(key, new_status):
    statuses[key] = new_status
    return whitelist

def all_data(_client_data):
    print("Combinator.all_data handler called, sending data to frontend.")
    # doesn't matter what the client sends,
    # they always get the same response: all of the current data.
    return statuses

# Whitelist format:
# {"mode":"add","data":"8.8.8.8"}
# {"mode":"remove","data":"8.8.8.8"}
# <written on whiteboard>

def whitelist_server(data):
    if data["mode"] == "add":
        whitelist.append(data["data"])
    else:
        whitelist.remove(data["data"])
    return "success"

tls_handshake_status_server = partial(status_server, key="tls_handshake_status")
kelly_ai_status_server      = partial(status_server, key="kelly_ai_status")
dns_spoof_status_server     = partial(status_server, key="dns_spoof_status")
arp_spoof_status_server     = partial(status_server, key="arp_spoof_status")

async def main():
    print("Combinator.main() coroutine started.")
    await asyncio.gather(
        picklesocks.make_server(all_data, 3952),
        tls_handshake_status_server,
        kelly_ai_status_server,
        dns_spoof_status_server,
        arp_spoof_status_server,
    )

asyncio.run(main())