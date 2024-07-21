from .animation import AnimationStates
import time

class ActionHandler():
    def handle(self,response):
        if(response.get('action') == "Play Gif"):
            if(response.get('code') == "Treat"):
                self.set_animation_state(AnimationStates.GIVE_TREAT)

