import cv2
import os
import base64
import socket as s
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from gtts import gTTS
import time
from pygame import mixer

'''
All responses sent are in json form:

sys (system message)
message
image

All responses recived are in json form:

answer
action
code

'''
"[{}, {}, {}]"
class Client:
        def __init__(self, initalMessage):
                global client_socket
                global MAX_BYTES_ACCEPTED
                global cap
                HOST = "57.132.171.87" 
                #Testing: HOST = s.gethostbyname(s.gethostname())
                PORT = 7106
                MAX_BYTES_ACCEPTED = 8192
                client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                mixer.init()
                cap = cv2.VideoCapture(0)
                self.sendData("Question", initalMessage)

        def tts(self, text, output_file='Temp/output.mp3'):
                """Convert text to speech and save it to an output file."""
                tts = gTTS(text, lang='en', tld='co.in')
                tts.save(output_file)
                self.__playSound(output_file)
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
                
                        
        def sendData(self, sys, message=None, image=None):
                print("Sending Data")
                if sys not in ["Question", "Quit", "Convo", "Set Convo"]:
                        raise Exception("You need a valid system message")
                data = {
                        'sys': sys,
                        'message': message,
                        'image': image
                }
                data = json.dumps(data).encode('utf-8')

                client_socket.sendall(len(data).to_bytes(4, 'big'))
                client_socket.sendall(data)
                response = self.__receive_response()
                response = json.loads(response)
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
                        'sys': "Quit",
                        'message': None,
                        'image': None
                }
                data = json.dumps(data).encode('utf-8')
                client_socket.sendall(len(data).to_bytes(4, 'big'))
                client_socket.sendall(data)
                client_socket.close()

        def __playSound(self, file_path):
                """Play the given audio file using pygame."""
                mixer.music.load(file_path)
                mixer.music.play()
                while mixer.music.get_busy():
                        time.sleep(1)

if __name__ == "__main__":        
        client = Client()
        while True:
                ask = input("T: terminate, C: convo, SC: set convo or ask question: ")
                if ask == "T":
                        client.disconnect()
                        break
                elif ask == "C":
                        print(client.sendData("Convo"))
                elif ask == "SC":
                        ask = input("New Convo: ")
                        client.sendData("Set Convo", ask)
                else:
                        print(client.sendData("Question", ask))