import socket as s
import json
import ast

class ServerReader:
    def __init__(self):
        global client_socket
        global MAX_BYTES_ACCEPTED
        HOST = "57.132.171.87"
        #Testing: HOST = s.gethostbyname(s.gethostname())
        PORT = 7106
        MAX_BYTES_ACCEPTED = 2048
        client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.settimeout(30)
        
    def sendData(self):
        print("Sending Data")
        data = {
            'sys': "Send Info",
            'message' : None,
            'image' : None
        }
        data = json.dumps(data).encode('utf-8')
        client_socket.sendall(len(data).to_bytes(4, 'big'))
        client_socket.sendall(data)
        response = self.__receive_response()
        return response

    def __receive_response(self):
        data = b''
        while True:
            part = client_socket.recv(MAX_BYTES_ACCEPTED)
            print(f"Part Len: {len(part)}")
            data += part
            print(f"Part: {part}")
            if len(part) < MAX_BYTES_ACCEPTED:
                break
        return data.decode('utf-8')

    def disconnect(self):
        data = {
            'sys': "Quit"
        }
        data = json.dumps(data).encode('utf-8')
        client_socket.sendall(len(data).to_bytes(4, 'big'))
        client_socket.sendall(data)
        client_socket.close()

    def getData(self):
        try:
            for val in ast.literal_eval(self.sendData()):
                print(val) 
        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            self.getData()

if __name__ == "__main__":        
    client = ServerReader()
    while True:
        ask = input("T: Terminate or Get current Server data: ").upper()
        if ask == "T":
            client.disconnect()
            break
        else:
            client.getData()