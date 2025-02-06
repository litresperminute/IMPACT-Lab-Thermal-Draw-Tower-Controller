import customtkinter as ctk
from configuration import configuration
from configuration import configurations

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class configurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Live Serial Reader - Configuration Editor")
        self.geometry("700x450")
        self.resizable(True, True)

    def openMenu(self):
        self.destroy()
        open_menu_window()

def open_menu_window():
    from menu_window import menuWindow
    menu_win = menuWindow()
    menu_win.mainloop()