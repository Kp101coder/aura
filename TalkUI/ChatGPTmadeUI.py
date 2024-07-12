import tkinter as tk
import customtkinter as ctk
from tkinter import END

class ChatbotGUI(ctk.CTk):

    def __init__(self, name):
        super().__init__()
        self.title(f"{name}'s Corner")
        
        self.geometry("600x600")     
        
         
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
        self.entry.pack(side = "left", pady=10, padx=10, expand=True , fill = "x")
        self.entry.bind("<Return>", self.send_message)

       # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side = "left", pady=10, padx=10)

    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message.strip() != "":
            self.create_speech_bubble(user_message, "right")
            self.entry.delete(0, END)
            bot_response = "This is a predefined response."
            self.create_speech_bubble(bot_response, "left")

    def create_speech_bubble(self, message, side):
        bubble_frame = ctk.CTkFrame(self.canvas, corner_radius=15, fg_color="#5c5b5b", width=360)
        bubble_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=250, justify="left" if side == "left" else "right")
        bubble_label.pack(padx=10, pady=5)

        if side == "left":
            bubble_frame.pack(anchor="w", padx=10, pady=5)
        else:
            bubble_frame.pack(anchor="e", padx=10, pady=5)


if __name__ == "__main__":
    app = ChatbotGUI("Jerry")
    app.mainloop()
