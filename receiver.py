import socket
from subprocess import check_output
#from cryptography.hazmat.primitives.asymmetric import rsa

SELF = socket.gethostbyname(socket.gethostname())
PORT = 5051
BUFFER_SIZE = 1024
FORMAT = "utf-8"
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((SELF, PORT))

HOST = "ENTER CONTROLLER IP ADDRESS HERE"
#using this computer's IP address temporarily for testing on the same computer
SOCKET.connect((SELF, 5050))

while True:
    command = SOCKET.recv(BUFFER_SIZE).decode(FORMAT).split(" ")
    SOCKET.send(check_output(command, shell=True))
