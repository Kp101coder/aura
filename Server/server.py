import socket as s

HOST = s.gethostbyname(s.gethostname())
PORT = 7106
MAX_BYTES_ACCEPTED = 1024

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(100)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    message = communication_socket.recv(MAX_BYTES_ACCEPTED).decode('utf-8')
    print(f"Message from client is: {message}")
    communication_socket.send(f"Hello!".encode('utf-8'))
    communication_socket.close()
