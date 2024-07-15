import customtkinter as ctk
from PIL import Image, ImageSequence
import xml.etree.ElementTree as obj
import subprocess as sp
import atexit

class SpriteDashboard(ctk.CTkToplevel):
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

    def __init__(self):
        super().__init__()
        self.title("Sprite Dashboard")

        # Calculate initial window size based on three buttons in width and three rows in height
        initial_width = 377  # 100 is button width, 20 is padx, 40 is for margins
        initial_height = 135  # Initial height for three rows

        self.geometry(f"{initial_width}x{initial_height}")

        self.sprite_buttons = []
        self.sprite_images = []
        self.image_references = []  # To keep references to avoid garbage collection
        self.create_widgets()

    def load_sprites(self):
        for name, file_path in self.list():
            image = Image.open(file_path)
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            resized_frames = [frame.resize((90, 90), Image.LANCZOS) for frame in frames]  # Resize frames to 90x90
            photos = [ctk.CTkImage(light_image=frame, size=(90, 90)) for frame in resized_frames]  # Convert to CTkImage
            button = ctk.CTkButton(self.sprite_frame, image=photos[0], text=name, compound="top", width=100, height=100)
            button.image_frames = photos  # keep a reference to avoid garbage collection
            button.image_index = 0
            button.image = photos[0]
            button.name = name  # Store the name in the button instance
            button.configure(command=lambda btn=button: self.on_sprite_button_click(btn.name))  # Bind click event
            self.sprite_buttons.append(button)
            self.sprite_images.append((button, resized_frames))
            self.image_references.extend(photos)  # Store photos to avoid garbage collection

    def animate(self):
        for button, frames in self.sprite_images:
            button.image_index = (button.image_index + 1) % len(button.image_frames)
            button.configure(image=button.image_frames[button.image_index])
        self.after(200, self.animate)  # Adjust the interval for smoother or faster animations

    def arrange_sprites(self):
        max_columns = 3  # Number of buttons per row
        current_row = 0
        current_column = 0

        for i, button in enumerate(self.sprite_buttons):
            button.grid(row=current_row, column=current_column, padx=10, pady=10, sticky="nsew")

            # Update current row and column
            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        # Make all rows and columns expand equally
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

        # Bind mouse wheel event to canvas
        self.sprite_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Update canvas and scroll region
        self.sprite_canvas.update_idletasks()
        self.sprite_canvas.configure(scrollregion=self.sprite_canvas.bbox("all"))

        self.animate()  # Start animation

    def on_mousewheel(self, event):
        self.sprite_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_sprite_button_click(self, name):
        from .main import killbuddy, start_program
        tree = obj.ElementTree(file = "config.xml")
        root = tree.getroot()
        
        for amounts in root.iter("defualt_pet"):
            amounts.text= name
        tree = obj.ElementTree(root)
         
        with open(file="config.xml", mode="wb") as fileupdate:
            tree.write(fileupdate)
        
        print(f"Clicked on sprite: {name}")
        self.destroy()
        killbuddy()
        start_program()

    def list(self):
        # List of sprites with names and file paths
        sprites = [
            ("blob", "src/sprites/blob/slimeidle.gif"),
            ("cat", "src/sprites/cat/catidle.gif"),
            ("horse", "src/sprites/horse/Horse/Sleep/Sleeping/IMG_0883.GIF")
            # Add more sprites here
        ]
        return sprites
