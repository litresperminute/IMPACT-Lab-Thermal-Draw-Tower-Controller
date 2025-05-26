import json
import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from configuration import configurations
from data_manager import save_configurations, find_file, erase_csv
from input_check import int_check
from run import run_plots
from resource_manager import icon_path, COMMUNICATION, CURRENT_CONFIG
import csv
from configuration import configuration
import time
import threading
from plots import plot
from lines import line

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

global csv_path
csv_path = ''

class configurationWindow(ctk.CTk):
    def __init__(self, name):
        # Define window appearance and behavior
        super().__init__()
        self.name = name
        self.title(f"Live Serial Reader - {self.name}")
        self.geometry("700x450")
        self.resizable(True, True)
        self.iconbitmap(icon_path)
        self.plot_dict = {}

        # Obtain config
        self.current_config = self.getConfiguration(self.name)

        # Running bool for live plotting
        self.running = False

        self.csv_recording = False
        self.trial_num = 0
        self.new_trial = False

        self.exit_gui = False
        self.run_module = run_plots()
        self.communication_dict = {
            'running': self.running,
            'trial_num': self.trial_num,
            'new_trial': False,
            'csv_recording': self.csv_recording,
            'valid_port': False,
            'error_triggered': False,
            'serial_values': [],
            'plot_dict': serialize_plot_dict(self.plot_dict),
            'exit_gui': False,
            'update_gui_plots': False,
            'generate_gui_plots': False,
            'validate_port_settings': False,
            'obtain_serial_data': False,
            'plot_serial_data': False,
            'update_config_to_json': False,
            'skip_to_beginning': False,
            'gui': 'waiting',
            'backend': 'requestd',
            'designated_author': 'baackend'
        }

        # Create menubar
        menubar = tk.Menu(self)

        # Add file menu and commands
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file)
        file.add_command(label="Rename Configuration", command=lambda: self.entry_popup(self.rename_configuration, self.current_config))
        file.add_command(label="Save", command=lambda: save_configurations(configurations))
        file.add_command(label="Delete", command=self.delete_configuration)
        file.add_command(label="Exit to Menu", command=lambda: open_menu_window(self, self.run_module, self.communication_dict))

        # Add serial variables menu and commands
        serial_variables = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Serial Variables", menu=serial_variables)
        serial_variables.add_command(label="Add Variables", command=lambda: open_add_serial_variables_window(self.current_config))
        serial_variables.add_command(label="Edit Variables", command=lambda: open_edit_serial_variables_window(self.current_config))
        serial_variables.add_command(label="Delete Variables", command=lambda: open_delete_serial_variables_window(self.current_config))

        # Add lines menu and commands
        lines = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Lines", menu=lines)
        lines.add_command(label="Add Lines", command=lambda: open_add_basic_lines_window(self.current_config))
        lines.add_command(label="Edit Lines", command=lambda: open_edit_basic_lines_window(self.current_config))
        lines.add_command(label="Delete Lines", command=lambda: open_delete_lines_window(self.current_config))
        
        # Add plots menu and commands
        plots = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plots", menu=plots)
        plots.add_command(label="Add Plots", command=lambda: open_add_plot_window(self.current_config))
        plots.add_command(label="Edit Plots", command=lambda: open_edit_plot_window(self.current_config))
        plots.add_command(label="Delete Plots", command=lambda: open_delete_plot_window(self.current_config))

        # Add baud rate menu and commands
        baud = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Baud Rate", menu=baud)
        baud.add_command(label="Edit Baud Rate", command=lambda: self.entry_popup(self.edit_baud, self.current_config))

        # Add COM port menu and commands
        com_port = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="COM Port", menu=com_port)
        com_port.add_command(label="Edit COM Port", command=lambda: self.entry_popup(self.edit_com, self.current_config))

        # Add CSV file menu and commands
        csv = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="CSV File", menu=csv)
        # csv.add_command(label="Choose CSV File", command=lambda: self.entry_popup(self.edit_csv, self.current_config))
        csv.add_command(label="Toggle CSV Data Recording", command=self.toggle_csv_recording)
        csv.add_command(label="Erase CSV File", command=lambda: erase_csv())

        # Add other settings menu and commands
        other_settings = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Other Settings", menu=other_settings)
        # other_settings.add_command(label="Edit Serial Delimiter", command=None)
        other_settings.add_command(label="View Details", command=lambda: self.view_config_settings(self.current_config))
        other_settings.add_command(label="Help", command=self.help)

        # Add run button to menubar
        run_list = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="RUN!", menu=run_list)
        run_list.add_command(label="RUN!", command=lambda: setattr(self, "running", True))
        run_list.add_command(label="STOP!", command=lambda: setattr(self, "running", False))
        run_list.add_command(label="Trial Number", command=lambda: self.entry_popup(self.edit_trial_num))
        run_list.add_command(label="Start New Trial", command=lambda: setattr(self, "new_trial", True))
        
        self.config(menu=menubar)

        self.start_time = time.time()
        self.stop_time = 13

        self.communication_keys = [key for key in self.communication_dict]
        # print(f"GUI plot cycle has been started! - Running status = {self.running}")
        config_to_json(self.current_config, self)
        self.after(2, write_communication_file(self.communication_dict))
        self.after(1, self.check_communication_file())
        self.after(3, self.run_module.start_gui_plot_processes())

    def gui_plot_dict_json_parser(self):
        json_plot_dict = {}
        if not self.plot_dict:
            json_plot_dict = serialize_plot_dict(json_plot_dict)
            return json_plot_dict
        json_plot_dict = {}
        for plot_key, (_, _, _, ax) in self.plot_dict.items():
            line_objs = [line_obj for line_obj in list(ax.get_lines())]
            json_plot_dict[plot_key] = line_objs
        json_plot_dict = serialize_plot_dict(json_plot_dict)
        return json_plot_dict

    def check_communication_file(self):
        threading.Thread(target=self._check_communication_file, daemon=True).start()

    def _check_communication_file(self):
    #     # current_time = time.time()
    #     # if current_time - self.start_time >= self.stop_time:
    #     #     self.destroy()
    #     #     return
        if self.exit_gui and not self.run_module.plot_cycle_termination_event.is_set():
            self.communication_dict['running'] = False
            self.communication_dict['valid_port'] = False
            self.communication_dict['error_triggered'] = False
            self.communication_dict['serial_values'] = []
            self.communication_dict['plot_dict'] = {}
            self.communication_dict['exit_gui'] = True
            self.communication_dict['update_gui_plots'] = False
            self.communication_dict['generate_gui_plots'] = False
            self.communication_dict['validate_port_settings'] = False
            self.communication_dict['obtain_serial_data'] = False
            self.communication_dict['plot_serial_data'] = False
            self.communication_dict['update_config_to_json'] = False
            self.communication_dict['skip_to_beginning'] = False
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['backend'] = 'waiting'
            self.communication_dict['designated_author'] = None
            self.after(2, lambda: write_communication_file(self.communication_dict))
            self.after(3, self._check_communication_file)
            return
        elif self.exit_gui and self.run_module.plot_cycle_termination_event.is_set():
            return
        self.communication_dict = read_communication_file() # Stores the contents of communication.json as its own dictionary attribute
        self.communication_dict['csv_recording'] = self.csv_recording
        if not self.current_config.plots or not self.current_config.lines or not self.current_config.serial_variables:
            self.running = False
        # Checks its own communication dictionary to see if the gui is even being requested or the designated author of communication.json
        if (all(key in self.communication_dict for key in self.communication_keys)
            and self.communication_dict['gui'] == 'requested'
            and self.communication_dict['designated_author'] == 'gui'
            and not self.communication_dict['exit_gui']
        ):
            if not self.running and self.csv_recording and not self.communication_dict['exit_gui']:
                self.communication_dict['running'] = False
                self.communication_dict['csv_recording'] = False
                self.communication_dict['skip_to_beginning'] = True
                self.csv_recording = False
                self.running = False
                self.after(2, lambda: write_communication_file(self.communication_dict))
                self.after(3, self._check_communication_file)
                return
            elif self.communication_dict['update_config_to_json']: # Condition to handle when the backend requests the gui to update config.json with self.current_config
                # print(f"Request successfully received from process! - Running status = {self.running}")
                config_to_json(self.current_config, self)
                self.after(2, lambda: write_communication_file(self.communication_dict))
                self.after(3, self._check_communication_file)
                return
            elif self.communication_dict['generate_gui_plots']:
                # print(f"Request successfully received from process! - Running status = {self.running}")
                self.after(1, lambda: self.generate_gui_plots())
                self.after(2, lambda: write_communication_file(self.communication_dict))
                self.after(3, self._check_communication_file)
                return
            elif self.communication_dict['plot_serial_data']:
                # print(f"Request successfully received from process! - Running status = {self.running}")
                self.after(1, lambda: self.plot_serial_data())
                self.after(2, lambda: write_communication_file(self.communication_dict))
                self.after(3, self._check_communication_file)
                return
        elif all(key in self.communication_dict for key in self.communication_keys):
            if self.communication_dict['error_triggered'] and not self.communication_dict['exit_gui']:
                self.running = False
                self.communication_dict['running'] = self.running
                self.communication_dict['error_triggered'] = False
                self.after(2, lambda: write_communication_file(self.communication_dict))
                self.after(3, self._check_communication_file)
                return
        self.after(3, self._check_communication_file)
        return

    def generate_gui_plots(self):
        # print(f"GUI has begun to generate plots! - Running status = {self.running}")
        plots = self.current_config.plots
        if self.plot_dict:
            for (canvas_widget, canvas, fig, ax) in self.plot_dict.values():
                plt.close(fig)
                ax.get_lines().clear()
                canvas_widget.destroy()
            self.plot_dict = {}
        for plot_obj in plots:
            if plot_obj.lines:
                fig, ax = plt.subplots()
                ax.set_title(plot_obj.plot_title)
                ax.set_xlabel(plot_obj.x_label)
                ax.set_ylabel(plot_obj.y_label)
                ax.yaxis.set_label_position('right')
                ax.yaxis.tick_right()
                ax.grid()
                for line_obj in plot_obj.lines:
                    ax.add_line(line_obj.duplicate())
                ax.legend(loc=plot_obj.legend_position)
                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas.draw_idle()
                fig.tight_layout()
                fig.subplots_adjust(right=0.75, bottom=0.25, top=0.85)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=plot_obj.plot_position[0], column=plot_obj.plot_position[1], sticky="nsew")
                self.grid_rowconfigure(plot_obj.plot_position[0], weight=1)
                self.grid_columnconfigure(plot_obj.plot_position[1], weight=1)
                self.plot_dict[plot_obj] = (canvas_widget, canvas, fig, ax)
        # print(f"GUI has finished generating gui plots! - Running status = {self.running}")
        if self.plot_dict:
            self.communication_dict['running'] = self.running
            if not self.running:
                self.communication_dict['skip_to_beginning'] = True
            self.communication_dict['plot_dict'] = serialize_plot_dict(self.plot_dict)
            self.communication_dict['generate_gui_plots'] = False
            self.communication_dict['validate_port_settings'] = True
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['backend'] = 'requested'
            self.communication_dict['designated_author'] = 'backend'
        elif not self.plot_dict:
            self.running = False
            self.communication_dict['running'] = self.running
            self.communication_dict['skip_to_beginning'] = True
            self.communication_dict['plot_dict'] = serialize_plot_dict(self.plot_dict)
            self.communication_dict['generate_gui_plots'] = False
            self.communication_dict['validate_port_settings'] = False
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['backend'] = 'requested'
            self.communication_dict['designated_author'] = 'backend'
        return

    def plot_serial_data(self):
        # print(f"GUI has begun plotting serial data! - Running status = {self.running} - Valid Port? = {self.communication_dict['valid_port']}")
        if 'valid_port' in self.communication_dict and not self.communication_dict['valid_port']:
            self.running = False
            self.communication_dict['running'] = self.running
            self.communication_dict['plot_serial_data'] = False
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['skip_to_beginning'] = True
            return
        serial_values = self.communication_dict['serial_values']
        try:
            value_index = 0
            for value_index in range(len(serial_values)):
                for serial_var in self.current_config.serial_variables:
                    if serial_var.variable_number == value_index:
                        serial_var.data_array.append(float(serial_values[value_index].strip()))
            for plot_key, (canvas_widget, canvas, fig, ax) in self.plot_dict.items():
                for line_obj in list(ax.get_lines()):
                    line_obj.update_line()
                ax.relim()
                ax.autoscale()
                canvas.draw_idle()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=plot_key.plot_position[0], column=plot_key.plot_position[1], sticky="nsew")
                self.grid_rowconfigure(plot_key.plot_position[0], weight=1)
                self.grid_columnconfigure(plot_key.plot_position[1], weight=1)
            # print(f"GUI has successfully plotted serial values! - Running status = {self.running}")
            self.communication_dict['running'] = self.running
            self.communication_dict['plot_serial_data'] = False
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['skip_to_beginning'] = True
            self.communication_dict['backend'] = 'requested'
            self.communication_dict['designated_author'] = 'backend'
            return
        except:
            # print(f"GUI failed to plot serial values! - Running status = {self.running}")
            self.communication_dict['running'] = self.running
            self.communication_dict['plot_serial_data'] = False
            self.communication_dict['gui'] = 'waiting'
            self.communication_dict['skip_to_beginning'] = True
            self.communication_dict['backend'] = 'requested'
            self.communication_dict['designated_author'] = 'backend'
            return

    def entry_popup(self, func, current_config=None):
        """ General use popup for entire window's menu bar """
        entry_popup = tk.Entry(self)
        entry_popup.place(x=self.winfo_pointerx() - self.winfo_rootx(), y=self.winfo_pointery() - self.winfo_rooty(), width=100, height=20)
        entry_popup.focus_set()
        if not current_config is None:
            entry_popup.bind("<Return>", lambda event: self.pass_entry_popup(entry_popup, func, current_config))
            entry_popup.bind("<Escape>", lambda event: entry_popup.destroy())
        else:
            entry_popup.bind("<Return>", lambda event: self.pass_entry_popup(entry_popup, func))
            entry_popup.bind("<Escape>", lambda event: entry_popup.destroy())

    def pass_entry_popup(self, tk_entry_widget, func, current_config=None):
        """ Passes popup entry to a function """
        entry = tk_entry_widget.get()
        if not current_config is None:
            func(entry, current_config)
        else:
            func(entry)
        tk_entry_widget.destroy()

    def edit_trial_num(self, trial_num: int | float):
        self.trial_num = trial_num
        self.communication_dict['trial_num'] = self.trial_num
        return

    def toggle_csv_recording(self):
        if self.running:
            self.csv_recording = not self.csv_recording
        else:
            self.csv_recording = False
        return

    def edit_csv(self, csv_name, current_config):
        valid_csv = True
        if any(char in csv_name for char in r""":"'/\*?|!@$%^&""") or csv_name.count(".") > 1 or csv_name[-4:] != '.csv' or csv_name == '':
            valid_csv = False
        
        if valid_csv:
            csv_path = find_file(csv_name)
        else:
            error_message = f'The CSV file {csv_name} is invalid!'
            error_title = "CSV File Error"
            error_function(error_message, error_title, csv_name=csv_name)

        if csv_path is None:
            error_message = f"The CSV file {csv_name} doesn't exist!"
            error_title = "CSV File Error"
            error_function(error_message, error_title, csv_name=csv_name)
        else:
            current_config.csv_file = csv_name
            config_to_json(current_config)

    def edit_baud(self, new_baud, current_config):
        self.communication_dict['valid_port'] = False
        self.running = False
        self.communication_dict['running'] = self.running
        valid_baud = int_check(new_baud)
        if not valid_baud:
            valid_baud = False
        elif valid_baud:
            current_config.baud_rate = new_baud
            config_to_json(current_config, self)
        else:
            error_message = f"The baud rate {new_baud} is invalid!"
            error_title = "Invalid Baud Rate"
            error_function(error_message, error_title, new_baud=new_baud)

    def edit_com(self, new_com, current_config):
        self.communication_dict['valid_port'] = False
        self.running = False
        self.communication_dict['running'] = self.running
        valid_port = int_check(new_com)
        if not valid_port:
            valid_port = False
        elif valid_port:
            current_config.com_port = new_com
            config_to_json(current_config, self)
        else:
            error_message = f"The COM port {new_com} is invalid!"
            error_title = "Invalid COM Port"
            error_function(error_message, error_title, new_com=new_com)

    def rename_configuration(self, new_name, current_config):
        old_name = current_config.configuration_name
        valid_name = True

        for config in configurations:
            if new_name == config.configuration_name:
                valid_name = False

        if new_name == old_name:
            valid_name = True

        if not valid_name:
            error_message = f'The configuration enetered already exists:\n\n"{new_name}"'
            error_title = "Duplicate Configuration Names"
            error_function(error_message, error_title, new_name=new_name)
            return

        for config in configurations:
            if old_name == config.configuration_name and valid_name == True:
                config.configuration_name = new_name
                self.name = new_name

        self.title(f"Live Serial Reader - {self.name}")
        save_configurations(configurations)

    def getConfiguration(self, name):
        for config in configurations:
            if name == config.configuration_name:
                current_config = config
        return current_config

    def delete_configuration(self):
        """ Deletes configuration object from JSON file """
        for config_object in configurations:
            if config_object == self.current_config:
                configurations.remove(config_object)
        save_configurations(configurations)
        open_menu_window(self, self.run_module, self.communication_dict)

    def view_config_settings(self, current_config):
        self.settings_window = config_settings(self, current_config)
        self.settings_window.mainloop()

    def help(self):
        self.help_win = help_window()
        self.help_win.mainloop()

