
import asyncio

from functools import partial

from pickledsocks import picklesocks

# receive data from ports:
#     3953: tls handshakes
#     3954: kelly ai
#     3955: dns spoof
#     3956: arp spoof

# these lists are unnecessary but function as code comments
statuses = {
    "tls_handshake_status": "loading...", 
    "kelly_ai_status": "loading...", 
    "dns_spoof_status": "loading...", 
    "arp_spoof_status": "loading...",
}

ports = [3953, 3954, 3955, 3956]

def status_server(key, new_status):
    statuses[key] = new_status
    return "success"

def all_data(_client_data):
    print("Combinator.all_data handler called, sending data to frontend.")
    # doesn't matter what the client sends,
    # they always get the same response: all of the current data.
    return statuses

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