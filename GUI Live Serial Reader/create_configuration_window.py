import customtkinter as ctk
from configuration import configuration, configurations

class createConfigurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Live Serial Reader - Create New Configuration")
        self.geometry("700x450")
        self.resizable(True, True)

        self.entryBox = ctk.CTkEntry(self, placeholder_text="Enter a Configuration Name...")
        self.entryBox.grid(row=0, padx=20, pady=20)
        self.entryBox.bind("<Return>", self.updateName)

        self.cancelButton = ctk.CTkButton(self, text="Cancel", anchor='e', command=self.openMainMenu)
        self.cancelButton.grid(row=1, padx=20, pady=10)

    def openMainMenu(self):
        self.destroy()
        open_menu_window()

    def updateName(self, event=None):
        entryText = self.entryBox.get()
        duplicate = False

        for config in configurations:
            if entryText == config.configuration_name:
                self.openDuplicateConfigWarning(entryText)
        
        if duplicate == False:
            configuration(entryText, 0, 0, 0, 0, "No CSV File")
            self.openConfiguration(entryText)

    def openDuplicateConfigWarning(self, newConfigName):
        open_duplicate_warning_window(newConfigName)
        self.destroy()

    def openConfiguration(self, configName):
        open_configuration_window(configName)
        self.destroy()

def open_duplicate_warning_window(newConfigName):
    from duplicate_warning_window import duplicateWarningWindow
    warning_win = duplicateWarningWindow(newConfigName)
    warning_win.mainloop()

def open_configuration_window(configName):
    from configuration_window import configurationWindow
    config_win = configurationWindow(configName)
    config_win.mainloop()

def open_menu_window():
    from menu_window import menuWindow
    menu_win = menuWindow()
    menu_win.mainloop()