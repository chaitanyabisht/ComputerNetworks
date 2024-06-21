from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

UDP_client_socket = socket(family = AF_INET, type = SOCK_DGRAM)
UDP_client_socket.settimeout(1)

buffer_size = 1024

file_name = input("Enter file name: ")

UDP_client_socket.sendto(("FILE_NAME:"+file_name).encode(), ("127.0.0.1", 10001))


next = 1
f = open(file_name.split('.')[0] + "_server." + file_name.split('.')[1], 'w')
while True:
    msg, addr = UDP_client_socket.recvfrom(buffer_size)
    msg = msg.decode()

    if msg == 'FNF':
        print("File not found on server")
        break
    elif msg == 'EOF':
        f.write('EOF')
        f.close()
        print('Recieved EOF from server')
        print('Transfer complete')
        break
    
    f.write(msg)
    msg = msg.strip("\n")
    print(f'Received {msg} from server')
    next += 1
    sleep(1)

    UDP_client_socket.sendto(str(next).encode(), ("127.0.0.1", 10001))
    print(f'Requested Word#{next} to server')
    

    sleep(2)
