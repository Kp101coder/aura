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
        
    def sendData(self, code):
        print("Sending Data")
        data = {
            'sys': code,
            'message' : None,
            'image' : None
        }
        data = json.dumps(data).encode('utf-8')
        client_socket.sendall(len(data).to_bytes(4, 'big'))
        client_socket.sendall(data)
        response = str(self.__receive_response())
        return response

    def __receive_response(self):
        data = b''
        while True:
            part = client_socket.recv(MAX_BYTES_ACCEPTED)
            data += part
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
            with open("serverText.txt", "w") as f:
                self.sendData("Send Info")
                for val in ast.literal_eval():
                    f.write(val+"\n")
        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            self.getData()

if __name__ == "__main__":        
    client = ServerReader()
    while True:
        ask = input("T: Terminate, B: Bots, C: Clean Convos, I: Clean Images, V: View Images and Convos directory or Get current Server data: ").upper()
        if ask == "T":
            client.disconnect()
            break
        elif ask == "B":
            print(client.sendData("Send Bots"))
        elif ask == "C":
            print(client.sendData("Clean All Convos"))
        elif ask == "I":
            print(client.sendData("Clean All Images"))
        elif ask == "V":
            print(client.sendData("View Dirs"))
        else:
            client.getData()