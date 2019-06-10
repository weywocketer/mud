import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mySocket.bind(("127.0.0.1", 3000))
mySocket.listen()
clientSocket, clientAddress = mySocket.accept()

try:
    while True:
        data = clientSocket.recv(4096)
        data = data.decode()
        data = data[::-1]
        data = data.encode()
        clientSocket.sendall(data)
except KeyboardInterrupt:
    print("KI")
    clientSocket.close()
    mySocket.close()
finally:
    print("finally")
    clientSocket.close()
    mySocket.close()