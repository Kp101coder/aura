from .animation import AnimationStates
import os

class ActionHandler():
    def handle(self,response):
        action = response.get('action')
        code = response.get('code')
        if(action == "Play Gif"):
            if(code == "Treat"):
                self.set_animation_state(AnimationStates.GIVE_TREAT)
        elif(action == "Computer"):
            if("Shutdown" in code):
               sec = code[code.rfind("Shutdown ")+len("Shutdown "):]
               os.system(f"shutdown /s /t {sec}") 


