import dns.resolver

def lookup_dns_records(hostname):
    """Looks up all DNS records for a given hostname.

    Args:
        hostname: The hostname to resolve.

    Returns:
        A list of DNS records.
    """

    resolver = dns.resolver.Resolver()
    resolver.timeout = 5  # Set a timeout of 5 seconds
    resolver.lifetime = 5  # Set a lifetime of 5 seconds

    try:
        answers = resolver.resolve(hostname)
        return answers
    except dns.resolver.NXDOMAIN:
        print(f"No DNS records found for {hostname}")
        return []
    except dns.resolver.Timeout:
        print(f"DNS lookup timed out for {hostname}")
        return []
    except dns.exception.DNSException as e:
        print(f"Error resolving DNS: {e}")
        return []

if __name__ == "__main__":
    hostname = input("Enter a hostname: ")
    answers = lookup_dns_records(hostname)

    if answers:
        print("DNS records found for", hostname)
        for answer in answers:
            print(f"  {answer.rdtype}: {answer.to_text()}")
    else:
        print("No DNS records found for", hostname)