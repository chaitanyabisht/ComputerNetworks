from datetime import datetime as dt
from decimal import Decimal
import matplotlib.pyplot as plt
from time import sleep
from socket import AF_INET, socket, SOCK_DGRAM, timeout


# Get parameters from user
msg_total = int(input("Enter the number of messages: "))
interval = Decimal(input("Enter the interval (in seconds): "))
buffer_size = int(input("Enter the packet size (in bytes): "))

# Create UDP socket
UDP_client_socket = socket(family = AF_INET, type = SOCK_DGRAM)
UDP_client_socket.settimeout(1)

# Send buffer size to server
set_buffer = ("B :" + str(buffer_size)).encode()
UDP_client_socket.sendto(set_buffer, ("127.0.0.1", 10001))
ack_msg = UDP_client_socket.recvfrom(buffer_size)

# Define variables
avg_throughput_lst = []
avg_delay_lst = []
time_lst = []
avg_rtt = 0
count_seconds = 0
packets_success = 0
delta = 0
seq = 1

while msg_total > 0:
    count_seconds += 1
    print("Second", count_seconds, ":")

    avg_delay = 0
    packets_success = 0

    startSecond = Decimal(dt.now().timestamp())

    while Decimal(Decimal(dt.now().timestamp()) - Decimal(startSecond)) <= 1:
        
        # Check if the value of delta
        if delta > 1:
            tosleep = 1
            delta -= 1
        else: tosleep = Decimal(delta)
    
        sleep(float(tosleep))

        # if message finished, break or if sleep is 1, break
        if msg_total == 0 or tosleep == 1: break

        UDP_client_socket.sendto(str(seq).encode(), ("127.0.0.1", 10001))
        send_time_stamp = Decimal(dt.now().timestamp())
        msg_total -= 1

        # Receive message from server
        try:
            server_msg = UDP_client_socket.recvfrom(buffer_size)
            print("Reply from Server, Seq:", server_msg[0].decode())
        except timeout:
            continue
        
        # Calculate RTT, delay and throughput
        rtt = Decimal(Decimal(dt.now().timestamp()) - send_time_stamp)
        avg_delay += Decimal(rtt)
        sleep_time = Decimal(max(interval - rtt, 0))
        seq += 1
        past_time = Decimal(Decimal(dt.now().timestamp()) - startSecond)
        interval = interval * Decimal(0.9)
        packets_success += 1

        if past_time > 1:
            delta = Decimal(tosleep)
            break
        elif past_time + sleep_time > 1 and past_time <= 1:
            tosleep = Decimal(1 - past_time)
            delta = Decimal(sleep_time - tosleep)
        else:
            tosleep = Decimal(sleep_time)
        
        sleep(float(tosleep))
        

    if packets_success == 0: avg_delay = 0
    else: avg_delay = avg_delay / packets_success
    avg_throughput = packets_success * buffer_size * 2

    avg_delay_lst.append(avg_delay)
    avg_throughput_lst.append(avg_throughput)
    time_lst.append(count_seconds)

UDP_client_socket.sendto('exit'.encode(), ("127.0.0.1", 10001))


# Plot for Average Throughput vs Time
plt.subplot(1, 2, 1)
plt.plot(time_lst, avg_throughput_lst, 'red')
plt.xlabel('Time (s)')
plt.ylabel('Average Throughput (b/s)')
plt.title('Average Throughput (b/s) vs Time (s)')


# Plot for Average Delay vs Time
plt.subplot(1, 2, 2)
plt.plot(time_lst, avg_delay_lst, 'blue')
plt.xlabel('Time (s)')
plt.ylabel('Average Delay (s)')
plt.title('Average Delay (s) vs Time (s)')

plt.show()
