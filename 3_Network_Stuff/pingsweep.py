import socket
import sys
import time
import os
import ping

ipaddr = socket.gethostbyname(socket.gethostname())  # Find my IP address

ip_base = ''
for chunk in range(0, 3):  # Create base IP
    ip_base += ipaddr.split('.')[chunk] + '.'

for ip in range(0, 255):
    ping_ip = ip_base + str(ip)
    result = ping.do_one(ping_ip, 0.05)
    if result is not None:
        print(ping_ip + ' Responded in: ' + str(result) + 's')


