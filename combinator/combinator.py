
import asyncio

from pickledsocks import picklesocks

# receive data from ports:
#     3953: tls handshakes
#     3954: kelly ai
#     3955: dns spoof
#     3956: arp spoof

# these lists are unnecessary but function as code comments
tls_handshake_data = []
kelly_ai_data = []
dns_spoof_data = []
arp_spoof_data = []

history_lists = [[], [], [], []]
new_lists = [tls_handshake_data, kelly_ai_data, dns_spoof_data, arp_spoof_data]
ports = [3953, 3954, 3955, 3956]

def all_data(_client_data):
    print("Combinator.all_data handler called, sending data to frontend.")
    # doesn't matter what the client sends,
    # they always get the same response: all of the current data.
    result = [list_.copy() for list_ in new_lists]
    for list_ in new_lists:
        history_lists.extend(list_)
        list_.clear()
    return result

async def main():
    print("Combinator.main() coroutine started.")
    await asyncio.gather(
        picklesocks.make_server(all_data, 3952),
        *[
            picklesocks.make_server(list_.append, port)
            for list_, port in zip(lists, ports)
        ]
    )

asyncio.run(main())