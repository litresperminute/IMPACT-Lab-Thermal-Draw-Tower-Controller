import customtkinter as ctk
import tkinter as tk
from configuration import configuration, configurations
from data_manager import save_configurations, find_file
from create_configuration_window import open_duplicate_warning_window
import csv

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

global csv_path
csv_path = ''

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
        file.add_command(label="Rename Configuration", command=lambda: self.entry_popup(self.rename_configuration, current_config))
        file.add_command(label="Save", command=lambda: save_configurations(configurations))
        file.add_command(label="Delete", command=lambda: self.delete_configuration(current_config))
        file.add_command(label="Exit to Menu", command=self.openMenu)

        # Add serial variables menu and commands
        serial_variables = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Serial Variables", menu=serial_variables)
        serial_variables.add_command(label="Add Variables", command=lambda: self.addSerialVariables(current_config))
        serial_variables.add_command(label="Edit Variables", command=lambda: self.editSerialVariables(current_config))
        serial_variables.add_command(label="Delete Variables", command=lambda: self.deleteSerialVariables(current_config))

        # Add lines menu and commands
        lines = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Lines", menu=lines)
        lines.add_command(label="Add Lines", command=lambda: self.addBasicLines(current_config))
        lines.add_command(label="Edit Lines", command=lambda: self.editBasicLines(current_config))
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
        baud.add_command(label="Edit Baud Rate", command=lambda: self.entry_popup(self.edit_baud, current_config))

        # Add COM port menu and commands
        com_port = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="COM Port", menu=com_port)
        com_port.add_command(label="Edit COM Port", command=lambda: self.entry_popup(self.edit_com, current_config))

        # Add CSV file menu and commands
        csv = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="CSV File", menu=csv)
        csv.add_command(label="Choose CSV File", command=lambda: self.entry_popup(self.edit_csv, current_config))

        # Add other settings menu and commands
        other_settings = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Other Settings", menu=other_settings)
        other_settings.add_command(label="Edit Serial Delimiter", command=None)
        other_settings.add_command(label="View Configuration Details", command=lambda: self.view_config_settings(current_config))

        self.config(menu=menubar)

    def entry_popup(self, func, current_config):
        """ General use popup for entire window's menu bar """
        entry_popup = tk.Entry(self)
        entry_popup.place(x=self.winfo_pointerx() - self.winfo_rootx(), y=self.winfo_pointery() - self.winfo_rooty(), width=100, height=20)
        entry_popup.focus_set()
        entry_popup.bind("<Return>", lambda event: self.pass_entry_popup(entry_popup, func, current_config))
        entry_popup.bind("<Escape>", lambda event: entry_popup.destroy())

    def pass_entry_popup(self, tk_entry_widget, func, current_config):
        """ Passes popup entry to a function """
        entry = tk_entry_widget.get()
        func(entry, current_config)
        tk_entry_widget.destroy()
    
    def edit_csv(self, csv_name, current_config):
        valid_csv = True
        if any(char in csv_name for char in r""":"'/\*?|!@$%^&""") or csv_name.count(".") > 1 or csv_name[-4:] != '.csv' or csv_name == '':
            valid_csv = False
        
        if valid_csv:
            csv_path = find_file(csv_name)
        else:
            self.csvWarning1(csv_name)

        if csv_path is None:
            self.csvWarning2(csv_name)
        else:
            current_config.csv_file = csv_name

    def edit_baud(self, new_baud, current_config):
        valid_baud = True
        if new_baud.startswith('-') or not new_baud.isdigit():
            valid_baud = False
        if valid_baud:
            current_config.baud_rate = new_baud
        else:
            self.baudWarning1(new_baud)

    def edit_com(self, new_com, current_config):
        valid_port = True
        if new_com.startswith('-') or not new_com.isdigit():
            valid_port = False
        if valid_port:
            current_config.com_port = new_com
        else:
            self.comWarning1(new_com)

    def rename_configuration(self, new_name, current_config):
        old_name = current_config.configuration_name
        valid_name = True

        for config in configurations:
            if new_name == config.configuration_name:
                valid_name = False

        if new_name == old_name:
            valid_name = True

        if not valid_name:
            open_duplicate_warning_window(new_name)
            return

        for config in configurations:
            if old_name == config.configuration_name and valid_name == True:
                config.configuration_name = new_name
                self.name = new_name

        self.title(f"Live Serial Reader - {self.name}")
        save_configurations(configurations)
           
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

    def editSerialVariables(self, current_config):
        open_edit_serial_variables_window(current_config)

    def deleteSerialVariables(self, current_config):
        open_delete_serial_variables_window(current_config)

    def baudWarning1(self, baud_value):
        open_baud_warning1(baud_value)

    def comWarning1(self, com_value):
        open_com_warning1(com_value)

    def csvWarning1(self, csv_name):
        open_csv_warning1(csv_name)

    def csvWarning2(self, csv_name):
        open_csv_warning2(csv_name)

    def view_config_settings(self, current_config):
        self.settings_window = config_settings(current_config)
        self.settings_window.mainloop()

    def addBasicLines(self, current_config):
        open_add_basic_lines_window(current_config)

    def editBasicLines(self, current_config):
        open_edit_basic_lines_window(current_config)

