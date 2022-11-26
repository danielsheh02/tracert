import socket
import sys
from tracert_utils import *


def tracert(dest):
    try:
        name, _, address = socket.gethostbyaddr(dest)
    except socket.error:
        print(f"Service {dest} not known, try again")
        exit(1)

    port = 33434
    max_hops = 30
    ttl = 1
    print(f"Trace to {name} ({address[0]}), maximum {max_hops} hops")

    finishRequests = False
    while not finishRequests:
        udp_socket = create_udp_socket(ttl)
        icmp_socket = create_icmp_socket(port)
        print(f"{ttl} ", end="", flush=True)
        udp_socket.sendto(bytes("", "utf-8"), (dest, port))
        curr_name, curr_address = receive_packages(icmp_socket)
        udp_socket.close()
        icmp_socket.close()
        ttl += 1

        if curr_address is not None:
            print(f"{curr_name} {curr_address}")
        else: 
            print()
        if curr_address == address[0] or ttl > max_hops:
            finishRequests = True



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "You must pass one parameter, which will be the IP address or name of the service.\n"
        )
        exit(1)
    tracert(sys.argv[1])
