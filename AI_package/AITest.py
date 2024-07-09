from AI import Chatbot

ai = Chatbot("")

while(True):
    choice = input("0: Break, 1: Question, 2: Image and Question: ")
    print()
    if(choice == "0"):
        break
    elif(choice == "1"):
        print(ai.question(input("Enter question: ")))
        print()
    elif(choice == "2"):
        print(ai.questionImage(input("Enter question: "), input("Enter relative filepath: ")))
        print()
        
print("\n\n")
print(ai.getConvo())
with open("AI/output.txt", "w+") as f:
    f.write(str(ai.getConvo()))