class help_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Live Serial Reader - Help Window")
        self.resizable(True, True)
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=50)
        with open("Resources/Help.txt", "r") as file:
            content = file.read()
        self.text_area.insert(tk.END, content)
        self.text_area.config(state=tk.DISABLED)

class config_settings(tk.Toplevel):
    def __init__(self, ctk_window, current_config):
        super().__init__()
        self.title("Live Serial Reader - Config Settings")
        self.resizable(False, False)

        self.config_name = tk.Label(self, text=f"Config Name: {current_config.configuration_name}")
        self.config_name.grid(row=0, column=0)
        
        self.config_baud = tk.Label(self, text=f"Baud Rate: {current_config.baud_rate}")
        self.config_baud.grid(row=1, column=0)

        self.config_com = tk.Label(self, text=f"COM Port: {current_config.com_port}")
        self.config_com.grid(row=2, column=0)

        self.config_csv = tk.Label(self, text=f"CSV File: {current_config.csv_file}")
        self.config_csv.grid(row=3, column=0)

        self.trial_num = tk.Label(self, text=f"Trial Num: {ctk_window.trial_num}")
        self.trial_num.grid(row=4, column=0)

        self.csv_recording = tk.Label(self, text=f"CSV Recording: {ctk_window.csv_recording}")
        self.csv_recording.grid(row=5, column=0)

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

