import socket as s
import io
import json
import base64
from AI import Chatbot
import threading as t
import os
import subprocess

APIKEY = open("apikey openai.txt", "r+").read()

HOST = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip() #Windows: s.gethostbyname(s.gethostname())
print(HOST)
PORT = 7106
MAX_BYTES_ACCEPTED = 4096

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(100)

'''
Actions are when gpt interprets the user requesting it to interface directly with their system.
When GPT interprets an action, it adds a special string to the response.
This string tells the user the next thing is an action.
the action is a string indicates a specific operation like changing character
The code loads that action into the output json.
After the action is the code which tells the specifcs of the action and is also loaded into the json.

For example:
action: Add Calendar Event
code: 

All responses sent are in json form:

answer
action
code

'''

def handle_client(communication_socket, ai):
    print("Running handle")
    clientData = receive_data(communication_socket)
    clientData = json.loads(clientData)

    sysMessage = clientData.get('sys')
    question = clientData.get('question')
    image_data = clientData.get('image')

    print(f"Message from client: {sysMessage}\nQuestion: {question}")
    if sysMessage == "Quit":
        communication_socket.close()
        print("Stopping handle...")
    else:
        response = None
        if sysMessage == "Convo":
            response = str(ai.getConvo())
        elif image_data:
            image = base64.b64decode(image_data)
            with open("Temp/received_image" + str(count("Temp")) + ".jpg", "wb") as f:
                f.write(image)
            print("Image received.")
            response = ai.questionImage(question, image_data)
        else:
            response = ai.question(question)
        communication_socket.send(json.dumps(processResponse(response)).encode('utf-8'))
        handle_client(communication_socket, ai)

def processResponse(response):
    answer = None
    action = None
    code = None

    if not response.rfind("Action: ") == -1:
        answer = response[:response.rfind("Action: ")]
        action = response[response.rfind("Action: "):response.rfind("Code: ")]
        if not response.rfind("Code: ") == -1:
            code = response[response.rfind("Code: "):]
        else:
            print("Code not found")
    else:
        answer = response
        print("Action not found")

    data = {
        'answer' : answer,
        'action' : action,
        'code' : code
    }
    return data

def count(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def receive_data(sock):
    # First, read the length of the JSON data (4 bytes)
    data_length = int.from_bytes(sock.recv(4), 'big')
    
    # Now, read the actual JSON data
    data = b''
    while len(data) < data_length:
        part = sock.recv(min(data_length - len(data), MAX_BYTES_ACCEPTED))
        data += part
    return data.decode('utf-8')
    
print("Starting Server")
while True:
    print("Listening for new connection")
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    t.Thread(target=handle_client, args=[communication_socket, Chatbot(APIKEY)]).start()
