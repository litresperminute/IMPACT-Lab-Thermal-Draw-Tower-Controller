import customtkinter as ctk
from configuration import configuration, configurations
from data_manager import save_configurations

class createConfigurationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Live Serial Reader - Create New Configuration")
        self.geometry("450x150")
        self.resizable(False, False)

        self.iconbitmap("Resources/serial_port_icon_blue.ico")

        self.grid_columnconfigure(0, weight=1)

        self.entryBox = ctk.CTkEntry(self, placeholder_text="Enter a configuration name...")
        self.entryBox.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.entryBox.bind("<Return>", self.updateConfigs)

        self.cancelButton = ctk.CTkButton(self, text="Cancel", anchor='e', command=self.openMainMenu)
        self.cancelButton.grid(row=1, padx=20, pady=10)

    def openMainMenu(self):
        self.destroy()
        open_menu_window()

    def updateConfigs(self, event=None):
        entryText = self.entryBox.get()
        duplicate = False

        for config in configurations:
            if entryText == config.configuration_name:
                self.openDuplicateConfigWarning(entryText)
        
        if duplicate == False:
            configuration(entryText, [], 0, 0, 0, "No File", [])
            save_configurations(configurations)
            self.openConfiguration(entryText)

    def openDuplicateConfigWarning(self, newConfigName):
        open_duplicate_warning_window(newConfigName)
        self.destroy()

    def openConfiguration(self, configName):
        self.destroy()
        open_configuration_window(configName)

def open_duplicate_warning_window(newConfigName):
    from warning_windows import duplicateWarningWindow
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