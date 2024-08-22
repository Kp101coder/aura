import cv2
import os
import base64
import socket as s
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from gtts import gTTS
import time
from pygame import mixer
from time import strftime, time

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
class Client:
        def __init__(self, id, pet):
                HOST = "57.132.171.87" 
                #Testing: 
                HOST = s.gethostbyname(s.gethostname())
                PORT = 7106
                self.MAX_BYTES_ACCEPTED = 2048
                self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
                self.client_socket.connect((HOST, PORT))
                mixer.init()
                self.cap = cv2.VideoCapture(0)
                self.setPet(pet)
                self.sendID(id)

        def tts(self, text, output_file='Temp/output.mp3'):
                """Convert text to speech and save it to an output file."""
                tts = gTTS(text, lang='en', tld='co.in')
                tts.save(output_file)
                self.__playSound(output_file)
                return output_file

        def capture(self):
                rep, frame = self.cap.read()
                path = "GPT-Image.jpg"
                cv2.imwrite(path, frame)
                data = None
                with open(path, "rb") as image_file:
                        data = base64.b64encode(image_file.read()).decode('utf-8')
                os.remove(path)
                return data
        
        def sendData(self, sys, message=None, image=None) -> dict:
                print("Sending Data")
                if sys not in ["Question", "Quit", "Convo"]:
                        raise Exception("You need a valid system message")
                data = {
                        'sys': sys,
                        'message': message,
                        'image': image
                }
                print(f"Data: {data}")
                data = json.dumps(data).encode('utf-8')
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)
                response = self.__receive_response()
                response = json.loads(response)
                print(f"Response: {response}")
                return response
        
        def cleanConvo(self):
                print("Sending ID Data")
                data = {
                        'sys': "Clean Convo",
                        'message': None,
                        'image': None
                }
                print(f"Data: {data}")
                data = json.dumps(data).encode('utf-8')
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)
        
        def setPet(self, message):
                print("Sending Pet Data")
                data = {
                        'sys': "Pet",
                        'message': message,
                        'image': strftime("%Z")
                }
                print(f"Data: {data}")
                data = json.dumps(data).encode('utf-8')
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)

        def sendID(self, message):
                print("Sending ID Data")
                data = {
                        'sys': "ID",
                        'message': message,
                        'image': None
                }
                print(f"Data: {data}")
                data = json.dumps(data).encode('utf-8')
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)

        def __receive_response(self):
                data = b''
                while True:
                        part = self.client_socket.recv(self.MAX_BYTES_ACCEPTED)
                        data += part
                        if len(part) < self.MAX_BYTES_ACCEPTED:
                                break
                return data.decode('utf-8')

        def disconnect(self):
                data = {
                        'sys': "Quit",
                        'message': None,
                        'image': None
                }
                data = json.dumps(data).encode('utf-8')
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)
                self.client_socket.close()

        def __playSound(self, file_path):
                """Play the given audio file using pygame."""
                mixer.music.load(file_path)
                mixer.music.play()
                while mixer.music.get_busy():
                        time.sleep(1)

if __name__ == "__main__":        
        client = Client()
        while True:
                ask = input("T: terminate, C: convo, SC: set convo , P: Pic and question, or ask question: ")
                if ask.upper() == "T":
                        client.disconnect()
                        break
                elif ask.upper() == "C":
                        print(client.sendData("Convo"))
                elif ask.upper() == "SC":
                        ask = input("New Convo: ")
                        client.sendData("Set Convo", ask)
                elif ask.upper() == "P":
                        ask = input("Question: ")
                        print(client.sendData("Question", ask, client.self.capture()).get('answer'))
                else:
                        print(client.sendData("Question", ask).get('answer'))