def open_menu_window():
    from menu_window import menuWindow
    menu_win = menuWindow()
    menu_win.mainloop()

class config_settings(tk.Toplevel):
    def __init__(self, current_config):
        super().__init__()
        self.title("Live Serial - Config Settings")
        self.resizable(False, False)

        self.config_name = tk.Label(self, text=f"Config Name: {current_config.configuration_name}")
        self.config_name.grid(row=0, column=0)
        
        self.config_baud = tk.Label(self, text=f"Baud Rate: {current_config.baud_rate}")
        self.config_baud.grid(row=1, column=0)

        self.config_com = tk.Label(self, text=f"COM Port: {current_config.com_port}")
        self.config_com.grid(row=2, column=0)

        self.config_csv = tk.Label(self, text=f"CSV File: {current_config.csv_file}")
        self.config_csv.grid(row=3, column=0)

def open_add_serial_variables_window(current_config):
    from serial_variables import add_serial_variable
    add_serial_var_window = add_serial_variable(current_config)
    add_serial_var_window.mainloop()

def open_edit_serial_variables_window(current_config):
    from serial_variables import edit_serial_variables_list
    edit_serial_var_window = edit_serial_variables_list(current_config)
    edit_serial_var_window.mainloop()

def open_delete_serial_variables_window(current_config):
    from serial_variables import delete_serial_variables
    delete_serial_var_window = delete_serial_variables(current_config)
    delete_serial_var_window.mainloop()

def open_baud_warning1(baud_value):
    from warning_windows import baud_error_window1
    baud_warning_window = baud_error_window1(baud_value)
    baud_warning_window.mainloop()

def open_com_warning1(com_value):
    from warning_windows import com_error_window1
    com_warning_window = com_error_window1(com_value)
    com_warning_window.mainloop()

def open_csv_warning1(csv_name):
    from warning_windows import csv_error_window1
    csv_warning_window = csv_error_window1(csv_name)
    csv_warning_window.mainloop()

def open_csv_warning2(csv_name):
    from warning_windows import csv_error_window2
    csv_warning_window = csv_error_window2(csv_name)
    csv_warning_window.mainloop()

def open_add_basic_lines_window(current_config):
    from lines import add_basic_line
    add_basic_line_window = add_basic_line(current_config)
    add_basic_line_window.mainloop()

def open_edit_basic_lines_window(current_config):
    from lines import edit_basic_line_list
    edit_basic_line_window = edit_basic_line_list(current_config)
    edit_basic_line_window.mainloop()