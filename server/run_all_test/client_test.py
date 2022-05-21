import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.188.26", 65336))

print("Connected.")

data = s.recv(1024)

print("Client received data from server:")
print(data)
