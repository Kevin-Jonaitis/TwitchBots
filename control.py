import socket
while(True):
	control_socket = socket.socket()
	control_socket.connect(('localhost',1234))
	key = raw_input("Move:")
	control_socket.send(key)
	control_socket.shutdown(0)
	control_socket.close()
