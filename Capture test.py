from Server.AI import Chatbot

ai = Chatbot("")
image = ai.Capture()

print(ai.questionImage("What emotions is this person displaying. How can we make them happy?", image))

