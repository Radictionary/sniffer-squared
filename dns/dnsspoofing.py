from typing import List

import dns.resolver

name_servers = [
    "8.8.8.8",
    "76.76.2.0", 
    "9.9.9.9",
    "208.67.222.222",
    "1.1.1.1",
    "94.140.14.14",
    "185.228.168.9",
    "76.76.19.19",
    None,
]

tested_domains = [
    "google.com",
    "openai.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "reddit.com",
    "microsoft.com",
]

def dns_lookup(domain, nameserver=None, record_type='A') -> List:
    resolver = dns.resolver.Resolver()
    if nameserver:
        resolver.nameservers = [nameserver]
    try:
        return resolver.resolve(domain, record_type)
    except Exception as e:
        raise RuntimeError(f"dns_lookup({domain}, {nameserver}, {record_type})\nError: {e}")

def all_results(domain, record_type='A'):
    unflattened = [dns_lookup(domain, name_server, record_type) for name_server in name_servers]
    flattened_results = []
    for sublist in unflattened:
        flattened_results.extend(sublist)
    return flattened_results

def any_results_inconsistent(domain, record_type='A'):
    return len(set(all_results(domain, record_type))) != 1

def test(domain):
    if any_results_inconsistent(domain):
        print(f"Error with domain {domain}!")
        for result in all_results(domain):
            print(f"\t{result}")
        exit(1)

if __name__ == "__main__":
    for domain in tested_domains:
        test(domain)
    exit(0)

