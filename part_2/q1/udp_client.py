from socket import AF_INET
from socket import socket
from socket import SOCK_DGRAM
from time import sleep
from datetime import datetime



server_IP_address_port = ("127.0.0.1", 10001)
UDP_client_socket = socket(family = AF_INET, type = SOCK_DGRAM)
UDP_client_socket.settimeout(1)


msg_count = int(input("Enter the number of echo messages to be sent: "))

interval = float(input("Enter the interval: "))

buffer_size = int(input("Enter the packet size in bytes: "))

print('Sending server size of buffer')

buffer_msg = ("BUFFER_SIZE:" + str(buffer_size)).encode()
UDP_client_socket.sendto(buffer_msg, server_IP_address_port)
ack_msg = UDP_client_socket.recvfrom(buffer_size)

if (ack_msg[0].decode().split(':')[0] == 'BUFFER_SIZE'):
    print('Buffer size set to ', ack_msg[0].decode().split(':')[1], 'bytes')
else:
    print('[Invalid ACK] Buffer size failed to set')
    exit()


avg_rtt = 0
packets_success = 0


for msg_count in range(1, msg_count + 1):
    print("Pinging Server, Seq:", msg_count, "of size", buffer_size, "bytes")
    send_time = datetime.now().timestamp()
    UDP_client_socket.sendto(str(msg_count).encode(), server_IP_address_port)
    try:
        msg = UDP_client_socket.recvfrom(buffer_size)
        print('Reply from server, Seq: ', msg[0].decode(), end='')
    except:
        print('Packet Lost, Seq: ', msg_count)
        continue

    packets_success += 1

    recieve_time = datetime.now().timestamp()

    rtt = recieve_time - send_time
    print(', RTT: ', rtt, 'seconds')
    avg_rtt += rtt

    sleep(max(0, interval - rtt))


UDP_client_socket.sendto('exit'.encode(), server_IP_address_port)

print()
print('Average RTT: ', avg_rtt/packets_success, 'seconds')
print('Packets Dropped: ', msg_count - packets_success)
print('Packets Success: ', packets_success)
print('Loss Percentage: ', (msg_count - packets_success)/msg_count * 100, '%')