def open_add_basic_lines_window(current_config):
    from lines import add_basic_line
    add_basic_line_window = add_basic_line(current_config)
    add_basic_line_window.mainloop()

def open_edit_basic_lines_window(current_config):
    from lines import edit_basic_line_list
    edit_basic_line_window = edit_basic_line_list(current_config)
    edit_basic_line_window.mainloop()

def open_delete_lines_window(current_config):
    from lines import delete_lines
    delete_lines_window = delete_lines(current_config)
    delete_lines_window.mainloop()

def open_add_plot_window(current_config):
    from plots import add_plots
    add_plot_win = add_plots(current_config)
    add_plot_win.mainloop()

def open_edit_plot_window(current_config):
    from plots import edit_plots_list
    edit_plot_win = edit_plots_list(current_config)
    edit_plot_win.mainloop()

def open_delete_plot_window(current_config):
    from plots import delete_plot_list
    delete_plot_win = delete_plot_list(current_config)
    delete_plot_win.mainloop()

def open_menu_window(current_win: configurationWindow, run_module: run_plots, communication_dict: dict):
    from menu_window import menuWindow
    current_win.exit_gui = True
    # print(f"Ready to exit!")
    current_win.withdraw()
    current_win.after(250, lambda: current_win.destroy)
    menu_win = menuWindow()
    menu_win.mainloop()

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, **kwargs)
    error_win.mainloop()

