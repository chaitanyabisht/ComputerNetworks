from _thread import start_new_thread as thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
from utils import *
import ssl
import warnings; warnings.filterwarnings("ignore")

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server_socket = ssl.wrap_socket(
    server_socket, server_side=True, keyfile="host.key", certfile="host.cert"
)

if len(sys.argv) != 3:
	print ("Usage: python3 server.py <hostname> <port>")
	exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])

server_socket.bind((ip, port))
server_socket.listen(100)

print("Server started on port", port)

while 1:
	conn, addr = server_socket.accept()
	list_of_clients.append(conn)
	print('<'+addr[0] + ':' + str(addr[1]) + '> joined the chat')
	thread(client_thread,(conn,addr))	

