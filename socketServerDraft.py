#!/usr/bin/env python3

import socket
import time
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
i = 684.94
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        if data == "pies":
            conn.sendall("Pytasz o psa??? Twój pies ma {0} lat".format(i).encode())
        else:
            time.sleep(4)
            conn.sendall("Ja Cię nie rozumiem! xD".encode())
    conn.close()
