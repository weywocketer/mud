import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mySocket.bind(("127.0.0.1", 3000))
mySocket.listen()