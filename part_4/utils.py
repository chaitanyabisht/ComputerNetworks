list_of_clients = []

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients == connection:
			continue
		try:
			clients.send(message)
		except:
			clients.close()
			remove(clients)

def remove(connection): 
	if connection in list_of_clients: list_of_clients.remove(connection)

def client_thread(conn, addr):
	announcement = '<' + addr[0] + ':' + str(addr[1]) + '>' + ' has joined the chat\n'
	broadcast(announcement.encode(), conn)
	while 1:
			try:
				message = conn.recv(2048).decode()
				if message:
					if message == "\exit":
						announcement = '<' + addr[0] + ':' + str(addr[1]) + '>' + ' has left the chat\n'
						print(announcement)
						broadcast(announcement.encode(), conn)
						conn.close()
						remove(conn)
						break
					if (message.split(':')[0] == 'SOF'):
						broadcast(message.encode(), conn)
						while (True):
							message = conn.recv(2048).decode()
							if (message == 'EOF'):
								broadcast(message.encode(), conn)
								break
							broadcast(message.encode(), conn)
					name = message.split(":")[0]
					message_data = message.split(":")[1]
					print ("<" + name + "> " + message_data, end='')
					message_to_send = "<" + name + "> " + message_data
					broadcast(message_to_send.encode(), conn)
				else:
					remove(conn)
			except:
				continue