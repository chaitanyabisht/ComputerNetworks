from socket import AF_INET
from socket import socket
from socket import SOCK_DGRAM
from socket import timeout
from time import sleep


server_IP_address_port = ("127.0.0.1", 10001)
UDP_server_socket = socket(family = AF_INET, type = SOCK_DGRAM)

buffer_size = 1024

UDP_server_socket.bind(server_IP_address_port)

print('Server is listening on port 10001')
ptr = None
f = None
while True:
    msg, addr = UDP_server_socket.recvfrom(buffer_size)
    msg = msg.decode()

    if msg.split(':')[0] == 'FILE_NAME':
        print(f'File name requested: {msg.split(":")[1]}')
        try:
            f = open(msg.split(':')[1], 'r')
            ptr = 1
        except:
            UDP_server_socket.sendto('FNF'.encode(), addr)
            f.close()
            print('File not found on server')
            continue
        ptr = 1
    else:
        ptr = msg

    message = f.readline()
    if message.strip('\n') == 'EOF':
        UDP_server_socket.sendto('EOF'.encode(), addr)
        print('Sent EOF to client')
        print('Transfer complete')
        f.close()
        continue
    
    UDP_server_socket.sendto(str(message).encode(), addr)
    print(f'Sent Word#{ptr} to client')
    sleep(3)
