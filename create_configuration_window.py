import customtkinter as ctk

class createConfigurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Live Serial Reader - Create New Configuration")
        self.geometry("700x450")
        self.resizable(True, True)