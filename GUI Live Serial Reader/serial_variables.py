import customtkinter as ctk

class serial_variable:
    def __init__(self, variable_number: int, variable_name: str, variable_units: str, data_array: list):
        # Serial Variable Object Attributes
        self.variable_number = variable_number
        self.variable_name = variable_name
        self.variable_units = variable_units
        self.data_array = data_array
    
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
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
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
        number = self.entry1.get()
        valid_number = True

        for serial in config.serial_variables:
            if number == str(serial.variable_number):
                valid_number = False

        if valid_number and number.isnumeric() == True and "-" not in number and "." not in number:
            serial_var.variable_number = int(number)
        else:
            serial_error1(number)

    def add_variable_name(self, serial_var, config, event=None):
        name = self.entry2.get()
        valid_name = True
        
        for serial in config.serial_variables:
            if name == serial.variable_name:
                valid_name = False

        if valid_name:
            serial_var.variable_name = name
        else:
            serial_error2(name)

    def add_variable_units(self, serial_var, event=None):
        units = self.entry3.get()
        serial_var.variable_units = units

    def add_serial_variable_to_config(self, serial_var, config, event=None):
        config.serial_variables.append(serial_var)
        self.destroy()

    def add_another_variable(self, serial_var, config, event=None):
        self.add_serial_variable_to_config(serial_var, config)
        new_add_var_window = add_serial_variable(config)
        new_add_var_window.mainloop()

    def add_serial_error1(self, serial_num):
        self.destroy()
        serial_error1(serial_num)

    def add_serial_error2(self, serial_name):
        self.destroy()
        serial_error2(serial_name)

class edit_serial_variables_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Serial Variables")
        self.geometry("435x200")
        self.resizable(False, False)
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
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
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
        self.entry3.bind("<Return>", lambda event: self.edit_variable_units(serial_var))

        self.button1 = ctk.CTkButton(self, text="Edit Another Variable", command=lambda: self.edit_another_variable(serial_var, config, serial_var_ID), width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editing Variables", command=lambda: self.edit_serial_variable_in_config(serial_var, config, serial_var_ID), width=180)
        self.button2.grid(row=4, column=0)

    def edit_variable_number(self, serial_var, config, event=None):
        number = self.entry1.get()
        valid_number = True

        for serial in config.serial_variables:
            if number == str(serial.variable_number):
                valid_number = False

        if valid_number and number.isnumeric() == True and "-" not in number and "." not in number:
            serial_var.variable_number = int(number)
        else:
            serial_error1(number)

    def edit_variable_name(self, serial_var, config, event=None):
        name = self.entry2.get()
        valid_name = True
        
        for serial in config.serial_variables:
            if name == serial.variable_name:
                valid_name = False

        if serial_var.variable_name == '':
            valid_name = False

        if valid_name:
            serial_var.variable_name = name
        else:
            serial_error2(name)

    def edit_variable_units(self, serial_var, event=None):
        units = self.entry3.get()
        serial_var.variable_units = units

    def edit_serial_variable_in_config(self, serial_var, config, serial_var_ID, event=None):
        config.serial_variables[serial_var_ID] = serial_var
        self.destroy()

    def edit_another_variable(self, serial_var, config, serial_var_ID, event=None):
        self.edit_serial_variable_in_config(serial_var, config, serial_var_ID)
        new_edit_win = edit_serial_variables_list(config)
        new_edit_win.mainloop()

    def edit_serial_error1(self, serial_num):
        self.destroy()
        serial_error1(serial_num)

    def edit_serial_error2(self, serial_name):
        self.destroy()
        serial_error2(serial_name)

class delete_serial_variables(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Delete Serial Variables")
        self.geometry("435x200")
        self.resizable(False, False)
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
        for serial in config.serial_variables:
            if serial.variable_number == serial_var.variable_number:
                config.serial_variables.remove(serial)
        self.populate_delete_list(config)

def serial_error1(serial_num):
    from warning_windows import serial_error_window1
    warning_win = serial_error_window1(serial_num)
    warning_win.mainloop()

def serial_error2(serial_name):
    from warning_windows import serial_error_window2
    warning_win = serial_error_window2(serial_name)
    warning_win.mainloop()