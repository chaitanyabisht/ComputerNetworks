from socket import SOCK_STREAM, socket, AF_UNSPEC, getaddrinfo

host = input('Enter host [ip6-localhost, localhost]: ')
port = input('Enter port [8000]: ') # 8000

if host == '': host = 'ip6-localhost'
if port == '': port = 8000

server_socket = None

for addr_family, socket_type, protocol, cn, socket_address in getaddrinfo(host, port, AF_UNSPEC, SOCK_STREAM):
    try:
        server_socket = socket(addr_family, socket_type, protocol)
        server_socket.bind(socket_address)
        server_socket.listen(1)
        print(f'Socket: {addr_family, socket_type, protocol, cn, socket_address}')
        break
    except:
        print('Unable to create socket.')
        exit()

client, address = server_socket.accept()

print(f'Connected to: {address[0]}:{address[1]}')

while 1:
    message = client.recv(1024)
    if message:
        print(f'Received message: {message.decode()}')
        client.send(message)
    else:
        print(f'Disconnected from: {address[0]}:{address[1]}')
        client.close()
        break
