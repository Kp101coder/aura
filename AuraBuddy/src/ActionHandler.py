from src.pets import Pet
import os
import src.calendarAPI as c

class ActionHandler():

    pet : Pet

    def __init__(self, pet):
        self.pet = pet

    def handle(self,response):
        action : str = response.get('action')
        code : str = response.get('code')
        if(action == "Play Gif"):
            if(code == "Treat"):
                self.pet.give_treat()
        elif(action == "Calendar"):
            if("Add" in code):
                arr = code[code.find("Add")]
                c.add_event(arr[0], arr[1], arr[2], arr[3], arr[5], arr[6])
        elif(action == "Computer"): 
            os.system(code)
            # if(code == "Cancel Shutdown"):
            #     os.system("shutdown -a")
            # elif("Shutdown" in code):
            #    sec = code[code.rfind("Shutdown ")+len("Shutdown "):]
            #    os.system(f"shutdown /s /t {sec}")


