from socket import *
import ping
testing = False
ipaddr = '192.168.1.48' # gethostbyname(gethostname())  # Find my IP address


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.close()
        return True
    except:
        # print('[-]' + str(tgtPort) + '/tcp closed')
        return False


def portScan(tgtHost, tgtPort):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        # print('[-] Cannot resolve ' + tgtHost + ': Unknown host')
        return False
    setdefaulttimeout(1)
    if connScan(tgtHost, int(tgtPort)):
        return True
    else:
        # print('Error')
        return False

def findAddresses():
	print('Finding viable IP addresses')
	ip_base = ''
	if testing:  # If we are in the testing environment, feed it the IPs we know work
		return ['192.168.1.33', '192.168.1.46', '192.168.1.47', '192.168.1.48']
	for chunk in range(0, 3):  # Create base IP
		ip_base += ipaddr.split('.')[chunk] + '.'
	viable_ips = []
	for ip in range(1, 254):
		ping_ip = ip_base + str(ip)
		result = ping.do_one(ping_ip, 0.05)
		if result is not None and portScan(ping_ip, '22'):
			viable_ips.append(ping_ip)
	print('Found viable IPs: ' + str(viable_ips))
	return viable_ips
