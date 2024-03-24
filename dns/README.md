# DNS Resolver Tool

This Python script performs DNS lookups for a list of domains using multiple name servers. It checks for inconsistencies in the DNS responses and reports any errors encountered during the lookup process.

## Usage

1. **Install Required Packages**: Ensure you have the required packages installed, which will already be done by program. You can install them using pip:
    ```
    pip install dnspython
    ```

2. **Run the Script**: The script is executed by the microservice manager. 
3. **View Results**: The script will perform DNS lookups for the specified domains using the list of name servers. It will report any errors encountered during the lookup process and display the DNS responses for each domain.

## Description

- **`dns_lookup(domain, nameserver=None, record_type='A') -> List`:** Performs a DNS lookup for the specified domain. Optionally, you can specify a name server and record type. Returns a list of DNS responses.

- **`all_results(domain, record_type='A')`:** Performs DNS lookups for the specified domain using all configured name servers. Returns a flattened list of DNS responses.

- **`any_results_inconsistent(domain, record_type='A')`:** Checks if there are any inconsistencies in the DNS responses for the specified domain. Returns True if inconsistencies are found, False otherwise.

- **`test(domain)`:** Tests the specified domain for DNS inconsistencies. If any inconsistencies are found, it prints an error message along with the DNS responses.

## Additional Notes

- The script uses the `dnspython` library for DNS resolution.
- The `name_servers` list contains the IP addresses of the name servers to be used for DNS lookups. You can modify this list to include additional or custom name servers.
- The `tested_domains` list contains the domains to be tested. You can modify this list to include the domains you want to test.
- Ensure that your system has network connectivity and access to the specified name servers.
