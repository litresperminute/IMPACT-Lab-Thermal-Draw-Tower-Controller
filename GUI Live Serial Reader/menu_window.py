import customtkinter as ctk
from configuration import configuration, configurations
from resource_manager import icon_path
from data_manager import load_configurations

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class menuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Live Serial Reader - Main Menu")
        self.geometry("700x450")
        self.resizable(True, True)

        global json_data
        json_data = load_configurations()

        self.iconbitmap(icon_path)

        # Make sure main window columns expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Scrollable area should expand

        # Search Entry
        self.entryBox = ctk.CTkEntry(self, placeholder_text="Search for configuration...")
        self.entryBox.grid(row=0, column=0, padx=20, sticky="ew", pady=10)
        self.entryBox.bind("<KeyRelease>", self.updateFrame)

        # Headers
        headers = ["Configuration Name", "Variables", "Plots", "Baud Rate", "COM Port", "CSV File"]
        header_font = ctk.CTkFont(family="Helvetica", size=12, weight="bold")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=1, column=0, sticky="ew", padx=10)

        # Configure columns in header frame
        for i in range(len(headers)):
            self.header_frame.grid_columnconfigure(i, weight=1)

        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.header_frame, text=header, font=header_font)
            label.grid(row=0, column=col, sticky="ew", padx=5)

        # Scrollable Frame for search results
        self.scrollFrame = ctk.CTkScrollableFrame(self, fg_color="gray")
        self.scrollFrame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Ensure the scroll frame's columns align properly
        for i in range(len(headers)):
            self.scrollFrame.grid_columnconfigure(i, weight=1)

        # Store configuration list
        self.configs = configurations

        # Populate Scrollable Frame initially
        self.populateFrame(self.configs)

    def populateFrame(self, configs):
        """ Populate scrollable frame with configuration buttons and labels """
        # Clear existing widgets
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()

        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, config in enumerate(configs):
            parameters = [
                config.configuration_name,
                str(len(config.serial_variables)),
                str(len(config.plots)),
                str(config.baud_rate),
                f"COM{config.com_port}",
                config.csv_file
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scrollFrame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0] and len(parameter) > 26:
                    label_text = parameter[:23] + "..."
                    label = ctk.CTkLabel(self.scrollFrame, text=label_text, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, name=config.configuration_name: open_configuration_window(name, self))
                    label.configure(cursor="hand2")
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scrollFrame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, name=config.configuration_name: open_configuration_window(name, self))
                    label.configure(cursor="hand2")

        row_count = len(self.scrollFrame.grid_slaves())
        button = ctk.CTkButton(self.scrollFrame, text="+ Create New Configuration", command=lambda: open_new_configuration_window(self))
        button.grid(row=row_count, column=0, columnspan=self.scrollFrame.grid_size()[0])

    def updateFrame(self, event=None):
        """ Filter results and update scrollable frame """
        searchText = self.entryBox.get().lower()
        filteredConfigs = [config for config in self.configs if searchText in config.configuration_name.lower()]
        self.populateFrame(filteredConfigs)

def open_configuration_window(name: str, menu_win: menuWindow):
    from configuration_window import configurationWindow
    menu_win.withdraw()
    menu_win.after(250, lambda: menu_win.destroy)
    config_win = configurationWindow(name)
    config_win.mainloop()

def open_new_configuration_window(menu_win: menuWindow):
    from create_configuration_window import createConfigurationWindow
    menu_win.withdraw()
    menu_win.after(250, lambda: menu_win.destroy)
    new_config_win = createConfigurationWindow()
    new_config_win.mainloop()

if __name__ == "__main__":
    MenuWindow = menuWindow()
    MenuWindow.mainloop()