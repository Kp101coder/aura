import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, size):
        self.size = size
        im = Image.open(r"C:\\Users\\andyw\\Documents\\GitHub\\aura\\desktop-pet-main\\src\\sprites\\cat\\catidle.gif")
        self.frames = [ImageTk.PhotoImage(img.resize(size)) for img in ImageSequence.Iterator(im)]
        self.frame_index = 0
        tk.Label.__init__(self, master, image=self.frames[self.frame_index])
        self.after(100, self.update_frame)
    
    def update_frame(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.configure(image=self.frames[self.frame_index])
        self.after(100, self.update_frame)

root = tk.Tk()
root.geometry("200x200")

gif_path = "path_to_your_gif.gif"
animated_gif = AnimatedGIF(root, gif_path, (200, 200))
animated_gif.pack()

root.mainloop()
