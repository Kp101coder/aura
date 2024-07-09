from openai import OpenAI
import requests

class Chatbot:
    def __init__(self, apiKey):
        global messageList
        global client
        client = OpenAI(api_key=apiKey)
        messageList = []
        

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
