import ctypes
import customtkinter as tk
from tkinter import *
from src.animation.animation import AnimationStates
from src.animation.animator import Animator
from src.animation.load_animations import get_animations
from src.pets import Pet
from screeninfo import get_monitors
from src import logger
from .window_utils import configure_window, show_window
from .config_reader import XMLReader
from .calendar import CalendarApp
from .MenuFinal import SpriteDashboard

def start_program(current_pet: str = None):
    global window
    """Creates a window and pet from the configuration xml and then shows that pet

    Args:
        current_pet (str, optional): [description]. Defaults to None.

    Raises:
        Exception: [description]
    """
    logger.debug("Loading general configuration from XML")
    ### General Configuration
    config = XMLReader()
    current_pet = config.getDefaultPet() if current_pet is None else current_pet
    topmost = config.getForceTopMostWindow()
    should_run_preprocessing = config.getShouldRunAnimationPreprocessing()

    ### Animation Specific Configuration
    # Find the desired pet
    logger.debug('Finding "current_pet" configurations from the XML')
    pet_config = config.getMatchingPetConfigurationClean(current_pet)

    ### Window Configuration
    logger.debug("Creating tkinter window/config")
    # Get info on the primary monitor (that is where the pet will be)
    monitor = get_monitors()[0]
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    offset = int(pet_config.offset + (10*((scale_factor-100)/25)))
    print("Offset: " + str(offset))
    resolution = {
        "width": int(monitor.width),
        "height": int(monitor.height - offset),
    }
    window = tk.CTk()
    canvas = configure_window(
        window, topmost=topmost, bg_color=pet_config.bg_color, resolution=resolution
    )



    ## Load the animations.
    logger.debug("Starting to load animations")
    animations = get_animations(
        current_pet, pet_config.target_resolution, should_run_preprocessing
    )

    animator = Animator(
        state=AnimationStates.IDLE, frame_number=0, animations=animations
    )

    # We esentially only need to run preprocessing once as it is really expensive to do
    # so make it false for the next time the program runs
    if should_run_preprocessing:
        config.setFirstTagValue("should_run_preprocessing", "false")
        config.save()

    ## Initialize pet
    # Create the desktop pet
    logger.debug("Create pet")
    x = int(canvas.resolution["width"]/2)
    y = int(canvas.resolution["height"])
    pet = Pet(x, y, canvas=canvas, animator=animator)
    # bind key events to the pet and start the app
    canvas.label.bind("<ButtonPress-1>", pet.start_move)
    canvas.label.bind("<ButtonRelease-1>", pet.stop_move)
    # make canvas that opens option menu

    canvas.label.bind("<B1-Motion>", pet.do_move)
    logger.info(pet.__repr__())

    # Begin the main loop
    window.after(1, pet.on_tick)
    show_window(window)
     
   
    # create menu
    def buddies():
        app = SpriteDashboard()
        app.mainloop()


    def cal():
        calendar_app = CalendarApp()
        calendar_app.mainloop()

    def talk():
        pass

    def my_popup(event):
        my_menu.tk_popup(event.x_root, event.y_root)
        my_menu.grab_release()

    my_menu = Menu(window, tearoff=False)
    my_menu.add_command(label="Buddies", command=buddies)
    my_menu.add_command(label="Calendar", command=cal)
    my_menu.add_command(label="Talk", command=talk)
    my_menu.add_separator()
    my_menu.add_command(label="Exit", command=killbuddy)

    window.bind("<Button-3>", my_popup)

    window.mainloop()
    return pet

def killbuddy():
    window.destroy()