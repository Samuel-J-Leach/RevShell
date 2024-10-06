import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
'''
def handleConnection(connection, address):
    while True:
        command = input(">> ")
        if command == "exit":
            connection.close()
            break
        connection.send(bytes(command, FORMAT))
        output = connection.recv(BUFFER_SIZE)
        print(output.decode(FORMAT))
'''

connections = {}

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5050
BUFFER_SIZE = 1024
FORMAT = "utf-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((SELF, PORT))

def acceptConnections():
    SOCKET.listen()
    while True:
        connection, address = SOCKET.accept()
        connections[address] = connection

def sendCommand(addr, cmd):
    conn = connections[addr]
    conn.send(bytes(cmd, FORMAT))
    print(conn.recv(BUFFER_SIZE).decode(FORMAT))

def disconnectAll():
    #terminate all connections
    #receivers should go into standby mode
    for addr in connections:
        connections[addr].send(bytes("HOST_DISCONNECT", FORMAT))

thread = threading.Thread(target=acceptConnections)
thread.start()

print("address:command")

while True:
    command = input(">")
    commandThread = threading.Thread(target=sendCommand, args=(command))

