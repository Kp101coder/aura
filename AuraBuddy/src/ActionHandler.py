#import statements needed

class ActionHandler():
    def handle(self,response):
        if(response.get('action') == "Play Gif"):
            if(response.get('code') == "Treat"):
                #play aimation treat