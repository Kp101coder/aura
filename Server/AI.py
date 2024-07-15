from openai import OpenAI
import requests

class Chatbot:
    def __init__(self, apiKey):
        self.client = OpenAI(api_key=apiKey)
        self.messageList = []
        

    def question(self, question):
        """Send a question to the ChatGPT API and return the response."""
        self.messageList.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messageList
        )
        self.messageList.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content

    def questionImage(self, question, imagedata):
        '''Send a question to ChatGPT along with an image for analysis'''
        # Getting the base64 string
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.client.api_key}"
        }
        self.messageList.append({"role": "user", "content": question})
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
        self.messageList.append({"role": "assistant", "content": response})
        return response
    
    def getConvo(self): 
        '''Returns the current array of messages sent between user and AI'''
        return self.messageList
    
    def setConvo(self, previousList): 
        '''Makes the current array of messages the inputted array. Returns the new array'''
        self.messageList = previousList
        return self.messageList