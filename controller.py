import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa

connections = {}

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5050
BUFFER_SIZE = 1024
FORMAT = "utf-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((SELF, PORT))

#runs constantly in the background letting receivers connect
def acceptConnections():
    SOCKET.listen()
    while True:
        try:
            connection, address = SOCKET.accept()
            connections[address[0]] = connection
        except:
            print("controller offline")
            break

def sendCommand(addr, cmd):
    conn = connections[addr]
    conn.send(bytes(cmd, FORMAT))
    return conn.recv(BUFFER_SIZE).decode(FORMAT)

def disconnectAll():
    for addr in connections:
        connections[addr].send(bytes("HOST_DISCONNECT", FORMAT))
        connections[addr].close()
    return "all connections terminated"


def main():
    thread = threading.Thread(target=acceptConnections)
    thread.start()

    print("address:command")

    while True:
        command = input(">")
        if command == "close":
            output = disconnectAll()
            break
        elif command == "connections":
            output = connections
        else:
            command = command.split(":")
            if len(command) == 2:
                output = sendCommand(command[0], command[1])
            elif len(command) > 2:
                output = sendCommand(command[0], ":".join(command[1:]))
            else:
                output = "command not recognized"
        print(output)

main()
SOCKET.close()
