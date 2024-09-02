import socket

def find_www_service(host):
    """Finds the WWW service of a given host using getaddrinfo().

    Args:
        host: The hostname to resolve.

    Returns:
        A list of tuples containing the resolved addresses and ports.
    """

    try:
        addrinfo = socket.getaddrinfo(host, 80, socket.AF_INET)  # Resolve IPv4 addresses
    except socket.gaierror as e:
        print(f"Error resolving host: {e}")
        return []

    www_services = []
    for family, socktype, proto, canonname, sockaddr in addrinfo:
        if sockaddr[1] == 80:
            www_services.append(sockaddr)

    return www_services

if __name__ == "__main__":
    hostname = input("Enter a hostname: ")
    www_services = find_www_service(hostname)

    if www_services:
        print("WWW services found for", hostname)
        for address, port in www_services:
            print(f"  {address}:{port}")
    else:
        print("No WWW services found for", hostname)
