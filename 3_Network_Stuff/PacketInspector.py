# Packet sniffer in python
# For Linux
import socket
import decoder
import time
from struct import unpack


def capturePacket():
    t0 = time.time()
    capture_duration = 10  # Duration in seconds to capture

    # create an INET, raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)  # Create the socket
    s.bind(("192.168.1.43", 0))  # Bind to the socket
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  # Receive all packets?

    ipObservations = []  # List of observations
    while True:
        if (time.time() - t0) > capture_duration:
            break
        recvBuffer, addr = s.recvfrom(65565)  # Receive a packet
        content = decoder.PacketExtractor(recvBuffer, False)
        ipObservations.append(content)

    s.close()


capturePacket()

