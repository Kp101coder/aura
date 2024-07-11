from __future__ import print_function
import os
from pynput.keyboard import Key, Controller
keyboard = Controller()
from pynput.mouse import Button, Controller
mouse = Controller()
import time
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import io
import time

'''
while(True):
    print("Mouse pos: {0}".format(mouse.position))
'''

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/drive']

def search_for_file(service, name, type, parents):
    print("Searching for File")
    #application/vnd.google-apps.folder
    #text/plain
    files = []
    page_token = None
    while True:
        if parents != None:
            response = service.files().list(q="mimeType='" + type + "' and name contains '" + name + "' and parents in '" + parents + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        elif name == None:
            response = service.files().list(q="mimeType='" + type + "' and parents in '" + parents + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        else:
            response = service.files().list(q="mimeType='" + type + "' and name contains '" + name + "' and trashed=false", spaces='drive', fields='nextPageToken, ''files(id, name)',pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files[0].get('id')

def download_file(service, file_id, filepath):
    print("Downloading File")
    file = service.files().get_media(fileId=file_id).execute()
    # Write the content to a file
    with io.open(filepath, "w", encoding="utf-8") as j:
        for character in file.decode("utf-8"):
            if not character == "\n":
                j.write(character)

def mouseKeyboard():
    mouse.position = 143,18
    mouse.click(Button.left)
    mouse.release(Button.left)

    time.sleep(5)

    mouse.position = 804,89
    mouse.click(Button.left)
    mouse.release(Button.left)

    time.sleep(3)

    mouse.position = 480,280
    mouse.click(Button.left)
    mouse.release(Button.left)

    time.sleep(3)

    # Press and release space

    keyboard.type("cd \"Desktop\\Aura Server\"")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(3)

    keyboard.type("python3.11 server.py")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

creds = None
try:
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0) 
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
except:
    mouseKeyboard()
    exit()
    
serviceD = build('drive', 'v3', credentials=creds)

try:
    id = search_for_file(serviceD, "server.py", "text/x-python", search_for_file(serviceD, "Server Update", "application/vnd.google-apps.folder", None))
    if os.path.exists("server.py"):
        os.remove("server.py")
    download_file(serviceD, id, "server.py")
    time.sleep(5)
    print("Updated")
except:
    print("No update")

mouseKeyboard()