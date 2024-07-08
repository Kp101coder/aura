from tkcalendar import Calendar
import customtkinter as ctk
from tkinter import ttk

class Calendar():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("550x400")

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", padx=10, pady=10, expand=True)

    style = ttk.Style(root)
    style.theme_use("default")

    cal = Calendar(frame, selectmode='day', locale='en_US', disabledforeground='red',
               cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
    cal.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()