import tkinter as tk
from .animation import Animation, AnimationStates, Animator
from .pets.interactable_pet import InteractablePet
from .main import pet
from .animation import AnimationStates
import os

class ActionHandler():

    animator: Animator

    def handle(self,response):
        action = response.get('action')
        code = response.get('code')
        if(action == "Play Gif"):
            if(code == "Treat"):
                
        elif(action == "Computer"):
            if("Shutdown" in code):
               sec = code[code.rfind("Shutdown ")+len("Shutdown "):]
               os.system(f"shutdown /s /t {sec}") 


