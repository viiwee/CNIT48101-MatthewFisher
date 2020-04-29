import socket  # Standard Library Socket Module
MAX_BUFFER = 1024  # Set the maximum size to receive

# Create a Socket
myClientSocket = socket.socket()

localHost = socket.gethostname()  # Get local host address


localPort = 57979  # Port to attempt a connection

myClientSocket.connect((localHost, localPort))  # Attempt connection to localHost and localPort

msg = myClientSocket.recv(MAX_BUFFER)  # Program will wait until message is received
print(msg.decode())
# Close the Socket, this will terminate the connection
myClientSocket.close()