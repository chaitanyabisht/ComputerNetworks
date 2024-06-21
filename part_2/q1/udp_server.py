from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from random import randint

UDP_server_socket = socket(family = AF_INET, type = SOCK_DGRAM)
UDP_server_socket.bind(("127.0.0.1", 10001))

buffer_size = 1024

print('Server is listening for client connection')

while True:
    msg, addr = UDP_server_socket.recvfrom(buffer_size)
    msg = msg.decode()

    if (msg.split(':')[0] == 'BUFFER_SIZE'):
        buffer_size = int(msg.split(':')[1])
        print('Buffer size set to ', buffer_size, 'bytes')
        UDP_server_socket.sendto((f"BUFFER_SIZE:{buffer_size}").encode(), addr)
        continue
    elif (msg == 'exit'):
        print('Client has exited')
        continue
    
    # To simulate packet loss
    if (randint(1, 100) <= 5):
        print('Packet Dropped by the Server: ', msg)
        continue

    print('Ping from client, Seq: ', msg)
    UDP_server_socket.sendto(msg.encode(), addr)