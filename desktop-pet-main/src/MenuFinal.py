import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

class SpriteDashboard(ctk.CTk):
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

    def __init__(self):
        super().__init__()
        self.title("Sprite Dashboard")

        # Calculate initial window size based on three buttons in width and three rows in height
        initial_width = 3 * ((100 + 20) + 40)  # 100 is button width, 20 is padx, 40 is for margins
        initial_height = 3 * ((100 + 20))  # Initial height for three rows

        self.geometry(f"{initial_width}x{initial_height}")

        self.create_widgets()

    def load_sprites(self):
        self.sprite_buttons = []
        self.sprite_images = []

        for name, file_path in self.list():
            try:
                image = Image.open(file_path)
                frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
                frames = [frame.resize((100, 100), Image.Resampling.LANCZOS) for frame in frames]
                photos = [ImageTk.PhotoImage(frame) for frame in frames]
                button = ctk.CTkButton(self.sprite_frame, image=photos[0], text=name, compound="top")
                button.image_frames = photos  # keep a reference to avoid garbage collection
                button.image_index = 0
                button.image = photos[0]
                button.name = name  # Store the name in the button instance
                button.configure(command=lambda btn=button: self.on_sprite_button_click(btn.name))  # Bind click event
                self.sprite_buttons.append(button)
                self.sprite_images.append((button, frames))
            except Exception as e:
                print(f"Error loading image for {name}: {e}")

    def animate(self):
        for button, frames in self.sprite_images:
            button.image_index = (button.image_index + 1) % len(button.image_frames)
            button.configure(image=button.image_frames[button.image_index])
        self.after(100, self.animate)  # Adjust the interval for smoother or faster animations

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
        print(f"Clicked on sprite: {name}")

    def list(self):
        # List of sprites with names and file paths
        sprites = [
        ("Jerry", "src/sprites/blob/slimeidle.gif"),
        ("Cat", "src/sprites/blob/slimeidle.gif"),
        ("Horse", "src/sprites/blob/slimeidle.gif"),
        ("Dog", "src/sprites/blob/slimeidle.gif"),
        ("Rabbit", "src/sprites/blob/slimeidle.gif"),
        ("John", "src/sprites/blob/slimeidle.gif"),
        ("AndySucks", "src/sprites/blob/slimeidle.gif"),
        ("Harith", "src/sprites/blob/slimeidle.gif"),
        ("KrishpyDonuts", "src/sprites/blob/slimeidle.gif"),
        ("VAAYU", "src/sprites/blob/slimeidle.gif"),
        ("Aashi", "src/sprites/blob/slimeidle.gif"),
        ("Laya", "src/sprites/blob/slimeidle.gif"),
        ("Catherine", "src/sprites/blob/slimeidle.gif"),
        # Add more sprites here
    ]
        return sprites
app = SpriteDashboard()
app.mainloop()

'''if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

    # List of sprites with names and file paths
    sprites = [
        ("Jerry", "src/sprites/blob/slimeidle.gif"),
        ("Cat", "src/sprites/blob/slimeidle.gif"),
        ("Horse", "src/sprites/blob/slimeidle.gif"),
        # Add more sprites here
    ]

    app = SpriteDashboard(sprites)
    app.mainloop()'''
