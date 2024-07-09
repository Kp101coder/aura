import customtkinter as tk
from PIL import Image, ImageTk

class MyApp(tk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color='white')

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label_gif1 = tk.CTkLabel(self.main_frame, fg_color='white', text='')
        self.label_gif1.grid(column=0, row=0)
         
        self.gif1_frames = self._get_frames('desktop-pet-main/src/sprites/blob/slimeidle.gif')
        root.after(50, self._play_gif, self.label_gif1, self.gif1_frames)

    def _get_frames(self, img):
        with Image.open(img) as gif:
            index = 0
            frames = []
            transparent_color = gif.info.get('transparency')

            while True:
                try:
                    gif.seek(index)
                    frame = gif.convert('RGBA')
                    if transparent_color is not None:
                        datas = frame.getdata()
                        new_data = []
                        for item in datas:
                            # Change all white (also shades of whites)
                            # to transparent
                            if item[0:3] == (255, 255, 255):
                                new_data.append((255, 255, 255, 0))
                            else:
                                new_data.append(item)
                        frame.putdata(new_data)
                    frame = ImageTk.PhotoImage(frame)
                    frames.append(frame)
                except EOFError:
                    break
                index += 1
            return frames
        
    def _play_gif(self, label, frames):
        total_delay = 50
        delay_frames = 200

        for frame in frames:
            root.after(total_delay, self._next_frame, frame, label, frames)
            total_delay += delay_frames
        root.after(total_delay, self._next_frame, frame, label, frames, True)

    def _next_frame(self, frame, label, frames, restart=False):
        if restart:
            root.after(1, self._play_gif, label, frames)
            return
        
        label.configure(image=frame)


root = tk.CTk()
root.title('My App')
root.geometry('150x150')
root.resizable(width=False, height=False)

my_app_instance = MyApp(root)

root.mainloop()
