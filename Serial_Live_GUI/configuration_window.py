import customtkinter as ctk
import tkinter as tk
from menu_window import menuWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class configurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Live Serial Reader - Configuration Editor")
        self.geometry("700x450")
        self.resizable(True, True)

    def open_menu(self):
        self.destroy()
        menuWindow()