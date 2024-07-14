import customtkinter as ctk
from PIL import Image
import os

global main_Path, status
status = 'idle'
main_Path = 'SpriteMenu/Frames/'
class AnimatedButton(ctk.CTkButton):

	def __init__(self, parent, Name, status):
		#animation logic setup
		self.frames=self.import_folders(Name, status)
		self.frame_index = 0
		self.animation_length = len(self.frames)-1
		self.animation_status = ctk.StringVar(value = 'start')


		super().__init__(master = parent, 
				   text = "", 
				   image=self.frames[self.frame_index], 
				   height=100, width=100,
				   command= self.infinite_animate)
		self.pack(expand = True)

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

	def enter(self):
		status = 'hover'
	def leave(self):
		status = 'idle'

	def decide_status(self, Name):
		self.bind('<Enter>', self.enter(self))
		self.bind('<Leave>', self.leave(self))
		self.import_folders(Name, status)
		self.infinite_animate()
			

	def infinite_animate(self):
		self.frame_index += 1
		self.frame_index = 0 if self.frame_index > self.animation_length else self.frame_index
		self.configure(image = self.frames[self.frame_index])
		self.after(100, self.infinite_animate)

# window 
window = ctk.CTk()
window.title('Animations')
window.geometry('300x200')

window.bind("<Enter>", AnimatedButton.decide_status(self=AnimatedButton,Name='Jerry'))

AnimatedButton(window, 'Jerry', 'hover')



# run
window.mainloop()