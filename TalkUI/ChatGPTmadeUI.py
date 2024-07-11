import tkinter as tk
import customtkinter as ctk
from tkinter import END

class ChatbotGUI(ctk.CTk):

    def __init__(self, name):
        super().__init__()

        self.title(f"{name}'s Corner")
        self.geometry("550x600")

        # Create main frame
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.main_frame, bg = "#1c1b1b")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Input frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=20, pady=20)

        # Entry box
        self.entry = ctk.CTkEntry(self.input_frame)
        self.entry.place(rely=0.1, relx=0.0125, anchor="w")
        self.entry.bind("<Return>", self.send_message)

       # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.place(rely=.1, relx=0.9875, anchor="e")
         
        # Bind the mouse wheel to the canvas for scrolling
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_scroll(self, *args):
        self.canvas.yview_moveto(args[0])

    '''def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")'''

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

        # Scroll to the bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatbotGUI("Jerry")
    app.mainloop()
