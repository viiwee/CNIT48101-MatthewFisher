import socket
import sys
from struct import unpack

PROTOCOL_TCP = 6
PROTOCOL_UDP = 17


def PacketExtractor(packet, displaySwitch):
    # Strip off the first 20 characters for the ip header
    stripPacket = packet[0:20]
    # now unpack them
    ipHeaderTuple = unpack('!BBHHHBBH4s4s', stripPacket)
    # unpack returns a tuple, for illustration I will extract
    # each individual values
    # Field Contents
    verLen = ipHeaderTuple[0]  # Field 0: Version and Length
    dscpECN = ipHeaderTuple[1]  # Field 1: DSCP and ECN
    packetLength = ipHeaderTuple[2]  # Field 2: Packet Length
    packetID = ipHeaderTuple[3]  # Field 3: Identification
    flagFrag = ipHeaderTuple[4]  # Field 4: Flags and Fragment Offset
    timeToLive = ipHeaderTuple[5]  # Field 5: Time to Live (TTL)
    protocol = ipHeaderTuple[6]  # Field 6: Protocol Number
    checkSum = ipHeaderTuple[7]  # Field 7: Header Checksum
    sourceIP = ipHeaderTuple[8]  # Field 8: Source IP
    destIP = ipHeaderTuple[9]  # Field 9: Destination IP
    data = packet[verLen:]
    print("################################################")
    print("DATA: " + str(data.decode("utf-8", errors='ignore').strip()))
    print("################################################")
    # Calculate / Convert extracted values
    version = verLen >> 4  # Upper Nibble is the versionNumber
    length = verLen & 0x0F  # Lower Nibble represents the size
    ipHdrLength = length * 4  # Calculate the header length in bytes
    # covert the source and destination address to typical dottednotation strings
    sourceAddress = socket.inet_ntoa(sourceIP)
    destinationAddress = socket.inet_ntoa(destIP)
    if displaySwitch:
        print('=======================')
        print('IP HEADER')
        print('_______________________')
        print('Version:' + str(version))
        print('Packet Length:' + str(packetLength) + 'bytes')
        print('Header Length:' + str(ipHdrLength) + 'bytes')
        print('TTL:' + str(timeToLive))
        print('Protocol:' + str(protocol))
        print('Checksum:' + hex(checkSum))
        print('Source IP:' + str(sourceAddress))
        print('Destination IP:' + str(destinationAddress))
        # _______________________
    if protocol == PROTOCOL_TCP:
        stripTCPHeader = packet[ipHdrLength:ipHdrLength + 20]
        # unpack returns a tuple, for illustration I will extract
        # each individual values using the unpack() function
        tcpHeaderBuffer = unpack('!HHLLBBHHH', stripTCPHeader)
        sourcePort = tcpHeaderBuffer[0]
        destinationPort = tcpHeaderBuffer[1]
        sequenceNumber = tcpHeaderBuffer[2]
        acknowledgement = tcpHeaderBuffer[3]
        dataOffsetandReserve = tcpHeaderBuffer[4]
        tcpHeaderLength = (dataOffsetandReserve >> 4) * 4
        tcpChecksum = tcpHeaderBuffer[7]
        if displaySwitch:
            print('_______________________')
            print('TCP Header')
            print('Source Port: ' + str(sourcePort))
            print('Destination Port :' + str(destinationPort))
            print('Sequence Number : ' + str(sequenceNumber))
            print('Acknowledgement : ' + str(acknowledgement))
            print('TCP Header Length: ' + str(tcpHeaderLength) + 'bytes')
            print('TCP Checksum:' + hex(tcpChecksum))
        return ['TCP', sourceAddress, sourcePort, destinationAddress, destinationPort]
    elif protocol == PROTOCOL_UDP:
        stripUDPHeader = packet[ipHdrLength:ipHdrLength + 8]
        # unpack returns a tuple, for illustration I will extract
        # each individual values using the unpack() function
        udpHeaderBuffer = unpack('!HHHH', stripUDPHeader)
        sourcePort = udpHeaderBuffer[0]
        destinationPort = udpHeaderBuffer[1]
        udpLength = udpHeaderBuffer[2]
        udpChecksum = udpHeaderBuffer[3]
        if displaySwitch:
            print('_______________________')
            print('UDP Header')
            print('Source Port: ' + str(sourcePort))
            print('Destination Port :' + str(destinationPort))
            print('UDP Length: ' + str(udpLength) + 'bytes')
            print('UDP Checksum:' + hex(udpChecksum))
            return ['UDP', sourceAddress, sourcePort, destinationAddress, destinationPort]
        else:
            # For expansion protocol support
            if displaySwitch:
                print('Found Protocol :' + str(protocol))
            return ['Unsupported', sourceAddress, 0, destinationAddress, 0]
