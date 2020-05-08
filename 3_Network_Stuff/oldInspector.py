import socket
import os
import struct

os.system("netsh bridge set adapter 1 forcecompatmode=enable")


def grab_packet():
    sniffSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    ainfo=socket.getaddrinfo('127.0.0.1', 255)

    sniffSocket.bind(ainfo[0][4])
    # Next command will wait until a package is received to continue
    recvBuffer = sniffSocket.recvfrom(65536)
    return recvBuffer


def grabData(packet):
    print(packet[0])
    ipHeaderTuple = struct.unpack('!BBHHHBBH4s4s', packet[0][0:20])
    print(ipHeaderTuple)


grabData(grab_packet())
