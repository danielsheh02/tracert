import socket
import struct


def create_udp_socket(ttl: int) -> socket.socket:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return udp_socket


def create_icmp_socket(port: int) -> socket.socket:
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = struct.pack("ll", 5, 0)
    icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
    return icmp_socket


def receive_packages(icmp_socket: socket.socket):
    tries = 3
    curr_address = None
    curr_name = None
    finished = False
    while not finished and tries > 0:
        try:
            _, curr_address = icmp_socket.recvfrom(1024)
            finished = True
            curr_address = curr_address[0]
            try:
                curr_name, _, _ = socket.gethostbyaddr(curr_address)
            except socket.error:
                curr_name = curr_address
        except socket.error:
            tries -= 1
            print("* ", end="", flush=True)

    return curr_name, curr_address
