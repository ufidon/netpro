import dns.resolver

def resolve_multiple_records(hostname, record_types):
    """Resolves multiple DNS records for a given hostname.

    Args:
        hostname: The hostname to resolve.
        record_types: A list of record types to query.

    Returns:
        A dictionary containing the resolved records.
    """

    resolver = dns.resolver.Resolver()
    resolver.timeout = 5  # Set a timeout of 5 seconds
    resolver.lifetime = 5  # Set a lifetime of 5 seconds

    results = {}
    for record_type in record_types:
        try:
            answers = resolver.resolve(hostname, record_type)
            results[record_type] = answers
        except dns.resolver.NXDOMAIN:
            print(f"No {record_type} records found for {hostname}")
        except dns.resolver.Timeout:
            print(f"DNS lookup timed out for {hostname}")
        except dns.exception.DNSException as e:
            print(f"Error resolving DNS: {e}")

    return results

if __name__ == "__main__":
    hostname = input("Enter a hostname: ")
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS']

    records = resolve_multiple_records(hostname, record_types)

    for record_type, answers in records.items():
        if answers:
            print(f"{record_type} records found for {hostname}:")
            for answer in answers:
                print(f"  {answer.to_text()}")
        else:
            print(f"No {record_type} records found for {hostname}")