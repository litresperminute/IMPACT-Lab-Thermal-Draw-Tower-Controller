import customtkinter as ctk
import tkinter as tk
from configuration_window import configurationWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class menuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Live Series Reader - Main Menu")
        self.geometry("700x450")
        self.resizable(True, True)

        

    def open_configuration(self):
        self.destroy()
        configurationWindow()

    