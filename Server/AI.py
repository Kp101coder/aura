from openai import OpenAI

class Chatbot:
    def __init__(self, apiKey):
        self.client = OpenAI(api_key=apiKey)
        self.messageList = []
        self.MODEL="gpt-4o-mini"

    def question(self, question):
        """Send a question to the ChatGPT API and return the response."""
        self.messageList.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=self.messageList
        ).choices[0].message.content
        self.messageList.append({"role": "assistant", "content": response})
        return response
    
    def questionImage(self, question, imagedata):
        '''Send a question to ChatGPT along with an image for analysis'''
        messageListPicture = self.messageList.copy()
        messageListPicture.append({"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{imagedata}"}
            }
        ]})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messageListPicture,
            temperature=0.0,
        ).choices[0].message.content
        self.messageList.append({"role": "assistant", "content": response})
        return response
    
    def setTrainerText(self, text):
        if self.messageList[0].get("role") == "system":
            self.messageList[0] = {"role": "system", "content": text}
        else:
            self.messageList.insert(0, {"role": "system", "content": text})
    
    def getConvo(self): 
        '''Returns the current array of messages sent between user and AI'''
        messages = self.messageList.copy()
        if(len(messages) > 0):
            messages.pop(0)
            return messages
        return messages
    
    def cleanConvo(self): 
        '''Emptys the current array of messages except the first element. Returns the new array'''
        self.messageList = [self.messageList[0]]
        return self.messageList
    
    def setConvo(self, previousList): 
        '''Makes the current array of messages the inputted array. Returns the new array'''
        self.messageList = previousList
        return self.messageList