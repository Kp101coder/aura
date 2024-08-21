import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageSequence
import xml.etree.ElementTree as obj
import tkinter.font as tkFont
from tktooltip import ToolTip
from .config_reader import XMLReader
from contextlib import suppress

class SpriteDashboard(ctk.CTkToplevel):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    def __init__(self):
        super().__init__()
        self.title("Sprite Dashboard")
        
        self.list = [
            ("Jerry", "src/sprites/blob/slimeidle.gif", "src/sprites/blob/slimegrabbed.gif"),
            ("Loki", "src/sprites/cat/catidle.gif", "src/sprites/cat/catgrabbed.gif"),
            ("Vaayu", "src/sprites/dog/dogidle.gif", "src/sprites/dog/doggrabbed.gif")
        ]
        
        initial_width = 377
        initial_height = 135
        self.geometry(f"{initial_width}x{initial_height}")

        self.sprite_buttons = []
        self.create_widgets()

    def load_sprites(self):
        tooltip_font = tkFont.Font(family="Space Grotesk", size=13, weight="bold")
        config = XMLReader()
        for petTuple in self.list:
            name = petTuple[0]
            file_path = petTuple[1]
            file_path_grab = petTuple[2]

            image = Image.open(file_path)
            imageGrab = Image.open(file_path_grab)
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            frames_grab = [frame.copy() for frame in ImageSequence.Iterator(imageGrab)]
            photos = [ctk.CTkImage(light_image=frame, size=(90, 90)) for frame in frames]
            photosGrab = [ctk.CTkImage(light_image=frame, size=(90, 90)) for frame in frames_grab]
            button = ctk.CTkButton(self.sprite_frame, image=photos[0], text=name, compound="top", width=100, height=100)
            button.image_frames = photos
            button.image_frames_grab = photosGrab
            button.image_index = 0
            button.status = False
            button.name = name
            button.tooltip = ToolTip(button, msg=config.getPetDescription(name), y_offset=40, font=tooltip_font)
            self.sprite_buttons.append(button)
            button.configure(command=lambda btn=button: self.on_sprite_button_click(btn.name))

            button.bind("<Enter>", lambda event, btn=button: self.on_hover(btn))
            button.bind("<Leave>", lambda event, btn=button: self.not_hover(btn))

            #this thing somehow calls an imaginary method that shows/hides the tool tip
            #doesnt even do anything wtf but without it doesnt work
            button.bind("<Enter>", lambda event, btn=button: 1)
            button.bind("<Leave>", lambda event, btn=button: 1)

    def animate(self):
        for button in self.sprite_buttons:
            if button.status:
                button.image_index = (button.image_index + 1) % len(button.image_frames_grab)
                button.configure(image=button.image_frames_grab[button.image_index])
            else:
                button.image_index = (button.image_index + 1) % len(button.image_frames)
                button.configure(image=button.image_frames[button.image_index])
        self.after(200, self.animate)

    def arrange_sprites(self):
        max_columns = 3
        current_row = 0
        current_column = 0

        for i, button in enumerate(self.sprite_buttons):
            button.grid(row=current_row, column=current_column, padx=10, pady=10, sticky="nsew")

            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        for i in range(current_row + 1):
            self.sprite_frame.grid_rowconfigure(i, weight=1)
        for j in range(max_columns):
            self.sprite_frame.grid_columnconfigure(j, weight=1)

    def create_widgets(self):
        self.sprite_canvas = ctk.CTkCanvas(self)
        self.sprite_canvas.pack(side="left", fill="both", expand=True)

        self.sprite_frame = ctk.CTkFrame(self.sprite_canvas)
        self.sprite_canvas.create_window((0, 0), window=self.sprite_frame, anchor="nw")

        self.load_sprites()
        self.arrange_sprites()

        self.sprite_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.sprite_canvas.update_idletasks()
        self.sprite_canvas.configure(scrollregion=self.sprite_canvas.bbox("all"))

        self.animate()

    def on_mousewheel(self, event):
        self.sprite_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_sprite_button_click(self, name):
        from .main import killbuddy, start_program
        tree = obj.ElementTree(file="config.xml")
        root = tree.getroot()
        
        for amounts in root.iter("defualt_pet"):
            amounts.text = name
        tree = obj.ElementTree(root)
         
        with open(file="config.xml", mode="wb") as fileupdate:
            tree.write(fileupdate)
    
        self.destroy()
        killbuddy()
        start_program()
           
    def on_hover(self, button):
        button.status = True

    def not_hover(self, button):
        button.status = False
