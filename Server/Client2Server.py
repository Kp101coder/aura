import cv2
import os
import base64
import socket as s
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from gtts import gTTS
import time

class Client:
        def __init__(self):
                global client_socket
                global MAX_BYTES_ACCEPTED
                global cap
                HOST = "192.168.3.126"#"57.132.171.87"
                PORT = 7106
                MAX_BYTES_ACCEPTED = 8192
                client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                pygame.mixer.init()
                cap = cv2.VideoCapture(0)

        def tts(self, text, output_file='output.mp3'):
                """Convert text to speech and save it to an output file."""
                tts = gTTS(text)
                tts.save(output_file)
                return output_file

        def capture(self):
                rep, frame = cap.read()
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

                client_socket.sendall(len(data).to_bytes(4, 'big'))
                client_socket.sendall(data)
                response = self.receive_response()
                print(response)
                return response

        def receive_response(self):
                data = b''
                while True:
                        part = client_socket.recv(MAX_BYTES_ACCEPTED)
                        data += part
                        if len(part) < MAX_BYTES_ACCEPTED:
                                break
                return data.decode('utf-8')

        def disconnect(self):
                self.sendData("Quit")
                client_socket.close()

        def playSound(self, file_path):
                """Play the given audio file using pygame."""
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                        time.sleep(1)
                
client = Client()
client.sendData("Question", "What color shirt am I wearing?", client.capture())
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