from openai import OpenAI
import requests
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import base64
import cv2

class Chatbot:
    def __init__(self, apiKey):
        global messageList
        global client
        client = OpenAI(api_key=apiKey)
        messageList = []
        pygame.mixer.init()

    def question(self, question):
        """Send a question to the ChatGPT API and return the response."""
        global messageList
        global client
        messageList.append({"role": "user", "content": question})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messageList
        )
        messageList.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content

    def tts(self, text, output_file='output.mp3'):
        """Convert text to speech and save it to an output file."""
        tts = gTTS(text)
        tts.save(output_file)
        return output_file

    def playSound(self, file_path):
        """Play the given audio file using pygame."""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def questionImage(self, question, imagedata):
        '''Send a question to ChatGPT along with an image for analysis'''
        global messageList
        global client
        # Getting the base64 string
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.api_key}"
        }
        messageList.append({"role": "user", "content": question})
        payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": question
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{imagedata}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()['choices'][0]['message']['content']
        messageList.append({"role": "assistant", "content": response})
        return response
    
    def getConvo(self):
        global messageList
        return messageList
