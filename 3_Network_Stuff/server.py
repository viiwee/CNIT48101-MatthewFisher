#
# Server Objective
# 1) Setup a Simple listening Socket
# 2) Wait for a connection request
# 3) Accept a connection on port 5555
# 4) Upon a successful connection send a message to the client
#
import socket # Standard Library Socket Module
# Create Socket
myServerSocket = socket.socket()
# Get my local host address
localHost = socket.gethostname()
# Specify a local Port to accept connections on
localPort = 5565
# Bind myServerSocket to localHost and the specified Port
# Note the bind call requires one parameter, but that
# parameter is a tuple (notice the parenthesis usage)
myServerSocket.bind((localHost, localPort))
# Begin Listening for connections
myServerSocket.listen(1)
# Wait for a connection request
# Note this is a synchronous Call
# meaning the program will halt until
# a connection is received.
# Once a connection is received
# we will accept the connection and obtain the
# ipAddress of the connector
print('Python-Forensics .... Waiting for Connection Request')
conn, clientInfo = myServerSocket.accept()
# Print a message to indicate we have received a connection
print('Connection Received From:', clientInfo)
# Send a message to connector using the connection object'conn'
# that was returned from the myServerSocket.accept() call
# Include the client IP Address and Port used in the response
conn.send(('Connection Confirmed:'+'IP: ' + clientInfo[0] + ' Port:' + str(clientInfo[1])).encode())
