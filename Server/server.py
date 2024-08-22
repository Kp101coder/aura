import socket as s
import json
import base64
from AI import Chatbot
import threading as t
import os
import traceback
import ast
import subprocess
from config_reader import XMLReader

prints = []
print("Initializing Server")
prints.append("Initalizing Server")
APIKEY = open("apikey openai.txt", "r+").read()

HOST = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()
HOST = HOST[:HOST.find(" ")]
#Windows: HOST = s.gethostbyname(s.gethostname())
print(f"HOST: {HOST}")
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
def handle_client(communication_socket, ai, id = ""):
    try:
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
            if os.path.exists(f"previous_convos/{id}.txt"):
                with open(f"previous_convos/{id}.txt", "w") as f:
                    f.write(str(ai.getConvo()))
            else:
                with open(f"previous_convos/{id}.txt", "x") as f:
                    f.write(str(ai.getConvo()))
            print("Stopping handle...")
            prints.append("Stoppping handle...")
        else:
            if sysMessage == "Send Info":
                print("Running reader")
                prints.append("Running reader")
                communication_socket.send(str(prints).encode('utf-8'))
            elif sysMessage == "Clean All Convos":
                print("Running clean all convos")
                prints.append("Running clean all convos")
                folder_path = "previous_convos"
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)
                communication_socket.send("Done".encode('utf-8'))
            elif sysMessage == "Clean All Images":
                print("Running clean all images")
                prints.append("Running clean all images")
                folder_path = "images"
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)
                communication_socket.send("Done".encode('utf-8'))
            elif sysMessage == "View Dirs":
                print("Running view dirs")
                prints.append("Running view dirs")
                files = []
                folder_path = "images"
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    files.append(file_path)
                folder_path = "previous_convos"
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    files.append(file_path)  
                communication_socket.send(str(files).encode('utf-8'))
            elif sysMessage == "Send Bots":
                print("Running botlist")
                prints.append("Running botlist")
                allConvos = ""
                for bot in bots:
                    allConvos+=bot.getConvo()+"\n"
                communication_socket.send(str(allConvos).encode('utf-8'))
            elif sysMessage == "Convo":
                response = ai.getConvo()
                data = {
                    'answer' : response,
                    'action' : None,
                    'code' : None
                }
                communication_socket.send(json.dumps(data).encode('utf-8'))
            elif sysMessage == "Clean Convo":
                ai.cleanConvo()
            elif sysMessage == "ID":
                id = message
                if os.path.exists(f"previous_convos/{id}.txt"):
                    with open(f"previous_convos/{id}.txt", "r") as f:
                        convo = f.read()
                    if convo != "" and convo != "[]":
                        convo = ast.literal_eval(convo)
                        ai.setConvo(convo)
            elif sysMessage == "Pet":
                config = XMLReader()
                petData = config.getPetDescription(message)
                interfaceDescription = config.getInterfaceDescription()
                trainerText = (f"""You are integrated into a software as a friend, therapist, and assistant.
                You will respond to all questions as {str(message)}. {str(message)} is {str(petData[0])}
                For example, if the user asks, "Its late at night but this lab report is due tomorrow afternoon.
                I'm running out of ideas, and I don't know if I should sleep or keep working?", you will respond like {str(petData[1])}
                The current timezone for the user is {clientData.get('image')}
                Finnaly, you will interface with the users computer or this software when responding to the users most recent message that fits the following criteria.
                At the end of your response you will include an Action and a Code formatted like this:
                
                your response

                Action: The action
                Code: The code

                Here are all the action codes and their criteria:
                {str(interfaceDescription)}

                Include the action if their description matches what the user is asking and then one of the relavent codes that pertain to that action.
                For example, if you are discussing getting treats with the user and the user mention something like giving you a treat, you will include the action "Play Gif" and the "Treat" code.""")
                ai.setTrainerText(trainerText)
            else:
                image_data = clientData.get('image')
                response = None
                if image_data:
                    image = base64.b64decode(image_data)
                    with open(f"images/{id}{str(count('images', id))}.jpg", "wb") as f:
                        f.write(image)
                    print("Image received")
                    prints.append("Image recieved")
                    response = ai.questionImage(message, image_data)
                else:
                    response = ai.question(message)
                communication_socket.send(json.dumps(processResponse(response)).encode('utf-8'))
            handle_client(communication_socket, ai, id)
    except:
        e = traceback.format_exc()
        print(f"Error: {e}")
        prints.append(f"Error: {e}")

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

def count(directory, name):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if name in file:
                file_count+=1
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
global bots
bots = []
while True:
    print("Listening for new connection")
    prints.append("Listening for new connection")
    communication_socket, address = server.accept()
    print(f"Connected to {address} on {communication_socket}")
    prints.append(f"Connected to {address} on {communication_socket}")
    aibot = Chatbot(APIKEY)
    bots.append(aibot)
    t.Thread(target=handle_client, args=[communication_socket, aibot]).start()