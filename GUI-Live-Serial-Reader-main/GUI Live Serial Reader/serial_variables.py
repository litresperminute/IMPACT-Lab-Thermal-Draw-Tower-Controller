import customtkinter as ctk
from file_manager import icon_path

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

    def __str__(self):
        return f"Serial_Name: {self.variable_name}, Serial_Num: {self.variable_number}, Serial_Units: {self.variable_units}"

    def serial_to_dict(self):
        return {
            "variable_number": self.variable_number,
            "variable_name": self.variable_name,
            "variable_units": self.variable_units,
            "data_array": []
        }

    def serial_from_dict(sub_data):
        return serial_variable(sub_data["variable_number"], sub_data["variable_name"], sub_data["variable_units"], sub_data["data_array"])

class add_serial_variable(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Serial Variable")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        variable_number = 0
        variable_name = ""
        variable_units = ""
        data_array = []
        serial_var = serial_variable(variable_number, variable_name, variable_units, data_array)

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter variable number...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.add_variable_number(serial_var, config))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter variable name...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.add_variable_name(serial_var, config))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter variable units...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.add_variable_units(serial_var))

        self.button1 = ctk.CTkButton(self, text="Add Another Variable", command=lambda: self.add_another_variable(serial_var, config), width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Variables", command=lambda: self.add_serial_variable_to_config(serial_var, config), width=180)
        self.button2.grid(row=4, column=0)
    
    def add_variable_number(self, serial_var, config, event=None):
        number = self.entry1.get().strip()
        valid_number = True

        for serial in config.serial_variables:
            if number == str(serial.variable_number):
                valid_number = False

        if valid_number and number.isnumeric() == True and "-" not in number and "." not in number:
            serial_var.variable_number = int(number)
            self.entry2.focus_set()
        else:
            error_message = "The serial number entered already exists or is invalid:\n\n\"{serial_num}\""
            error_title = "Duplicate Serial Variable"
            serial_error1(error_message, error_title, number)

    def add_variable_name(self, serial_var, config, event=None):
        name = self.entry2.get().strip()
        valid_name = True
        
        if not name:
            valid_name = False

        for serial in config.serial_variables:
            if name == serial.variable_name:
                valid_name = False

        if valid_name:
            serial_var.variable_name = name
            self.entry3.focus_set()
        else:
            error_message = "The serial name enetered already exists:\n\n\"{serial_name}\""
            error_title = "Duplicate Serial Name"
            serial_error2(error_message, error_title, name)

    def add_variable_units(self, serial_var, event=None):
        units = self.entry3.get().strip()
        if not units:
            error_message = "No units have been entered."
            error_title = "No Units"
            unit_error(error_message, error_title)
        else:
            serial_var.variable_units = units
        
    def add_serial_variable_to_config(self, serial_var, config, event=None):
        config.serial_variables.append(serial_var)
        self.destroy()

    def add_another_variable(self, serial_var, config, event=None):
        self.add_serial_variable_to_config(serial_var, config)
        new_add_var_window = add_serial_variable(config)
        new_add_var_window.mainloop()

    #def add_serial_error1(self, serial_num):
        #self.destroy()
        #serial_error1(serial_num)

    #def add_serial_error2(self, serial_name):
        #self.destroy()
        #serial_error2(serial_name)

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

        self.serial_vars = config.serial_variables
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

        serial_var_ID = config.serial_variables.index(serial_var)

        variable_number = serial_var.variable_number
        variable_name = serial_var.variable_name
        variable_units = serial_var.variable_units

        self.entry1 = ctk.CTkEntry(self, placeholder_text=f"Variable Number: {variable_number}", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.edit_variable_number(serial_var, config))

        self.entry2 = ctk.CTkEntry(self, placeholder_text=f"Variable Name: {variable_name}", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.edit_variable_name(serial_var, config))

        self.entry3 = ctk.CTkEntry(self, placeholder_text=f"Variable Units: {variable_units}", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.edit_variable_units(serial_var, config))

        self.button1 = ctk.CTkButton(self, text="Edit Another Variable", command=lambda: self.edit_another_variable(serial_var, config, serial_var_ID), width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editing Variables", command=lambda: self.edit_serial_variable_in_config(serial_var, config, serial_var_ID), width=180)
        self.button2.grid(row=4, column=0)

    def edit_variable_number(self, serial_var, config, event=None):
        number = self.entry1.get().strip()
        valid_number = True

        # for serial in config.serial_variables:
        #     if number == str(serial.variable_number):
        #         valid_number = False

        if valid_number and number.isnumeric() == True and "-" not in number and "." not in number:

            for serial in config.serial_variables:
                if number == str(serial.variable_number):
                    serial.variable_number = serial_var.variable_number

            for line_obj in config.lines:
                for plot_obj in config.plots:
                    if line_obj in plot_obj.lines and serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].x_serial.variable_number = int(number)
                        plot_obj.lines[plot_obj.lines.index(line_obj)].y_serial.variable_number = int(number)
                    elif line_obj in plot_obj.lines and serial_var == line_obj.x_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].x_serial.variable_number = int(number)
                    elif line_obj in plot_obj.lines and serial_var == line_obj.y_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].y_serial.varible_number = int(number)
                if serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                    line_obj.x_serial.variable_number = int(number)
                    line_obj.y_serial.variable_number = int(number)
                elif serial_var == line_obj.x_serial:
                    line_obj.x_serial.variable_number = int(number)
                elif serial_var == line_obj.y_serial:
                    line_obj.y_serial.variable_number = int(number)

            serial_var.variable_number = int(number)
            self.entry2.focus_set()
        else:
            error_message = "The serial number entered already exists or is invalid:\n\n\"{serial_num}\""
            error_title = "Duplicate Serial Variable"
            serial_error1(error_message, error_title, number)

    def edit_variable_name(self, serial_var, config, event=None):
        name = self.entry2.get().strip()
        valid_name = True
        
        for serial in config.serial_variables:
            if name == serial.variable_name:
                valid_name = False

        if not serial_var.variable_name:
            valid_name = False

        if valid_name:

            for line_obj in config.lines:
                for plot_obj in config.plots:
                    if line_obj in plot_obj.lines and serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].x_serial.variable_name = name
                        plot_obj.lines[plot_obj.lines.index(line_obj)].y_serial.variable_name = name
                    elif line_obj in plot_obj.lines and serial_var == line_obj.x_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].x_serial.variable_name = name
                    elif line_obj in plot_obj.lines and serial_var == line_obj.y_serial:
                        plot_obj.lines[plot_obj.lines.index(line_obj)].y_serial.variable_name = name
                if serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                    line_obj.x_serial.variable_name = name
                    line_obj.y_serial.variable_name = name
                elif serial_var == line_obj.x_serial:
                    line_obj.x_serial.variable_name = name
                elif serial_var == line_obj.y_serial:
                    line_obj.y_serial.variable_name = name

            serial_var.variable_name = name
            self.entry3.focus_set()
        else:
            error_message = "The serial name enetered already exists:\n\n\"{serial_name}\""
            error_title = "Duplicate Serial Name"
            serial_error2(error_message, error_title, name)

    def edit_variable_units(self, serial_var, config, event=None):
        units = self.entry3.get().strip()
        valid_units = True
        if not units:
            valid_units = False

        if valid_units:

            for line_obj in config.lines:
                for plot_obj in config.plots:
                    if line_obj in plot_obj.lines and len(plot_obj.lines) == 1 and serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                        plot_obj.lines[0].x_serial.variable_units = units
                        plot_obj.lines[0].y_serial.variable_units = units
                    elif line_obj in plot_obj.lines and len(plot_obj.lines) == 1 and serial_var == line_obj.x_serial:
                        plot_obj.lines[0].x_serial.variable_units = units
                    elif line_obj in plot_obj.lines and len(plot_obj.lines) == 1 and serial_var == line_obj.y_serial:
                        plot_obj.lines[0].y_serial.variable_units = units
                    elif line_obj in plot_obj.lines and (serial_var == line_obj.x_serial or serial_var == line_obj.y_serial):
                        plot_obj.lines.remove(line_obj)
                if serial_var == line_obj.x_serial and serial_var == line_obj.y_serial:
                    line_obj.x_serial.variable_units = units
                    line_obj.y_serial.variable_units = units
                elif serial_var == line_obj.x_serial:
                    line_obj.x_serial.variable_units = units
                elif serial_var == line_obj.y_serial:
                    line_obj.y_serial.variable_units = units

            serial_var.variable_units = units

    def edit_serial_variable_in_config(self, serial_var, config, serial_var_ID, event=None):
        config.serial_variables[serial_var_ID] = serial_var
        self.destroy()

    def edit_another_variable(self, serial_var, config, serial_var_ID, event=None):
        self.edit_serial_variable_in_config(serial_var, config, serial_var_ID)
        new_edit_win = edit_serial_variables_list(config)
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

        self.serial_vars = config.serial_variables

        self.populate_delete_list(config)

        self.lift()

    def populate_delete_list(self, config):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

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
                    label.bind("<Button-1>", lambda event, serial_var=serial: self.delete_serial_var(serial_var, config))
                    label.configure(cursor="hand2")
    
    def delete_serial_var(self, serial_var, config):
        for line_obj in config.lines:
            if line_obj.x_serial == serial_var or line_obj.y_serial == serial_var:
                config.lines.remove(line_obj)
                for plot_obj in config.plots:
                    if line_obj in plot_obj.lines:
                        config.plots[config.plots.index(plot_obj)].lines = [
                            L for L in config.plots[config.plots.index(plot_obj)].lines if L != line_obj
                        ]

        for serial in config.serial_variables:
            if serial == serial_var:
                config.serial_variables.remove(serial)
        self.populate_delete_list(config)

def serial_error1(error_message, error_title, serial_num):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, serial_num=serial_num)
    error_win.mainloop()

def serial_error2(error_message, error_title, serial_name):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, serial_name=serial_name)
    error_win.mainloop()

def unit_error(error_message, error_title):
    from warning_window import error_window
    error_win = error_window(error_message, error_title)
    error_win.mainloop()