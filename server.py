import socket

host = socket.gethostname()
port = 5000
	
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

msg = s.recv(1024)
print(msg.decode("utf-8"))
