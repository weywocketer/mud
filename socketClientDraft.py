#!/usr/bin/env python3

import socket

HOST = '192.168.0.18'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(input("wpisz wiadomość do wysłania.. .. .. ").encode())
data = s.recv(1024)

print('Received', data.decode())
s.close()