import customtkinter as ctk
from resource_manager import icon_path
from input_check import name_check, int_check
from collections import Counter

class serial_variable:
    def __init__(self, variable_number: int, variable_name: str, variable_units: str, data_array: list):
        # Serial Variable Object Attributes
        self.variable_number = variable_number
        self.variable_name = variable_name
        self.variable_units = variable_units
        self.data_array = data_array
    
    def __eq__(self, other):
        if isinstance(other, serial_variable):
            if (
                other.variable_number == self.variable_number and
                other.variable_name == self.variable_name and
                other.variable_units == self.variable_units
            ):
                return True
        return False

    def __hash__(self):
        return hash((self.variable_number, self.variable_name, self.variable_units))

    def __str__(self):
        return f"Serial Name: {self.variable_name}, Serial Num: {self.variable_number}, Serial Units: {self.variable_units}"

    def serial_to_dict(self):
        return {
            "variable_number": self.variable_number,
            "variable_name": self.variable_name,
            "variable_units": self.variable_units,
            "data_array": self.data_array
        }

    def serial_from_dict(sub_data):
        return serial_variable(sub_data["variable_number"], sub_data["variable_name"], sub_data["variable_units"], sub_data["data_array"])
    
    def is_valid_serial_var(self):
        valid_serial_var = True
        if not self.variable_units or not isinstance(self.variable_units, str):
            valid_serial_var = False
        elif not self.variable_name or not isinstance(self.variable_name, str):
            valid_serial_var = False
        elif not isinstance(self.variable_number, int):
            valid_serial_var = False
        elif isinstance(self.variable_number, int) and self.variable_number < 0:
            valid_serial_var = False
        # if not valid_serial_var:
        #     print(f"Invalid serial var detected!")
        return valid_serial_var

class add_serial_variable(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Serial Variable")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()
        self.config = config

        self.variable_number = 0
        self.variable_name = ""
        self.variable_units = ""
        self.data_array = []

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter variable number...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.change_focus(2, event))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter variable name...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.change_focus(3, event))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter variable units...", width=240)
        self.entry3.grid(row=2, column=0)

        self.button1 = ctk.CTkButton(self, text="Add Another Variable", command=self.add_another_variable, width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Variables", command=self.add_serial_variable_to_config, width=180)
        self.button2.grid(row=4, column=0)
    
    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 2:
            self.entry2.focus_set()
        elif entry_box_num == 3:
            self.entry3.focus_set()

    def add_variable_number(self):
        input_num = self.entry1.get().strip()
        serial_variables = self.config.serial_variables
        valid_int = int_check(input_num)
        if valid_int:
            for serial_obj in serial_variables:
                if serial_obj.variable_number == int(input_num):
                    valid_int = False
                elif not valid_int:
                    break
        if valid_int:
            self.variable_number = int(input_num)
            return True
        else:
            error_message = f'Serial variable number {input_num} is invalid or already exists!'
            error_title = "Invalid Serial Number"
            error_function(error_message, error_title, input_num=input_num)
            return False

    def add_variable_name(self):
        input_name = self.entry2.get().strip()
        valid_name = name_check(input_name)
        if valid_name:
            self.variable_name = input_name
            return True
        else:
            error_message = f'The serial variable name {input_name} is invalid!'
            error_title = "Invalid Serial Name"
            error_function(error_message, error_title, input_name=input_name)
            return False

    def add_variable_units(self):
        input_units = self.entry3.get().strip()
        if not input_units:
            error_message = "No units have been entered!"
            error_title = "Missing Units"
            error_function(error_message, error_title)
            return False
        else:
            self.variable_units = input_units
            return True
        
    def add_serial_variable_to_config(self, event=None):
        if self.add_variable_number() and self.add_variable_name() and self.add_variable_units():
            new_serial_obj = serial_variable(self.variable_number, self.variable_name, self.variable_units, self.data_array)
            self.config.serial_variables.append(new_serial_obj)
            self.destroy()
            return True
        return False

    def add_another_variable(self, event=None):
        if self.add_serial_variable_to_config():
            new_add_var_window = add_serial_variable(self.config)
            new_add_var_window.mainloop()

class edit_serial_variables_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Serial Variables")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        headers = ["Variable Name", "Serial Number", "Variable Units"]
        header_font = ctk.CTkFont(family="Helvetica", size=12, weight="bold")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10)

        for i in range(len(headers)):
            self.header_frame.grid_columnconfigure(i, weight=1)
        
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.header_frame, text=header, font=header_font)
            label.grid(row=0, column=col, sticky="ew", padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="gray")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        self.populate_edit_list(config)

        self.lift()
    def populate_edit_list(self, config):
        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, serial in enumerate(config.serial_variables):
            parameters = [
                serial.variable_name,
                str(serial.variable_number),
                serial.variable_units
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, serial_var=serial: self.edit_serial_var(serial_var, config))
                    label.configure(cursor="hand2")

    def edit_serial_var(self, serial_var, config):
        self.destroy()
        edit_win = edit_serial_variables(serial_var, config)
        edit_win.mainloop()

