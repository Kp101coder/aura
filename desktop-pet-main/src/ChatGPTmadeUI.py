import tkinter as tk
import customtkinter as ctk
from tkinter import END
from Client2Server import Client
import ast



class ChatbotGUI(ctk.CTk):

    def __init__(self, name, ai):
        
        super().__init__()
        self.title(f"{name}'s Corner")
        
        self.geometry("600x600")     
        
        
        self.client = ai

        #padding grids
        self.rowconfigure(0, weight=1)    
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)    
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0,weight=1)

        self.columnconfigure(1,weight=13)
        self.columnconfigure(2,weight=1)
        
        bgColor = "#2a2b2b"

        # Create main frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, border_width= 3, border_color="#5c5b5b", fg_color=bgColor)
        self.scroll_frame.grid(row=1,column=1, sticky="nsew")
        
        
        self.canvas = tk.Canvas(self.scroll_frame, bg =bgColor, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Input frame
        self.input_frame = ctk.CTkFrame(self, fg_color = bgColor, border_width= 3, border_color="#5c5b5b")
        self.input_frame.grid(row=3,column=1, sticky="nsew")

        # Entry box
        self.entry = ctk.CTkEntry(self.input_frame, width = 395)
        self.entry.xview_scroll(4, tk.UNITS)
        self.entry.pack(side = "left", pady=10, padx=10, expand=True , fill = "x")
        self.entry.bind("<Return>", self.send_message)

    # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side = "right", pady=10, padx=10)
    #New entry
       # self.entry = ctk.CTkTextbox(self.input_frame, height=20, wrap = 'word')
       # self.entry.pack(side = "left", pady=10, padx=10, expand=True, fill = "x")
       # self.entry.bind("<Return>", self.send_message)


#make button for prev conversaiont
#make text file that saves previous convos
#use ast.literal_eval(message))
#and load those text messages back in the speech bubble format
#also load the face of the blob up and everything and maybe make a blob thought bubble show up

    def send_message(self, event=None):
        user_message = self.entry.get()#1.0, END for text box
        #self.entry.delete(1.0, END) for text box
        if user_message.strip() != "":
            self.create_speech_bubble(user_message, "right")
            self.entry.delete(0, END)
            self.update()
            response = self.client.sendData(sys="Question", message=user_message)
            bot_response = response.get('answer')
            self.create_speech_bubble(bot_response, "left")

    def create_speech_bubble(self, message, side):
        bubble_frame = ctk.CTkFrame(self.canvas, corner_radius=15, fg_color="#5c5b5b", width=360)
        bubble_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=250, justify="left" if side == "left" else "right")
        bubble_label.pack(padx=10, pady=5)

        if side == "left":
            bubble_frame.pack(anchor="w", padx=10, pady=5)
        else:
            bubble_frame.pack(anchor="e", padx=10, pady=5)
        self.update_idletasks()
        self.scroll_frame._parent_canvas.yview_moveto(1.0)
        

if __name__ == "__main__":
    app = ChatbotGUI("Jerry", ai = Client())
    app.mainloop()
