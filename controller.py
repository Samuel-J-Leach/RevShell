import socket
import threading
#from cryptography.hazmat.primitives.asymmetric import rsa

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5050
BUFFER_SIZE = 1024
FORMAT = "utf-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((SELF, PORT))

SOCKET.listen()
connection, address = SOCKET.accept()

while True:
    command = input(">> ")
    if command == "exit":
        connection.close()
        break
    connection.send(bytes(command, FORMAT))
    output = connection.recv(BUFFER_SIZE)
    print(output)
