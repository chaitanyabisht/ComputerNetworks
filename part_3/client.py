from socket import AF_UNSPEC
from socket import getaddrinfo
from socket import SOCK_STREAM
from socket import socket

host = input('Enter host [ip6-localhost, localhost]: ')
port = input('Enter port [8000]: ')
message = input('Enter message: ')

if host == '': host = 'ip6-localhost'
if port == '': port = 8000

server_socket = None

for addr_family, socket_type, protocol, cn, socket_address in getaddrinfo(host, port, AF_UNSPEC, SOCK_STREAM):
    try:
        server_socket = socket(addr_family, socket_type, protocol)
        server_socket.connect(socket_address)
        print(f'Socket: {addr_family, socket_type, protocol, cn, socket_address}')
        break
    except:
        print('Unable to create socket.')
        exit()

print(f'Sending message: {message}')

server_socket.send(message.encode())

response = server_socket.recv(1024)

print(f'Reply from Server: {response.decode()}')

server_socket.close()
