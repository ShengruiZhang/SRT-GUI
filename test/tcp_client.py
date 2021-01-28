#   Simple TCP socket, client side, example

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 6507
BUFFER_SIZE = 1024

MESSAGE = "Radio Telescope, Team 21039"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(b'Radio Telescope')
data = s.recv(BUFFER_SIZE)
s.close()

print("client: received data: ", data)
