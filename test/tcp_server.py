#   Simple TCP socket, server side, example

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 6507
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address: ', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("server: received data: ", data)
    conn.send(b'data received server')
conn.close()
