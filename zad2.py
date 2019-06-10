import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mySocket.connect(("127.0.0.1", 3000))

try:
    while True:
        mySocket.sendall(input("Enter data to be send: ").encode())
        print(mySocket.recv(4096).decode())
except KeyboardInterrupt:
    print("KI")
    mySocket.close()
finally:
    print("finally")
    mySocket.close()

