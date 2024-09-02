import dns.resolver

def resolve_mail_record(hostname):
    """Resolves the MX record for a given hostname.

    Args:
        hostname: The hostname to resolve.

    Returns:
        A list of MX records.
    """

    resolver = dns.resolver.Resolver()
    resolver.timeout = 5  # Set a timeout of 5 seconds
    resolver.lifetime = 5  # Set a lifetime of 5 seconds

    try:
        answers = resolver.resolve(hostname, 'MX')
        return answers
    except dns.resolver.NXDOMAIN:
        print(f"No MX records found for {hostname}")
        return []
    except dns.resolver.Timeout:
        print(f"DNS lookup timed out for {hostname}")
        return []
    except dns.exception.DNSException as e:
        print(f"Error resolving DNS: {e}")
        return []

if __name__ == "__main__":
    hostname = input("Enter a hostname: ")
    mail_records = resolve_mail_record(hostname)

    if mail_records:
        print("MX records found for", hostname)
        for record in mail_records:
            print(f"  {record.preference}: {record.exchange}")
    else:
        print("No MX records found for", hostname)