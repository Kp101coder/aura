import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk, ImageSequence

class SpriteMenu (ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sprite Menu")
        
        self.geometry("600x600") 
        self.resizable(False,False)
         
        bgColor = "#2a2b2b"
         
        #main rows and columns
        self.columnconfigure(0,weight=10)
        self.rowconfigure(0, weight=10)
         
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=0,column=0, sticky="nsew")

        #scroll columns and rows
        scroll_frame.columnconfigure(0, pad=20,weight=5)
        scroll_frame.columnconfigure(1, pad=20,weight=5)
        scroll_frame.columnconfigure(2, pad=20,weight=5)

        scroll_frame.rowconfigure(0)
        scroll_frame.rowconfigure(1)
        scroll_frame.rowconfigure(2)
        scroll_frame.rowconfigure(3)
         
        #scroll frame
        canvas = ctk.CTkFrame(scroll_frame, width=150, height=200, border_width= 3, border_color="#5c5b5b", fg_color=bgColor)   
        canvas.grid(row=0, column=0)
        canvas2 = ctk.CTkFrame(scroll_frame, width=150, height=200, border_width= 3, border_color="#5c5b5b", fg_color=bgColor)   
        canvas2.grid(row=0, column=1)
        canvas3 = ctk.CTkFrame(scroll_frame, width=150, height=200, border_width= 3, border_color="#5c5b5b", fg_color=bgColor)   
        canvas3.grid(row=0, column=2)
         
        nameButton = ctk.CTkButton(canvas, width= 135, text="Jerry")
        nameButton.place(relx=0.499, rely=0.9, anchor="center")
        

if __name__ == "__main__":
    app = SpriteMenu()
    app.mainloop()