class edit_serial_variables(ctk.CTkToplevel):
    def __init__(self, serial_var, config):
        super().__init__()
        self.title("Live Serial Reader - Edit Serial Variable")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        self.config = config
        self.serial_var = serial_var
        variable_number = serial_var.variable_number
        self.variable_name = serial_var.variable_name
        self.variable_units = serial_var.variable_units

        self.entry1 = ctk.CTkEntry(self, placeholder_text=f"Variable Number: {variable_number}", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.change_focus(2, event))

        self.entry2 = ctk.CTkEntry(self, placeholder_text=f"Variable Name: {self.variable_name}", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.change_focus(3, event))

        self.entry3 = ctk.CTkEntry(self, placeholder_text=f"Variable Units: {self.variable_units}", width=240)
        self.entry3.grid(row=2, column=0)

        self.button1 = ctk.CTkButton(self, text="Edit Another Variable", command=lambda: self.edit_another_variable(variable_number), width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editing Variables", command=lambda: self.finish_serial_edit(variable_number), width=180)
        self.button2.grid(row=4, column=0)

    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 2:
            self.entry2.focus_set()
        elif entry_box_num == 3:
            self.entry3.focus_set()

    def edit_variable_number(self, variable_number):
        input_num = self.entry1.get().strip()
        serial_variables = self.config.serial_variables
        valid_int = int_check(input_num)
        if valid_int:
            for serial_obj in serial_variables:
                if serial_obj.variable_number == int(input_num):
                    serial_obj.variable_number = variable_number
                    break
            self.serial_var.variable_number = int(input_num)
            return True
        elif input_num == "":
            return True
        else:
            error_message = f'The entry {input_num} is an invalid serial variable number!'
            error_title = "Invalid Serial Number"
            error_function(error_message, error_title, input_num=input_num)
            return False
        
    def edit_variable_name(self):
        input_name = self.entry2.get().strip()
        valid_name = name_check(input_name)
        if valid_name:
            self.variable_name = input_name
            return True
        elif input_name == "":
            return True
        else:
            error_message = "Invalid serial variable name!"
            error_title = "Invalid Serial Name"
            error_function(error_message, error_title)
            return False

    def edit_variable_units(self):
        input_units = self.entry3.get().strip()
        if input_units:
            self.variable_units = input_units
        return True

    def finish_serial_edit(self, variable_number, event=None):
        if self.edit_variable_name() and self.edit_variable_units():
            if self.edit_variable_number(variable_number):
                self.serial_var.variable_name = self.variable_name
                self.serial_var.variable_units = self.variable_units
                for plot_obj in self.config.plots:
                    x_units = [line_obj.x_serial.variable_units for line_obj in plot_obj.lines]
                    x_unit_counter = Counter(x_units)
                    y_units = [line_obj.y_serial.variable_units for line_obj in plot_obj.lines]
                    y_unit_counter = Counter(y_units)
                    if len(x_unit_counter) != 1 or len(y_unit_counter) != 1:
                        incompatible_units = True
                    else:
                        incompatible_units = False
                    new_lines = []
                    for line_obj in plot_obj.lines:
                        if line_obj.x_serial != self.serial_var and line_obj.y_serial != self.serial_var:
                            new_lines.append(line_obj)
                    if incompatible_units:
                        plot_obj.lines = new_lines
                self.destroy()
                return True
        return False

        # if self.edit_variable_name() and self.edit_variable_units():
        #     if self.edit_variable_number(variable_number):
        #         self.serial_var.variable_name = self.variable_name
        #         self.serial_var.variable_units = self.variable_units
        #         for plot_obj in self.config.plots:
        #             x_units = [line_obj.x_serial.variable_units for line_obj in plot_obj.lines]
        #             x_unit_counter = Counter(x_units)
        #             y_units = [line_obj.y_serial.variable_units for line_obj in plot_obj.lines]
        #             y_unit_counter = Counter(y_units)
        #             if len(x_unit_counter) != 1 or len(y_unit_counter) != 1:
        #                 print(f"Plot {plot_obj.plot_title} has incompatible units!")
        #             for line_obj in plot_obj.lines:
        #                 if line_obj.x_serial == self.serial_var and line_obj.y_serial == self.serial_var:
        #                     print(f"Serial Var: {self.serial_var.variable_name} Found as xy-serial for line: {line_obj.get_label()} in Plot: {plot_obj.plot_title}")
        #                 elif line_obj.x_serial == self.serial_var:
        #                     print(f"Serial Var: {self.serial_var.variable_name} Found as x-serial for line: {line_obj.get_label()} in Plot: {plot_obj.plot_title}")
        #                 elif line_obj.y_serial == self.serial_var:
        #                     print(f"Serial Var: {self.serial_var.variable_name} Found as y-serial for line: {line_obj.get_label()} in Plot: {plot_obj.plot_title}")

                        
        #         self.destroy()
        #         return True
        # return False

    def edit_another_variable(self, variable_number, event=None):
        if self.finish_serial_edit(variable_number):
            new_edit_win = edit_serial_variables_list(self.config)
            new_edit_win.mainloop()
        
class delete_serial_variables(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Delete Serial Variables")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        headers = ["Variable Name", "Serial Number", "Variable Units"]
        header_font = ctk.CTkFont(family="Helvetica", size=12, weight="bold")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10)

        for i in range(len(headers)):
            self.header_frame.grid_columnconfigure(i, weight=1)
        
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.header_frame, text=header, font=header_font)
            label.grid(row=0, column=col, sticky="ew", padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="gray")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        self.config = config

        self.populate_delete_list()

        self.lift()

    def populate_delete_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, serial in enumerate(self.config.serial_variables):
            parameters = [
                serial.variable_name,
                str(serial.variable_number),
                serial.variable_units
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, serial_var=serial: self.delete_serial_var(serial_var))
                    label.configure(cursor="hand2")
    
    def delete_serial_var(self, serial_obj):
        new_serial_vars = []
        for serial_var in self.config.serial_variables:
            if serial_var != serial_obj:
                new_serial_vars.append(serial_var)
        self.config.serial_variables = new_serial_vars
        new_lines = []
        for line_obj in self.config.lines:
            if line_obj.x_serial != serial_obj and line_obj.y_serial != serial_obj:
                new_lines.append(line_obj)
        self.config.lines = new_lines
        new_plots = []
        for plot_obj in self.config.plots:
            new_lines = []
            for line_obj in plot_obj.lines:
                if line_obj.x_serial != serial_obj and line_obj.y_serial != serial_obj:
                    new_lines.append(line_obj)
            plot_obj.lines = new_lines
            if plot_obj.lines:
                new_plots.append(plot_obj)
        self.config.plots = new_plots
        self.populate_delete_list()

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, **kwargs)
    error_win.mainloop()