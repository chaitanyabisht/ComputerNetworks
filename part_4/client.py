from socket import socket, AF_INET, SOCK_STREAM
from select import select
import sys
import ssl
import warnings; warnings.filterwarnings("ignore")

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket = ssl.wrap_socket(
    client_socket, server_side=False, keyfile="host.key", certfile="host.cert"
)

if len(sys.argv) != 4:
	print ("Correct usage: script, IP address, port number, your name")
	exit()

ip_addr = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

client_socket.connect((ip_addr, port))

while True:

	sockets_list = [sys.stdin, client_socket]
	r, w, e = select(sockets_list,[],[])

	for sock in r:
		if sock == client_socket:
			message = sock.recv(2048)
			if (message.decode().split(':')[0] == 'SOF'):
				file_name = message.decode().split(':')[1]
				file_name = file_name.split('.')[0] + '_download.' + file_name.split('.')[1]
				f = open(file_name, 'wb')
				while (True):
					message = sock.recv(2048)
					if (message.decode() == 'EOF'):
						f.close()
						break
					f.write(message)
				sys.stdout.write(f'File received {file_name}\n')
			else:
				print(message.decode(), end='')
		else:
			message = sys.stdin.readline()
			if (message.strip('\n') == "\exit"):
				client_socket.send(("\exit").encode())
				client_socket.close()
				exit()
			elif (message.strip('\n') == "\send"):
				file_name = sys.stdin.readline()
				client_socket.send((f"SOF:{file_name}").encode())
				file = open(file_name.strip('\n'), 'rb')
				while True:
					data = file.readline()
					if not data:
						break
					client_socket.send(data)
				file.close()
				client_socket.send(("EOF").encode())
			else:
				to_send = name + ":" + message
				client_socket.send(to_send.encode())
				sys.stdout.write("\033[1A")
				sys.stdout.write(f"<You>: {message}")
				sys.stdout.flush()
