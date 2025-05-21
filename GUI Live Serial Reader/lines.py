import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from serial_variables import serial_variable
import random
import copy
import customtkinter as ctk
from typing import Literal
from color_codes import is_hex_color
from resource_manager import icon_path
from input_check import name_check

global colors
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white','b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def random_color():
    return random.choice(colors)

class line(mlines.Line2D):
    _default_kwargs = {
        'color': (random_color, lambda obj: getattr(obj, '_color'), '_color'),
        'linewidth': (2, lambda obj: getattr(obj, '_linewidth'), '_linewidth'),
        'linestyle': ("solid", lambda obj: getattr(obj, '_linestyle'), '_linestyle'),
        'marker': ("None", lambda obj: getattr(obj, '_marker').get_marker(), '_marker.get_marker'),
        'markersize': (6.0, lambda obj: getattr(obj, '_markersize'), '_markersize'),
        'markeredgewidth': (1.0, lambda obj: getattr(obj, '_markeredgewidth'), '_markeredgewidth'),
        'markeredgecolor': (random_color, lambda obj: getattr(obj, '_markeredgecolor'), '_markeredgecolor'),
        'markerfacecolor': (random_color, lambda obj: getattr(obj, '_markerfacecolor'), '_markerfacecolor'),
        'markerfacecoloralt': ('none', lambda obj: getattr(obj, '_markerfacecoloralt'), '_markerfacecoloralt'),
        'label': (None, lambda obj: getattr(obj, '_label'), '_label'),
        'gapcolor': (None, lambda obj: getattr(obj, '_gapcolor'), '_gapcolor'),
        'fillstyle': ("full", lambda obj: getattr(obj, '_marker').get_fillstyle(), '_marker.get_fillstyle'),
        'antialiased': (False, lambda obj: getattr(obj, '_antialiased'), '_antialiased'),
        'dash_capstyle': ("butt", lambda obj: getattr(obj, '_dashcapstyle'), '_dashcapstyle'),
        'solid_capstyle': ("butt", lambda obj: getattr(obj, '_solidcapstyle'), '_solidcapstyle'),
        'dash_joinstyle': ("round", lambda obj: getattr(obj, '_dashjoinstyle'), '_dashjoinstyle'),
        'solid_joinstyle': ("miter", lambda obj: getattr(obj, '_solidjoinstyle'), '_solidjoinstyle'),
        'pickradius': (5.0, lambda obj: getattr(obj, '_pickradius'), '_pickradius'),
        'drawstyle': ("default", lambda obj: getattr(obj, '_drawstyle'), '_drawstyle'),
        'markevery': (None, lambda obj: getattr(obj, '_markevery'), '_markevery')
    }

    def __init__(self, x_serial: serial_variable, y_serial: serial_variable, **kwargs):
        # Set defaults for kwargs not passed as arguments
        for key, (default, _, _) in self._default_kwargs.items():
            if key not in kwargs:
                kwargs[key] = default if not callable(default) else default()

        # Store serial objects and specify data
        self.x_serial = x_serial
        self.y_serial = y_serial
        self.xdata = x_serial.data_array
        self.ydata = y_serial.data_array

        # Construct Line2D
        super().__init__(self.xdata, self.ydata, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, line):
            return False
        return (
            self.x_serial == other.x_serial and
            self.y_serial == other.y_serial and 
            all(getter(self) == getter(other) for (_, getter, _) in self._default_kwargs.values())
        )

    def __hash__(self):
        hash_list = [self.x_serial, self.y_serial]
        kwargs = [getter(self) for (_, getter, _) in self._default_kwargs.values()]
        hash_list = hash_list + kwargs
        hash_tuple = tuple(hash_list)
        return hash(hash_tuple)

    def __str__(self):
        return f"Label: {self.get_label()}, X Serial: {self.x_serial}, Y Serial: {self.y_serial}"

    def duplicate(self):
        duplicate_kwargs = {key: getter(self) for key, (_, getter, _) in self._default_kwargs.items()}
        line_obj = line(self.x_serial, self.y_serial, **duplicate_kwargs)
        # line_obj.expose_private_attributes()
        return line_obj
    
    # def expose_private_attributes(self):
    #     if hasattr(self, '_color'):
    #         self.set_color(getattr(self, '_color'))
    #     if hasattr(self, '_linewidth'):
    #         self.set_linewidth(getattr(self, '_linewidth'))
    #     if hasattr(self, '_linestyle'):
    #         self.set_linestyle(getattr(self, '_linestyle'))
    #     if hasattr(self, '_marker.get_marker'):
    #         self.set_marker(getattr(self, '_marker.get_marker')())
    #     if hasattr(self, '_markersize'):
    #         self.set_markersize(getattr(self, '_markersize'))
    #     if hasattr(self, '_markeredgewidth'):
    #         self.set_markeredgewidth(getattr(self, '_markeredgewidth'))
    #     if hasattr(self, '_markeredgecolor'):
    #         self.set_markeredgecolor(getattr(self, '_markeredgecolor'))
    #     if hasattr(self, '_markerfacecolor'):
    #         self.set_markerfacecolor(getattr(self, '_markerfacecolor'))
    #     if hasattr(self, '_markerfacecoloralt'):
    #         self.set_markerfacecoloralt(getattr(self, '_markerfacecoloralt'))
    #     if hasattr(self, '_label'):
    #         self.set_label(getattr(self, '_label'))
    #     if hasattr(self, '_gapcolor'):
    #         self.set_gapcolor(getattr(self, '_gapcolor'))
    #     if hasattr(self, '_marker.get_fillstyle'):
    #         self.set_fillstyle(getattr(self, '_marker.get_fillstyle')())
    #     if hasattr(self, '_antialiased'):
    #         self.set_antialiased(getattr(self, '_antialiased'))
    #     if hasattr(self, '_dash_capstyle'):
    #         self.set_dash_capstyle(getattr(self, '_dash_capstyle'))
    #     if hasattr(self, '_solid_capstyle'):
    #         self.set_solid_capstyle(getattr(self, '_solid_capstyle'))
    #     if hasattr(self, '_dash_joinstyle'):
    #         self.set_dash_joinstyle(getattr(self, '_dash_joinstyle'))
    #     if hasattr(self, '_solid_joinstyle'):
    #         self.set_solid_joinstyle(getattr(self, '_solid_joinstyle'))
    #     if hasattr(self, '_pickradius'):
    #         self.set_pickradius(getattr(self, '_pickradius'))
    #     if hasattr(self, '_drawstyle'):
    #         self.set_drawstyle(getattr(self, '_drawstyle'))
    #     if hasattr(self, '_markevery'):
    #         self.set_markevery(getattr(self, '_markevery'))

        # for public_attribute, (_, private_getter, private_attribute) in self._default_kwargs.items():
        #     if hasattr(self, private_attribute):
        #         getattr(self, f"set_{public_attribute}")(private_getter(self))

    def line_to_dict(self):
        return {
            "x_serial": self.x_serial.serial_to_dict(),
            "y_serial": self.y_serial.serial_to_dict(),
            **{key: getter(self) for key, (_, getter, _) in self._default_kwargs.items()}
        }

    def line_from_dict(json_line, serial_objs=None):
        if set(json_line) != {"x_serial", "y_serial", *line._default_kwargs}:
            error_message = "A line object is corrupted!\nPlease edit or wipe configurations.json!"
            error_title = "CORRUPTED LINE IN JSON FILE"
            error_function(error_message, error_title)
            return
        if serial_objs is None:
            x_serial = serial_variable.serial_from_dict(json_line["x_serial"])
            y_serial = serial_variable.serial_from_dict(json_line["y_serial"])
        else:
            x_serial = next((sv for sv in serial_objs if sv == serial_variable.serial_from_dict(json_line["x_serial"])))
            y_serial = next((sv for sv in serial_objs if sv == serial_variable.serial_from_dict(json_line["y_serial"])))
        kwargs = {key: json_line.get(key, None) for key in line._default_kwargs}
        if x_serial is None or y_serial is None:
            error_message = "A line object is corrupted!\nPlease edit or wipe configurations.json!"
            error_title = "CORRUPTED LINE IN JSON FILE"
            error_function(error_message, error_title)
            return
        line_obj = line(x_serial, y_serial, **kwargs)
        # print(f'Private Label Attribute: {getattr(line_obj, '_label')}')
        # line_obj.expose_private_attributes()
        # print(f'Public Label Attribute: {line_obj.get_label()}\n')
        # # print(f'Public Label Attribute: {getattr(line_obj, 'get_label')()}\n')
        return line_obj

    def update_line(self):
        self.set_xdata(self.x_serial.data_array)
        self.set_ydata(self.y_serial.data_array)

    def is_valid_line(self):
        valid_line = True
        if not self.x_serial or not isinstance(self.x_serial, serial_variable):
            valid_line = False
        elif not self.x_serial.is_valid_serial_var():
            valid_line = False
        elif not self.y_serial or not isinstance(self.y_serial, serial_variable):
            valid_line = False
        elif not self.y_serial.is_valid_serial_var():
            valid_line = False
        elif not self.get_label():
            valid_line = False
        if not valid_line:
            print(f"Invalid line detected!")
        return valid_line
        
