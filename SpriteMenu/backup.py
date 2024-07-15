import customtkinter as ctk
from PIL import Image
import os

class AnimatedButton(ctk.CTkButton):

	def __init__(self, parent, Name):
		#animation logic setup
		self.name = Name
		self.status= 'idle'
		self.frames=self.import_folders()
		self.frame_index = 0
		self.animation_length = len(self.frames)-1
		self.animation_status = ctk.StringVar(value = 'start')
		
		

		super().__init__(master = parent, 
				   text = "", 
				   image=self.frames[self.frame_index], 
				   height=100, width=100)
		self.pack(expand = True)
		self.infinite_animate()

	def import_folders(self):
		file_Location_idle = 'SpriteMenu/Frames/' + self.name + "/" + self.status
		idle_list = list(os.walk(file_Location_idle))
		for _, __, image_data in idle_list:
			sorted_data = sorted(
				image_data,
				key=lambda item:int(item.split('_')[1]))
			full_path_data = ['SpriteMenu/Frames/' + self.name + '/' + self.status + '/' + item for item in sorted_data]
		ctk_images = []
		for i in range(len(full_path_data)):
			ctk_image = ctk.CTkImage(dark_image=Image.open(full_path_data[i]), size=(90,90))
			ctk_images.append(ctk_image)
		return ctk_images
			
	def not_hover(self, event=None):
		self.status = 'idle'
		self.frames=self.import_folders()
		print("notHover")

	def on_hover(self, event=None):
		self.status = 'hover'
		self.frames=self.import_folders()
		print("onHover")


	def infinite_animate(self):
		self.frame_index += 1
		self.frame_index = 0 if self.frame_index > self.animation_length else self.frame_index
		self.configure(image = self.frames[self.frame_index])
		self.after(100, self.infinite_animate)
		

# window 
window = ctk.CTk()
window.title('Animations')
window.geometry('300x200')
button = AnimatedButton(window, 'Jerry')

window.bind("<Enter>", button.on_hover)
window.bind("<Leave>", button.not_hover)


# run
window.mainloop()