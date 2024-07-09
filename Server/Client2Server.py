import cv2
import os
import base64
import socket as s
import json

class Client:
    def __init__(self):
        global client_socket
        global MAX_BYTES_ACCEPTED
        HOST = "192.168.3.120" #"Whats my IP"
        PORT = 7106
        MAX_BYTES_ACCEPTED = 4096
        client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

    def capture(self):
        cap = cv2.VideoCapture(0)
        frame = cap.read()
        path = "GPT-Image.jpg"
        cv2.imwrite(path, frame)
        data = None
        with open(path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')
        os.remove(path)
        return data
        
                
    def sendData(self, sys, question=None, image=None):
        print("Sending Data")
        if sys not in ["Question", "Quit", "Convo"]:
            raise Exception("You need a valid system message")
        data = {
            'sys': sys,
            'question': question,
            'image': image
        }
        data = json.dumps(data).encode('utf-8')

        client_socket.sendall(data)
        response = self.receive_response()
        print(response)
        return response

    def receive_response(self):
        data = b''
        while True:
            part = client_socket.recv(4096)
            data += part
            if len(part) < 4096:
                break
        return data.decode('utf-8')

    def disconnect(self):
        self.sendData("Quit")
        client_socket.close()
                
client = Client()
while True:
    ask = input("T: terminate, C: convo or ask question: ")
    if ask == "T":
        client.sendData("Quit")
        client.disconnect()
        break
    elif ask == "C":
        client.sendData("Convo")
    else:
        client.sendData("Question", ask)