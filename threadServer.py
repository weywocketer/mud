import socket
from threading import Thread
import time
import random
#from SocketServer import ThreadingMixIn


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

    def __init__(self, ip, port, conn):
        self.i = random.random()
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        j = 0
        while True:
            time.sleep(2)
            self.conn.sendall(str(j).encode())
            j += 1

            """data = self.conn.recv(2048)
            data = data.decode()
            print("Server received data:", data)
            if data == "pies":
                time.sleep(1)
                self.conn.sendall("Pytasz o psa??? Twój pies ma {0} lat".format(self.i).encode())
            elif data == "thread":
                self.conn.sendall("threads: {}".format(threads).encode())
                #conn.sendall("conn: {}".format(self.co).encode())
            else:
                self.conn.sendall("Ja Cię nie rozumiem! xD".encode())
            #if data == 'exit':
            #    break
            #conn.send(MESSAGE.encode())  # echo"""


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '127.0.0.1'
TCP_PORT = 2004
BUFFER_SIZE = 20  # Usually 1024, but we need quick response
krzak = ""

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []
tcpServer.listen(4)

while True:

    print("server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)
    print("threads: ", threads)
#for t in threads:
 #   t.join()