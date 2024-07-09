import socket as s

HOST = s.gethostbyname(s.gethostname())
PORT = 7106

server = s.socket(s.AF_INET, s.SOCK_STREAM)