class add_basic_line(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Basic Line")
        self.geometry("590x225")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        self.config = config
        self.x_serial = 0
        self.y_serial = 0
        self.label = ""
        self.color = ""

        if not len(config.serial_variables):
            error_message = "Add serial variables first in order to create a line!"
            error_title = "No Serial Variables Exist"
            error_function(error_message, error_title)
            self.destroy()

        serials = [f"{serial_var}" for serial_var in config.serial_variables]

        self.label1 = ctk.CTkLabel(self, text="X-Value Serial Variable:")
        self.label1.grid(row=0, column=0, padx=8, pady=8)

        default_x_serial = ctk.StringVar(value=serials[0])
        self.add_serial_to_line("x", default_x_serial)
        self.entry1 = ctk.CTkOptionMenu(self, variable=default_x_serial, values=serials, width=395, command=lambda value: self.add_serial_to_line("x", value))
        self.entry1.grid(row=0, column=1, padx=8, pady=8)

        self.label2 = ctk.CTkLabel(self, text="Y-Value Serial Variable:")
        self.label2.grid(row=1, column=0, padx=8, pady=8)

        default_y_serial = ctk.StringVar(value=serials[0])
        self.add_serial_to_line("y", default_y_serial)
        self.entry2 = ctk.CTkOptionMenu(self, variable=default_y_serial, values=serials, width=395, command=lambda value: self.add_serial_to_line("y", value))
        self.entry2.grid(row=1, column=1, padx=8, pady=8)

        self.label3 = ctk.CTkLabel(self, text="Line Label:")
        self.label3.grid(row=2, column=0, padx=8, pady=8)

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter label here...", width=395)
        self.entry3.grid(row=2, column=1, padx=8, pady=8)
        self.entry3.bind("<Return>", lambda event: self.change_focus(4, event))

        self.label4 = ctk.CTkLabel(self, text="Line Color (optional):")
        self.label4.grid(row=3, column=0, padx=8, pady=8)

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter color or hex code here...", width=395)
        self.entry4.grid(row=3, column=1, padx=8, pady=8)

        self.button1 = ctk.CTkButton(self, text="Add Another Line", command=self.add_another_line)
        self.button1.grid(row=4, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Lines", command=self.add_line_to_config)
        self.button2.grid(row=4, column=1)

    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 4:
            self.entry4.focus_set()

    def add_serial_to_line(self, axis: Literal["x", "y"], serial_var: str):
        if isinstance(serial_var,ctk.StringVar):
            serial_var = serial_var.get().split(",")
        elif isinstance(serial_var, str):
            serial_var = serial_var.split(",")
        if axis == "x":
            serial_num = int(serial_var[1].strip()[len("Serial Num: "):])
            for serial_obj in self.config.serial_variables:
                if serial_num == serial_obj.variable_number:
                    self.x_serial = serial_obj
                    break
        elif axis == "y":
            serial_num = int(serial_var[1].strip()[len("Serial Num: "):])
            for serial_obj in self.config.serial_variables:
                if serial_num == serial_obj.variable_number:
                    self.y_serial = serial_obj
                    break
        else:
            return

    def add_label_to_line(self):
        label = self.entry3.get().strip()
        valid_label = name_check(label)
        if valid_label:
            self.label = label
            return True
        else:
            error_message = f'The label "{label}" is invalid!'
            error_title = "Invalid Line Label"
            error_function(error_message, error_title, label=label)
            return False

    def add_color_to_line(self):
        color = self.entry4.get().lower().strip()
        if color in colors:
            self.color = color
            return True
        elif is_hex_color(color):
            self.color = color
            return True
        elif color == "":
            self.color = color
            return True
        else:
            error_message = f'The color code "{color}" is invalid!'
            error_title = "Invalid Line Color"
            error_function(error_message, error_title, color=color)
            return False

    def add_line_to_config(self, event=None):
        if self.add_label_to_line() and self.add_color_to_line():
            if self.color != "":
                new_line_obj = line(self.x_serial, self.y_serial, label=self.label, color=self.color)
            elif self.color == "":
                new_line_obj = line(self.x_serial, self.y_serial, label=self.label)
            self.config.lines.append(new_line_obj)
            self.destroy()
            return True
        return False

    def add_another_line(self, event=None):
        if self.add_line_to_config():
            new_add_line_window = add_basic_line(self.config)
            new_add_line_window.mainloop()

class edit_basic_line_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Lines")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        headers = ["Line Label", "X Serial Var", "Y Serial Var", "Color"]
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

        self.line_objs = config.lines
        self.populate_line_list(config)

        self.lift()
    def populate_line_list(self, config):
        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, line_obj in enumerate(config.lines):
            parameters = [
                line_obj.get_label(),
                line_obj.x_serial.variable_name,
                line_obj.y_serial.variable_name,
                line_obj.get_color()
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, line_var=line_obj: self.edit_basic_line(line_var, config))
                    label.configure(cursor="hand2")

    def edit_basic_line(self, line_obj, config):
        self.destroy()
        edit_win = edit_basic_line(line_obj, config)
        edit_win.mainloop()

class edit_basic_line(ctk.CTkToplevel):
    def __init__(self, line_obj, config):
        super().__init__()
        self.title(f"Live Serial Reader - Edit Line \"{line_obj.get_label()}\"")
        self.geometry("590x225")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        self.config = config
        self.line_obj = line_obj
        self.x_serial = line_obj.x_serial
        self.y_serial = line_obj.y_serial
        self.label = line_obj.get_label()
        self.color = line_obj.get_color()

        if not len(config.serial_variables):
            error_message = "Add serial variables first in order to edit lines!"
            error_title = "No Serial Variables Exist"
            error_function(error_message, error_title)
            self.destroy()

        serials = [f"{serial_var}" for serial_var in config.serial_variables]

        self.label1 = ctk.CTkLabel(self, text="X-Value Serial Variable:")
        self.label1.grid(row=0, column=0, padx=8, pady=8)

        x_index = serials.index(f"{self.x_serial}")

        default_x_serial = ctk.StringVar(value=serials[x_index])
        self.entry1 = ctk.CTkOptionMenu(self, variable=default_x_serial, values=serials, width=395, command=lambda value: self.edit_serial_to_line("x", value))
        self.entry1.grid(row=0, column=1, padx=8, pady=8)

        self.label2 = ctk.CTkLabel(self, text="Y-Value Serial Variable:")
        self.label2.grid(row=1, column=0, padx=8, pady=8)

        y_index = serials.index(f"{self.y_serial}")

        default_y_serial = ctk.StringVar(value=serials[y_index])
        self.entry2 = ctk.CTkOptionMenu(self, variable=default_y_serial, values=serials, width=395, command=lambda value: self.edit_serial_to_line("y", value))
        self.entry2.grid(row=1, column=1, padx=8, pady=8)

        self.label3 = ctk.CTkLabel(self, text="Line Label:")
        self.label3.grid(row=2, column=0)

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter label here...", width=395)
        self.entry3.grid(row=2, column=1, padx=8, pady=8)
        self.entry3.bind("<Return>", lambda event: self.change_focus(4, event))

        self.label4 = ctk.CTkLabel(self, text="Line Color (optional):")
        self.label4.grid(row=3, column=0, padx=8, pady=8)

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter color or hex code here...", width=395)
        self.entry4.grid(row=3, column=1)
    
        self.button1 = ctk.CTkButton(self, text="Edit Another Line", command=self.edit_another_line)
        self.button1.grid(row=4, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editiing Lines", command=self.finish_line_edit)
        self.button2.grid(row=4, column=1)

    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 4:
            self.entry4.focus_set()
    
    def edit_serial_to_line(self, axis: Literal["x", "y"], serial_var: str):
        if isinstance(serial_var,ctk.StringVar):
            serial_var = serial_var.get().split(",")
        elif isinstance(serial_var, str):
            serial_var = serial_var.split(",")
        if axis == "x":
            serial_num = int(serial_var[1].strip()[len("Serial Num: "):])
            for serial_obj in self.config.serial_variables:
                if serial_num == serial_obj.variable_number:
                    self.x_serial = serial_obj
                    break
        elif axis == "y":
            serial_num = int(serial_var[1].strip()[len("Serial Num: "):])
            for serial_obj in self.config.serial_variables:
                if serial_num == serial_obj.variable_number:
                    self.y_serial = serial_obj
                    break
        else:
            return
        
    def edit_label_to_line(self):
        label = self.entry3.get().strip()
        valid_label = name_check(label)
        if valid_label:
            self.label = label
            return True
        elif label == "":
            return True
        else:
            error_message = f'The label "{label}" is invalid or already exists!'
            error_title = "Invalid Line Label"
            error_function(error_message, error_title, label=label)
            return False

    def edit_color_to_line(self):
        color = self.entry4.get().lower().strip()
        if color in colors:
            self.color = color
            return True
        elif is_hex_color(color):
            self.color = color
            return True
        elif color == "":
            return True
        else:
            error_message = f'The color code "{color}" is invalid!'
            error_title = "Invalid Line Color"
            error_function(error_message, error_title, color=color)
            return False

    def finish_line_edit(self, event=None):
        if self.edit_label_to_line() and self.edit_color_to_line():
            self.line_obj.x_serial = self.x_serial
            self.line_obj.y_serial = self.y_serial
            self.line_obj.set_label(self.label)
            self.line_obj.set_color(self.color)
            self.line_obj.update_line()
            self.destroy()
            for plot_obj in self.config.plots:
                new_lines = []
                x_units_collection = []
                y_units_collection = []
                for line_obj in plot_obj.lines:
                    if line_obj == self.line_obj:
                        x_units_collection.append(line_obj.x_serial.variable_units)
                        y_units_collection.append(line_obj.y_serial.variable_units)
                    elif line_obj != self.line_obj:
                        x_units_collection.append(line_obj.x_serial.variable_units)
                        y_units_collection.append(line_obj.y_serial.variable_units)
                        new_lines.append(line_obj)
                if len(x_units_collection) > 2 or len(x_units_collection) < 1 or len(x_units_collection) > 2 or len(x_units_collection) < 1:
                    plot_obj.lines = []
                elif len(x_units_collection) == 2 or len(y_units_collection) == 2:
                    plot_obj.lines = new_lines
                elif len(x_units_collection) == 1 and len(y_units_collection) == 1:
                    continue
            self.config.remove_lineless_plots()
            return True
        return False

    def edit_another_line(self, event=None):
        if self.finish_line_edit():
            new_edit_line_window = edit_basic_line_list(self.config)
            new_edit_line_window.mainloop()

class delete_lines(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Delete Lines")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        headers = ["Line Label", "X Serial Variable", "Y Serial Variable", "Color"]
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
        
        line_list = []
        for row_idx, line_obj in enumerate(self.config.lines):
            parameters = [
                line_obj.get_label(),
                line_obj.x_serial.variable_name,
                line_obj.y_serial.variable_name,
                line_obj.get_color()
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event: self.delete_line(line_obj))
                    label.configure(cursor="hand2")

    def delete_line(self, line_obj):
        new_lines = []
        for config_line in self.config.lines:
            if config_line != line_obj:
                new_lines.append(config_line)
        self.config.lines = new_lines
        new_plots = []
        for plot_obj in self.config.plots:
            new_lines = []
            for plot_line in plot_obj.lines:
                if plot_line != line_obj:
                    new_lines.append(plot_line)
            plot_obj.lines = new_lines
            if plot_obj.lines:
                new_plots.append(plot_obj)
        self.config.plots = new_plots
        self.populate_delete_list()

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, **kwargs)
    error_win.mainloop()