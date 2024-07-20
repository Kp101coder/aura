import socket as s
import json
import base64
from AI import Chatbot
import threading as t
import os
import subprocess
import ast

prints = []
print("Initializing Server")
prints.append("Initalizing Server")
APIKEY = open("apikey openai.txt", "r+").read()

HOST = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip() 
#Windows: HOST = s.gethostbyname(s.gethostname())
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
code: (calendar stuff)

All responses sent are in json form:

answer
action
code

All responses are recived in json form:

sys
message
image

Receivable system messages are:

"Question", "Quit", "Convo", "Set Convo"
'''
def handle_client(communication_socket, ai):
    print("Running handle")
    prints.append("Running handle")
    clientData = receive_data(communication_socket)
    clientData = json.loads(clientData)

    sysMessage = clientData.get('sys')
    print(f"System Message from client: {sysMessage}")
    prints.append(f"System Message from client: {sysMessage}")
    message = clientData.get('message')
    print(f"Message from client: {message}")
    prints.append(f"Message from client: {message}")

    if sysMessage == "Quit":
        communication_socket.close()
        print("Stopping handle...")
        prints.append("Stoppping handle...")
    else:
        if address[0] == '192.168.3.1' and sysMessage == "Send Info":
            print("Running reader")
            prints.append("Running reader")
            communication_socket.send(str(prints).encode('utf-8'))
        elif sysMessage == "Convo":
            response = ai.getConvo()
            data = {
                'answer' : response,
                'action' : None,
                'code' : None
            }
            communication_socket.send(json.dumps(data).encode('utf-8'))
        elif sysMessage == "Set Convo":
            ai.setConvo(ast.literal_eval(message))
        else:
            image_data = clientData.get('image')
            response = None
            if image_data:
                image = base64.b64decode(image_data)
                with open("Temp/received_image" + str(count("Temp")) + ".jpg", "wb") as f:
                    f.write(image)
                print("Image received")
                prints.append("Image recieved")
                response = ai.questionImage(message, image_data)
            else:
                response = ai.question(message)
            communication_socket.send(json.dumps(processResponse(response)).encode('utf-8'))
        handle_client(communication_socket, ai)

def processResponse(response):
    answer = None
    action = None
    code = None

    if not response.rfind("Action: ") == -1:
        answer = response[:response.rfind("Action: ")].rstrip()
        action = response[response.rfind("Action: ")+len("Action: "):response.rfind("Code: ")].rstrip()
        if not response.rfind("Code: ") == -1:
            code = response[response.rfind("Code: ")+len("Code: "):].rstrip()
        else:
            prints.append("Code not found")
            print("Code not found")
    else:
        answer = response
        print("Action not found")
        prints.append("Action not found")

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
prints.append("Starting Server")
while True:
    print("Listening for new connection")
    prints.append("Listening for new connection")
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    prints.append(f"Connected to {address} on {communication_socket}")
    t.Thread(target=handle_client, args=[communication_socket, Chatbot(APIKEY)]).start()