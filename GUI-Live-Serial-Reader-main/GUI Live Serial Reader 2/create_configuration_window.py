import customtkinter as ctk
from configuration import configuration, configurations
from data_manager import save_configurations
from input_check import name_check
from resource_manager import icon_path

class createConfigurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Live Serial Reader - Create New Configuration")
        self.geometry("450x150")
        self.resizable(False, False)

        self.iconbitmap(icon_path)

        self.grid_columnconfigure(0, weight=1)

        self.entryBox = ctk.CTkEntry(self, placeholder_text="Enter a configuration name...")
        self.entryBox.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.entryBox.bind("<Return>", self.updateConfigs)

        self.cancelButton = ctk.CTkButton(self, text="Cancel", anchor='e', command=lambda: open_menu_window(self))
        self.cancelButton.grid(row=1, padx=20, pady=10)

    def updateConfigs(self, event=None):
        entryText = self.entryBox.get().strip()
        duplicate = False

        for config in configurations:
            if entryText == config.configuration_name:
                duplicate = True

        if duplicate:
            error_message = f'The configuration enetered already exists:\n\n"{entryText}"'
            error_title = "Duplicate Configuration Names"
            error_function(error_message, error_title, entryText=entryText)
        elif not name_check(entryText):
            error_message = f'The configuration name "{entryText}" is not valid!'
            error_title = "Invalid Configuration Name"
            error_function(error_message, error_title, entryText=entryText)
        else:
            configuration(entryText, [], [], 0, 0, "No File", [])
            save_configurations(configurations)
            open_configuration_window(entryText, self)

def open_configuration_window(configName:str, current_win: createConfigurationWindow):
    from configuration_window import configurationWindow
    current_win.withdraw()
    current_win.after(250, lambda: current_win.destroy)
    config_win = configurationWindow(configName)
    config_win.mainloop()

def open_menu_window(current_win: createConfigurationWindow):
    from menu_window import menuWindow
    current_win.withdraw()
    current_win.after(250, lambda: current_win.destroy)
    menu_win = menuWindow()
    menu_win.mainloop()
    current_win.destroy()

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, **kwargs)
    error_win.mainloop()