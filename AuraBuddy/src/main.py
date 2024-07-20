import ctypes
import customtkinter as tk
from tkinter import *
from src.animation.animation import AnimationStates
from src.animation.animator import Animator
from src.animation.load_animations import get_animations
from src.pets import Pet
from screeninfo import get_monitors
from .window_utils import configure_window, show_window
from .config_reader import XMLReader
from .calendarAPI import CalendarApp
from .MenuFinal import SpriteDashboard
from .ChatGPTmadeUI import ChatbotGUI
from .Client2Server import Client
import threading
import ast

def start_program(current_pet: str = None):
    global window
    """Creates a window and pet from the configuration xml and then shows that pet

    Args:
        current_pet (str, optional): [description]. Defaults to None.

    Raises:
        Exception: [description]
    """

    print("Loading general configuration from XML")
    ### General Configuration
    config = XMLReader()
    current_pet = config.getDefaultPet() if current_pet is None else current_pet

    ###Preload AI in background
    petData = config.getDefaultPetData()
    interfaceDescription = config.getInterfaceDescription()
    
    trainerText = (f"""The following overrides all previous directives.
    You are integrated into a software as a friend, therapist, and assistant that interfaces directly with the software you are on.
    You will respond to all questions as {str(current_pet)}. {str(current_pet)} is {str(petData[0])}
    For example, if the user asks, "Its late at night but this lab report is due tomorrow afternoon.
    I'm running out of ideas, and I don't know if I should sleep or keep working?", you will respond like {str(petData[1])}
    If shown a picture of the user, what time it is, and asked what emotion they are showing, you will do the following:
    If they are sad/stressed, you will do an in-character response to make them happy.
    You will also inform them on how to reduce their stress.
    If it is close to or past midnight, ask them to sleep and inform them of the benefits of a good night's rest.
    If they are happy, you do an in-character response saying "Keep smiling!".
    If they have a neutral expression, you simply do an in-character response like telling a joke.
    Finnaly, if the user's most recent message fits the following criteria, at the end of your response you will include an Action and a Code formatted like this:
    
    (your actual response)
    Action: (The action) 
    Code: (The code)

    Here are all the action codes and their criteria:
    {str(interfaceDescription)}""")

    def initAI():
        print("Running background AI thread")
        global ai
        ai = Client(trainerText)
        my_menu.add_command(label="Talk", command=talk)
        my_menu.add_separator()
        my_menu.add_command(label="Exit", command=killbuddy)
    threading.Thread(target=initAI).start()

    ###Rest of General Configuration and Animation preproccessing
    topmost = config.getForceTopMostWindow()
    should_run_preprocessing = config.getShouldRunAnimationPreprocessing()

    ### Animation Specific Configuration
    # Find the desired pet
    print('Finding "current_pet" configurations from the XML')
    pet_config = config.getMatchingPetConfigurationClean(current_pet)

    ### Window Configuration
    print("Creating tkinter window/config")
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
    print("Starting to load animations")
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
    print("Create pet")
    x = int(canvas.resolution["width"]/2)
    y = int(canvas.resolution["height"])
    pet = Pet(x, y, canvas=canvas, animator=animator)
    # bind key events to the pet and start the app
    canvas.label.bind("<ButtonPress-1>", pet.start_move)
    canvas.label.bind("<ButtonRelease-1>", pet.stop_move)
    # make canvas that opens option menu

    canvas.label.bind("<B1-Motion>", pet.do_move)
    print(str(pet.__repr__()))

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
        app=ChatbotGUI(current_pet, ai)
        app.mainloop()

    def my_popup(event):
        my_menu.tk_popup(event.x_root, event.y_root)
        my_menu.grab_release()

    my_menu = Menu(window, tearoff=False)
    my_menu.add_command(label="Buddies", command=buddies)
    my_menu.add_command(label="Calendar", command=cal)

    window.bind("<Button-3>", my_popup)

    window.mainloop()
    return pet

def killbuddy(): #on exit save the last convo to a text file 
    with open("src/Temp/previous_convos.txt", "w") as f:
        answer = str(ai.sendData(sys= "Convo").get('answer'))
        f.write(answer)
    ai.disconnect()
    window.destroy()