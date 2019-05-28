import socket
import threading
import time


class ServerThread(threading.Thread):
    def run(self):
        server()

def server(port):
    i = 684.94
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
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


host = '127.0.0.1'