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
               os.system(f"shutdown /s /t {code[code.rfind("Shutdown ")+len("Shutdown "):]}") 


