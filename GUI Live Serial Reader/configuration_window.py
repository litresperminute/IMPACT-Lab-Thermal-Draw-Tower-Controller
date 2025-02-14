import customtkinter as ctk
import tkinter as tk
from configuration import configuration, configurations
from configuration_manager import save_configurations
from create_configuration_window import open_duplicate_warning_window

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class configurationWindow(ctk.CTk):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.title(f"Live Serial Reader - {self.name}")
        self.geometry("700x450")
        self.resizable(True, True)

        self.iconbitmap("Resources/serial_port_icon_blue.ico")

        # Obtain config
        current_config = self.getConfiguration(self.name)

        # Create menubar
        menubar = tk.Menu(self)

        # Add file menu and commands
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file)
        file.add_command(label="Rename Configuration", command=lambda: self.rename_popup(current_config))
        file.add_command(label="Save", command=lambda: save_configurations(configurations))
        file.add_command(label="Undo", command=None)
        file.add_command(label="Redo", command=None)
        file.add_command(label="Delete", command=lambda: self.delete_configuration(current_config))
        file.add_command(label="Exit to Menu", command=self.openMenu)

        # Add serial variables menu and commands
        serial_variables = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Serial Variables", menu=serial_variables)
        serial_variables.add_command(label="Add Variables", command=lambda: self.addSerialVariables(current_config))
        serial_variables.add_command(label="Edit Variables", command=None)
        serial_variables.add_command(label="Delete Variables", command=None)

        # Add lines menu and commands
        lines = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Lines", menu=lines)
        lines.add_command(label="Add Lines", command=None)
        lines.add_command(label="Edit Lines", command=None)
        lines.add_command(label="Delete Lines", command=None)
        
        # Add plots menu and commands
        plots = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plots", menu=plots)
        plots.add_command(label="Add Plots", command=None)
        plots.add_command(label="Edit Plots", command=None)
        plots.add_command(label="Merge Plots", command=None)
        plots.add_command(label="Delete Plots")

        # Add baud rate menu and commands
        baud = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Baud Rate", menu=baud)
        baud.add_command(label="Edit Baud Rate", command=None)

        # Add COM port menu and commands
        com_port = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="COM Port", menu=com_port)
        com_port.add_command(label="Edit COM Port", command=None)

        # Add CSV file menu and commands
        csv = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="CSV File", menu=csv)
        csv.add_command(label="Choose CSV File", command=None)

        # Add other settings menu and commands
        other_settings = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Other Settings", menu=other_settings)
        other_settings.add_command(label="Edit Serial Delimiter", command=None)

        self.config(menu=menubar)

    def rename_popup(self, current_config):
        rename_popup = tk.Entry(self)
        rename_popup.place(x=self.winfo_pointerx() - self.winfo_rootx(), y=self.winfo_pointery() - self.winfo_rooty(), width=100, height=20)
        rename_popup.focus_set()

        rename_popup.bind("<Return>", lambda event: self.rename_configuration(current_config, rename_popup))

    def rename_configuration(self, current_config, rename_popup):
       old_name = current_config.configuration_name
       new_name = rename_popup.get()
       valid_name = True

       for config in configurations:
           if new_name == config.configuration_name:
               valid_name = False
        
       if valid_name == False:
           open_duplicate_warning_window(new_name)
           rename_popup.destroy()
           return

       for config in configurations:
           if old_name == config.configuration_name and valid_name == True:
               config.configuration_name = new_name
               self.name = new_name
            
       self.title(f"Live Serial Reader - {self.name}")
       save_configurations(configurations)
        
       rename_popup.destroy()
           
    def openMenu(self):
        self.destroy()
        open_menu_window()

    def getConfiguration(self, name):
        for config in configurations:
            if name == config.configuration_name:
                current_config = config
        return current_config

    def delete_configuration(self, config):
        """ Deletes configuration object from JSON file """
        for config_object in configurations:
            if config_object.configuration_name == config.configuration_name:
                configurations.remove(config_object)
        save_configurations(configurations)
        self.openMenu()

    def addSerialVariables(self, current_config):
        open_add_serial_variables_window(current_config)

def open_menu_window():
    from menu_window import menuWindow
    menu_win = menuWindow()
    menu_win.mainloop()

def open_add_serial_variables_window(current_config):
    from serial_variables import add_serial_variable
    add_serial_var_window = add_serial_variable(current_config)
    add_serial_var_window.mainloop()