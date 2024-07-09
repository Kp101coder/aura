import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

class SpriteDashboard(ctk.CTk):
    def __init__(self, sprites, hover_animations):
        super().__init__()
        self.title("Sprite Dashboard")
        self.sprites = sprites
        self.hover_animations = dict(hover_animations)  # Convert hover_animations to a dictionary

        # Calculate initial window size based on three buttons in width and three rows in height
        initial_width = 3 * ((100 + 20) + 40)  # 100 is button width, 20 is padx, 40 is for margins
        initial_height = 3 * ((100 + 20))  # Initial height for three rows

        self.geometry(f"{initial_width}x{initial_height}")

        self.create_widgets()

    def load_sprites(self):
        self.sprite_buttons = []
        self.sprite_images = []

        for name, file_path in self.sprites:
            try:
                image = Image.open(file_path)
                frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
                frames = [frame.resize((100, 100), Image.Resampling.LANCZOS) for frame in frames]
                photos = [ImageTk.PhotoImage(frame) for frame in frames]
                button = ctk.CTkButton(self.sprite_frame, image=photos[0], text=name, compound="top")
                button.image_frames = photos  # keep a reference to avoid garbage collection
                button.image_index = 0
                button.image = photos[0]
                button.default_file_path = file_path  # Set default file path
                button.hover_file_path = self.hover_animations.get(name, file_path)  # Set hover file path
                button.bind("<Enter>", self.on_enter)
                button.bind("<Leave>", self.on_leave)
                self.sprite_buttons.append(button)
                self.sprite_images.append((button, frames))
            except Exception as e:
                print(f"Error loading image for {name}: {e}")

    def on_enter(self, event):
        button = event.widget
        if button.hover_file_path:
            try:
                image = Image.open(button.hover_file_path)
                frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
                frames = [frame.resize((100, 100), Image.Resampling.LANCZOS) for frame in frames]
                photos = [ImageTk.PhotoImage(frame) for frame in frames]
                button.image_frames = photos
                button.image_index = 0
                button.configure(image=photos[0])  # Start with the first frame of hover animation
            except Exception as e:
                print(f"Error loading hover image for {button.cget('text')}: {e}")

    def on_leave(self, event):
        button = event.widget
        try:
            image = Image.open(button.default_file_path)
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            frames = [frame.resize((100, 100), Image.Resampling.LANCZOS) for frame in frames]
            photos = [ImageTk.PhotoImage(frame) for frame in frames]
            button.image_frames = photos
            button.image_index = 0
            button.configure(image=photos[0])  # Start with the first frame of default animation
        except Exception as e:
            print(f"Error loading default image for {button.cget('text')}: {e}")

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

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

    # List of sprites with names and file paths
    sprites = [
        ("Jerry", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Cat", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Horse", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Dog", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Rabbit", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("John", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("AndySucks", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Harith", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("KrishpyDonuts", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("VAYU", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Aashi", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Laya", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        ("Catherine", "desktop-pet-main/src/sprites/blob/slimeidle.gif"),
        # Add more sprites here
    ]

    # List of hover animations with names and file paths
    hover_animations = [
        ("Jerry", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Cat", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Horse", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Dog", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Rabbit", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("John", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("AndySucks", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Harith", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("KrishpyDonuts", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("VAYU", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Aashi", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Laya", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        ("Catherine", "desktop-pet-main/src/sprites/blob/slimegrabbed.gif"),
        # Add more hover animations here
    ]

    app = SpriteDashboard(sprites, hover_animations)
    app.mainloop()
