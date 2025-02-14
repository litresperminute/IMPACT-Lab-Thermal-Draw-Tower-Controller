import customtkinter as ctk

class serial_variable:
    def __init__(self, variable_number: int, variable_name: str, variable_units: str):
        # Serial Variable Object Attributes
        self.variable_number = variable_number
        self.variable_name = variable_name
        self.variable_units = variable_units
    
    def serial_to_dict(self):
        return {
            "variable_number": self.variable_number,
            "variable_name": self.variable_name,
            "variable_units": self.variable_units
        }

    def serial_from_dict(sub_data):
        return serial_variable(sub_data["variable_number"], sub_data["variable_name"], sub_data["variable_units"])

class add_serial_variable(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Serial Variable")
        self.geometry("435x200")
        self.resizable(False, False)
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        variable_number = 0
        variable_name = ""
        variable_units = ""
        serial_var = serial_variable(variable_number, variable_name, variable_units)

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter variable number...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", self.add_variable_number(serial_var))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter variable name...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", self.add_variable_name(serial_var))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter variable units...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", self.add_variable_units(serial_var))

        self.button1 = ctk.CTkButton(self, text="Add Another Variable", command=lambda: self.add_another_variable(config), width=180)
        self.button1.grid(row=3, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Variables", command=lambda: self.add_serial_variable_to_config(serial_var, config), width=180)
        self.button2.grid(row=4, column=0)
    
    def add_variable_number(self, serial_var, event=None):
        number = self.entry1.get()

        if number.isnumeric() == True and "-" not in number and "." not in number:
            serial_var.variable_number = int(number)
        else:
            # PLACEHOLDER CODE BELOW
            # NEED TO ADD ERROR WINDOW
            # ERROR IF THERE ARE DUPLICATE NUMBERS
            # ERROR IF NUMBER IS NOT POSITIVE INTEGER
            serial_var.variable_number = 0

    def add_variable_name(self, serial_var, event=None):
        name = self.entry2.get()
        serial_var.variable_name = name

    def add_variable_units(self, serial_var, event=None):
        units = self.entry3.get()
        serial_var.variable_units = units

    def add_serial_variable_to_config(self, serial_var, config):
        config.serial_variables.append(serial_var)
        self.destroy()


    def add_another_variable(self, config):
        self.destroy()
        new_add_var_window = add_serial_variable(config)
        new_add_var_window.mainloop()