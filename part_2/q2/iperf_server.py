from socket import socket, AF_INET, SOCK_DGRAM

buffer_size = 1024
UDP_server_socket = socket(family = AF_INET, type = SOCK_DGRAM)
UDP_server_socket.bind(("127.0.0.1", 10001))

print("Listening on port", 10001)

while True:
    msg, addr = UDP_server_socket.recvfrom(buffer_size)
    client_msg = msg.decode()
    print("Ping from client, Seq:", client_msg)

    if client_msg[0] == 'B':
        buffer_size = int(client_msg.split(':')[1])
        UDP_server_socket.sendto((f"Buffer Size set to {buffer_size}").encode(), addr)

    elif client_msg == 'exit': print("Client has exited")
    else: UDP_server_socket.sendto(msg, addr)
