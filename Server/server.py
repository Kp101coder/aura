import socket as s
import PIL.Image as Image
import io
import json
import base64
from AI import Chatbot
import threading as t
import os

APIKEY = open("apikey openai.txt", "r+").read()

HOST = s.gethostbyname(s.gethostname())
PORT = 7106
MAX_BYTES_ACCEPTED = 4096

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(100)

def handle_client(communication_socket, ai):
    print("Running handle")
    data = receive_data(communication_socket)
    data = json.loads(data)

    sysMessage = data.get('sys')
    question = data.get('question')
    image_data = data.get('image')

    print(f"Message from client: {sysMessage}")
    if sysMessage == "Quit":
        communication_socket.close()
        print("Stopping handle...")
    else:
        if sysMessage == "Convo":
            list = ai.getConvo()
            data = {}
            for i in range(len(list)):
                data[i] = list[i]
            data = json.dumps(data).encode('utf-8')
            communication_socket.send(data)
        elif image_data:
            image = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image))
            image.save("Temp/received_image" + str(count("Temp")) + ".jpg")
            print("Image received.")
            communication_socket.send(ai.questionImage(question, image_data).encode('utf-8'))
        else:
            communication_socket.send(ai.question(question).encode('utf-8'))
        handle_client(communication_socket, ai)

def count(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def receive_data(sock):
    data = b''
    while True:
        part = sock.recv(MAX_BYTES_ACCEPTED)
        data += part
        if len(part) < MAX_BYTES_ACCEPTED:
            break
    return data.decode('utf-8')
    
print("Starting Server")
while True:
    print("Listening for new connection")
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    t.Thread(target=handle_client, args=[communication_socket, Chatbot(APIKEY)]).start()