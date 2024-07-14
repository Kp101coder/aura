import customtkinter as ctk
from PIL import Image
import os

global main_Path 
main_Path = 'SpriteMenu/Frames/'
class UI(ctk.CTk):

	def __init__(self, Name, status):
		super().__init__()
		self.title('Animations')
		self.geometry('300x200')

		self.AnimatedButton = ctk.CTkButton(master = self, 
				   text = "", 
				   image=self.frames[self.frame_index], 
				   height=100, width=100,
				   command= self.infinite_animate)
		self.AnimatedButton.pack(expand = True)

		#animation logic setup
		self.frames=self.import_folders(Name, status)
		self.frame_index = 0
		self.animation_length = len(self.frames)-1
		self.animation_status = ctk.StringVar(value = 'start')


		
	def import_folders(self, Name, status):
		file_Location_idle = main_Path + Name + "/" + status
		idle_list = list(os.walk(file_Location_idle))
		for _, __, image_data in idle_list:
			sorted_data = sorted(
				image_data,
				key=lambda item:int(item.split('_')[1]))
			full_path_data = [main_Path + Name + '/' + status + '/' + item for item in sorted_data]
		ctk_images = []
		for i in range(len(full_path_data)):
			ctk_image = ctk.CTkImage(dark_image=Image.open(full_path_data[i]), size=(90,90))
			ctk_images.append(ctk_image)
		return ctk_images


	def infinite_animate(self):
		self.frame_index += 1
		self.frame_index = 0 if self.frame_index > self.animation_length else self.frame_index
		self.configure(image = self.frames[self.frame_index])
		self.after(100, self.infinite_animate)

# window 
if __name__ == "__main__":
    app = UI("Jerry", 'idle')
    app.mainloop()
'''window = ctk.CTk()
window.title('Animations')
window.geometry('300x200')


def hover_animation():
	Stat = 'hover'
	AnimatedButton(window, 'Jerry', Stat)
def normal_animation():
	Stat = 'idle'
	AnimatedButton(window, 'Jerry', Stat)

AnimatedButton(window, 'Jerry', 'idle')
AnimatedButton.bind("<Enter>", hover_animation)
AnimatedButton.bind("<Leave>", normal_animation)



# run
window.mainloop()'''