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
from .chatUI import ChatbotGUI
from .Client2Server import Client
from .ActionHandler import ActionHandler
import os
import threading
from time import strftime, time
import ast

def start_program():
    global window

    def initAI():
        global ai
        print("Starting background")
        try:
            if os.path.exists("src/Temp/userId.txt"):
                with open("src/Temp/userId.txt", "r") as f:
                    ai = Client(f.read().rstrip(), current_pet)
            else:
                key = ""
                with open("src/Temp/userId.txt", "w+") as f:
                    import secrets
                    password_length = 13
                    key = secrets.token_urlsafe(password_length)
                    f.write(key)
                ai = Client(key, current_pet)
            my_menu.add_command(label="Talk", command=talk)
        except Exception as e:
            print(e)
        my_menu.add_separator()
        my_menu.add_command(label="Exit", command=killbuddy)

    
    """Creates a window and pet from the configuration xml and then shows that pet

    Args:
        current_pet (str, optional): [description]. Defaults to None.

    Raises:
        Exception: [description]
    """

    print("Loading general configuration from XML")
    ### General Configuration
    config = XMLReader()
    current_pet = config.getDefaultPet()

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

    def check_ai_response():
        try:
            response = ai.sendData("Question", 
            f"""What emotion is this person showing? 
            If they are sad/stressed, you will do an in-character response to make them happy, make sure to include the phrase, "you look sad".
            You will also inform them on how to reduce their stress.
            If it is close to or past midnight, ask them to sleep and inform them of the benefits of a good night's rest.
            If they are happy, you do an in-character response saying "Keep smiling!".
            If they have a neutral expression, you simply do an in-character response like telling a joke.
            The current time is: {strftime("%I:%M:%p")}""", ai.capture())
            if "you look sad" in response.get('answer').lower():
                if os.path.exists("src/Temp/previous_convos.txt"):
                    convo = ""
                    with open("src/Temp/previous_convos.txt", "r") as f:
                        convo = f.read()
                        if convo != "" and convo != "[]":
                            convo = ast.literal_eval(convo)
                            convo.append({'role': 'assistant', 'content': response.get('answer')})
                    with open("src/Temp/previous_convos.txt", "w") as f:
                        f.write(str(convo))
                else:
                    with open("src/Temp/previous_convos.txt", "x") as f:
                        f.write([{'role': 'assistant', 'content': response.get('answer')}])
                talk()

            window.after(600000, check_ai_response)
        except:
            window.after(1000, check_ai_response)

    window.after(00000, check_ai_response)

    # Begin the main loop
    window.after(1, pet.on_tick)
    show_window(window)

    def talk():
        app=ChatbotGUI(current_pet, ai, ActionHandler(pet))
        app.focus()
        app.mainloop()

    # create menu
    def buddies():
        app = SpriteDashboard()
        app.mainloop()

    def cal():
        app = CalendarApp()
        app.mainloop()

    def my_popup(event):
        my_menu.tk_popup(event.x_root, event.y_root)
        my_menu.grab_release()

    my_menu = Menu(window, tearoff=False)
    my_menu.add_command(label="Buddies", command=buddies)
    my_menu.add_command(label="Calendar", command=cal)

    threading.Thread(target=initAI).start()

    window.bind("<Button-3>", my_popup)

    window.mainloop()
    return pet

def killbuddy(): #on exit save the last convo to a text file 
    window.destroy()
    if os.path.exists("src/Temp/previous_convos.txt"):
        with open("src/Temp/previous_convos.txt", "w", encoding='utf-8') as f:
            answer = str(ai.sendData("Convo").get('answer'))
            f.write(answer)
    else:
        with open("src/Temp/previous_convos.txt", "x", encoding='utf-8') as f:
            answer = str(ai.sendData("Convo").get('answer'))
            f.write(answer)
    ai.disconnect()