def config_to_json(config: configuration, ctk_window):
    with open(CURRENT_CONFIG, "w") as file:
        json.dump(config.to_dict(), file, indent=4)
    ctk_window.communication_dict['running'] = ctk_window.running
    ctk_window.communication_dict['update_config_to_json'] = False
    ctk_window.communication_dict['gui'] = 'waiting'
    ctk_window.communication_dict['update_gui_plots'] = True
    ctk_window.communication_dict['backend'] = 'requested'
    ctk_window.communication_dict['designated_author'] = 'backend'
    # print(f"GUI has successfully updated config.json! - Running status = {ctk_window.running}")
    return

def reset_config_json():
    with open(CURRENT_CONFIG, "w") as file:
        json.dump({}, file, indent=4)
    return

def write_communication_file(gui_to_backend_dict: dict):
    with open(COMMUNICATION, "w") as file:
        json.dump(gui_to_backend_dict, file, indent=4)
        return
    
def read_communication_file():
    try:
        with open(COMMUNICATION, "r") as file:
            backend_to_gui_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        backend_to_gui_dict = {}
    return backend_to_gui_dict

def serialize_plot_dict(plot_dict: dict):
    plot_dict_serialized = []
    if not plot_dict:
        return plot_dict_serialized
    for key, (_, _, _, ax) in plot_dict.items():
        if isinstance(key, plot):
            new_key = key.plot_to_dict()
        else:
            return TypeError
        try:
            line_objs = list(ax.get_lines())
        except:
            return TypeError
        new_value = []
        for line_obj in line_objs:
            if isinstance(line_obj, line):
                new_value.append(line_obj.line_to_dict())
            else:
                return TypeError
        plot_dict_serialized.append((new_key, new_value))
    return plot_dict_serialized