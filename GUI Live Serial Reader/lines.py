import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from serial_variables import serial_variable
import random
import customtkinter as ctk
from typing import Literal
import color_codes

global colors
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white',
          'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

class line(mlines.Line2D):
    def __init__(self, x_serial: serial_variable, y_serial: serial_variable, **kwargs):
        # Set default line settings
        kwargs.setdefault('color', random.choice(colors))
        kwargs.setdefault('linewidth', 2)
        kwargs.setdefault('linestyle', 'solid')
        kwargs.setdefault('marker', None)
        kwargs.setdefault('markersize', None)
        kwargs.setdefault('markeredgewidth', None)
        kwargs.setdefault('markeredgecolor', None)
        kwargs.setdefault('markerfacecolor', None)
        kwargs.setdefault('markerfacecoloralt', 'none')
        kwargs.setdefault('label', None)
        kwargs.setdefault('gapcolor', None)
        kwargs.setdefault('fillstyle', None)
        kwargs.setdefault('antialiased', None)
        kwargs.setdefault('dash_capstyle', None)
        kwargs.setdefault('solid_capstyle', None)
        kwargs.setdefault('dash_joinstyle', None)
        kwargs.setdefault('solid_joinstyle', None)
        kwargs.setdefault('pickradius', 5)
        kwargs.setdefault('drawstyle', None)
        kwargs.setdefault('markevery', None)

        # Define xdata and ydata
        xdata, ydata = x_serial.data_array, y_serial.data_array

        # Define object attributes
        self.x_serial = x_serial
        self.y_serial = y_serial
        self.xdata = xdata
        self.ydata = ydata
        self.color = kwargs['color']
        self.linewidth = kwargs['linewidth']
        self.linestyle = kwargs['linestyle']
        self.marker = kwargs['marker']
        self.markersize = kwargs['markersize']
        self.markeredgewidth = kwargs['markeredgewidth']
        self.markeredgecolor = kwargs['markeredgecolor']
        self.markerfacecolor = kwargs['markerfacecolor']
        self.markerfacecoloralt = kwargs['markerfacecoloralt']
        self.label = kwargs['label']
        self.gapcolor = kwargs['gapcolor']
        self.fillstyle = kwargs['fillstyle']
        self.antialiased = kwargs['antialiased']
        self.dash_capstyle = kwargs['dash_capstyle']
        self.solid_capstyle = kwargs['solid_capstyle']
        self.dash_joinstyle = kwargs['dash_joinstyle']
        self.solid_joinstyle = kwargs['solid_joinstyle']
        self.pickradius = kwargs['pickradius']
        self.drawstyle = kwargs['drawstyle']
        self.markevery = kwargs['markevery']

        # Store kwargs for duplication function
        self._original_kwargs = dict(kwargs)

        # Construct Line2D object
        super().__init__(xdata, ydata, **kwargs)

    def __eq__(self, other):
        if isinstance(other, line):
            if(
                other.x_serial == self.x_serial and
                other.y_serial == self.y_serial and
                other.label == self.label and
                other.color == self.color and
                other.linewidth == self.linewidth and
                other.linestyle == self.linestyle and
                other.marker == self.marker and
                other.markersize == self.markersize and
                other.markeredgewidth == self.markeredgewidth and
                other.markeredgecolor == self.markeredgecolor and
                other.markerfacecolor == self.markerfacecolor and
                other.markerfacecoloralt == self.markerfacecoloralt and
                other.gapcolor == self.gapcolor and
                other.fillstyle == self.fillstyle and
                other.antialiased == self.antialiased and
                other.dash_capstyle == self.dash_capstyle and
                other.solid_capstyle == self.solid_capstyle and
                other.dash_joinstyle == self.dash_joinstyle and
                other.solid_joinstyle == self.solid_joinstyle and
                other.pickradius == self.pickradius and
                other.drawstyle == self.drawstyle and
                other.markevery == self.markevery
            ):
                return True
        return False

    def __str__(self):
        return f"Label: {self.label}, X_Serial: {self.x_serial}, Y_Serial: {self.y_serial}"
    
    def duplicate(self):
        return self.__class__(self.x_serial, self.y_serial, **self._original_kwargs)
    
    def line_to_dict(self):
        return {
            "x_serial": self.x_serial.serial_to_dict(),
            "y_serial": self.y_serial.serial_to_dict(),
            "color": self.color,
            "linewidth": self.linewidth,
            "linestyle": self.linestyle,
            "marker": self.marker,
            "markersize": self.markersize,
            "markeredgewidth": self.markeredgewidth,
            "markeredgecolor": self.markeredgecolor,
            "markerfacecolor": self.markerfacecolor,
            "markerfacecoloralt": self.markerfacecoloralt,
            "label": self.label,
            "gapcolor": self.gapcolor,
            "fillstyle": self.fillstyle,
            "antialiased": self.antialiased,
            "dash_capstyle": self.dash_capstyle,
            "solid_capstyle": self.solid_capstyle,
            "dash_joinstyle": self.dash_joinstyle,
            "solid_joinstyle": self.solid_joinstyle,
            "pickradius": self.pickradius,
            "drawstyle": self.drawstyle,
            "markevery": self.markevery
        }
    
    def line_from_dict(sub_data):
        x_serial = serial_variable.serial_from_dict(sub_data["x_serial"])
        y_serial = serial_variable.serial_from_dict(sub_data["y_serial"])
        return line(
            x_serial,
            y_serial,
            **{
                "color": sub_data["color"],
                "linewidth": sub_data["linewidth"],
                "linestyle": sub_data["linestyle"],
                "marker": sub_data["marker"],
                "markersize": sub_data["markersize"],
                "markeredgewidth": sub_data["markeredgewidth"],
                "markeredgecolor": sub_data["markeredgecolor"],
                "markerfacecolor": sub_data["markerfacecolor"],
                "markerfacecoloralt": sub_data["markerfacecoloralt"],
                "label": sub_data["label"],
                "gapcolor": sub_data["gapcolor"],
                "fillstyle": sub_data["fillstyle"],
                "antialiased": sub_data["antialiased"],
                "dash_capstyle": sub_data["dash_capstyle"],
                "solid_capstyle": sub_data["solid_capstyle"],
                "dash_joinstyle": sub_data["dash_joinstyle"],
                "solid_joinstyle": sub_data["solid_joinstyle"],
                "pickradius": sub_data["pickradius"],
                "drawstyle": sub_data["drawstyle"],
                "markevery": sub_data["markevery"]
            }
        )
    
class add_basic_line(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Basic Line")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap("Resources/serial_port_icon_blue.ico"))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        x_pass = serial_variable(0, "", "", [])
        y_pass = serial_variable(0, "", "", [])
        line_obj = line(x_pass, y_pass)

        serial_names = [serial_var.variable_name for serial_var in config.serial_variables]

        self.label1 = ctk.CTkLabel(self, text="X-Value Serial Variable:")
        self.label1.grid(row=0, column=0)

        x_serial_name = ctk.StringVar(value=serial_names[0])
        self.entry1 = ctk.CTkOptionMenu(self, variable=x_serial_name, values=serial_names, command=lambda value: self.add_serial_to_line("x", value, line_obj, config))
        self.entry1.grid(row=0, column=1)

        self.label2 = ctk.CTkLabel(self, text="Y-Value Serial Variable:")
        self.label2.grid(row=1, column=0)

        y_serial_name = ctk.StringVar(value=serial_names[0])
        self.entry2 = ctk.CTkOptionMenu(self, variable=y_serial_name, values=serial_names, command=lambda value: self.add_serial_to_line("y", value, line_obj, config))
        self.entry2.grid(row=1, column=1)

        self.label3 = ctk.CTkLabel(self, text="Line Label:")
        self.label3.grid(row=2, column=0)

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter label here...", width=240)
        self.entry3.grid(row=2, column=1)
        self.entry3.bind("<Return>", lambda event: self.add_label_to_line(line_obj, config))

        self.label4 = ctk.CTkLabel(self, text="Line Color (optional):")
        self.label4.grid(row=3, column=0)

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter color or hex code here...", width=240)
        self.entry4.grid(row=3, column=1)
        self.entry4.bind("<Return>", lambda event: self.add_color_to_line(line_obj))

        self.button1 = ctk.CTkButton(self, text="Add Another Line", command=lambda: self.add_another_line(line_obj, config))
        self.button1.grid(row=4, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Lines", command=lambda: self.add_line_to_config(line_obj, config))
        self.button2.grid(row=4, column=1)

    def add_serial_to_line(self, axis: Literal["x", "y"], serial_name, line_obj, config, event=None):
        for serial in config.serial_variables:
            if serial_name == serial.variable_name:
                serial_var = serial
        if axis == "x":
            line_obj.x_serial = serial_var
        elif axis == "y":
            line_obj.y_serial = serial_var

    def add_label_to_line(self, line_obj, config, event=None):
        label = self.entry3.get()
        valid_label = True
        for char in label:
            if char == "\\":
                valid_label = False
        for line_var in config.lines:
            if label == line_var.label:
                valid_label = False
        if valid_label:
            line_obj.label = label
            self.entry4.focus_set()
        else:
            error_message = "The label \"{label}\" is invalid or already exists."
            error_title = "Invalid Line Label"
            open_line_label_warning(error_message, error_title, label)

    def add_color_to_line(self, line_obj, event=None):
        color = self.entry4.get().lower()
        if color in colors:
            line_obj.color = color
        elif color_codes.is_hex_color(color):
            line_obj.color = color
        else:
            error_message = "The color code \"{color}\" is invalid."
            error_title = "Invalid Line Color"
            open_line_color_warning(error_message, error_title, color)

    def add_line_to_config(self, line_obj, config, event=None):
        if line_obj.x_serial == serial_variable(0, "", "", []):
            line_obj.x_serial = config.serial_variables[0]
        if line_obj.y_serial == serial_variable(0, "", "", []):
            line_obj.y_serial = config.serial_variables[0]
        config.lines.append(line_obj)
        self.destroy()

    def add_another_line(self, line_obj, config, event=None):
        self.add_line_to_config(line_obj, config)
        new_add_line_window = add_basic_line(config)
        new_add_line_window.mainloop()

class edit_basic_line_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Lines")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap("Resources/serial_port_icon_blue.ico"))
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
                line_obj.label,
                line_obj.x_serial.variable_name,
                line_obj.y_serial.variable_name,
                line_obj.color
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
        self.title(f"Live Serial Reader - Edit Line \"{line_obj.label}\"")
        self.geometry("435x200")
        self.resizable(True, True)
        self.after(250, lambda: self.iconbitmap("Resources/serial_port_icon_blue.ico"))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        line_ID = config.lines.index(line_obj)

        serial_names = [serial_var.variable_name for serial_var in config.serial_variables]

        self.label1 = ctk.CTkLabel(self, text="X-Value Serial Variable:")
        self.label1.grid(row=0, column=0)

        x_index = serial_names.index(line_obj.x_serial.variable_name)

        x_serial_name = ctk.StringVar(value=serial_names[x_index])
        self.entry1 = ctk.CTkOptionMenu(self, variable=x_serial_name, values=serial_names, command=lambda value: self.edit_serial_to_line("x", value, line_obj, config))
        self.entry1.grid(row=0, column=1)

        self.label2 = ctk.CTkLabel(self, text="Y-Value Serial Variable:")
        self.label2.grid(row=1, column=0)

        y_index = serial_names.index(line_obj.y_serial.variable_name)

        y_serial_name = ctk.StringVar(value=serial_names[y_index])
        self.entry2 = ctk.CTkOptionMenu(self, variable=y_serial_name, values=serial_names, command=lambda value: self.edit_serial_to_line("y", value, line_obj, config))
        self.entry2.grid(row=1, column=1)

        self.label3 = ctk.CTkLabel(self, text="Line Label:")
        self.label3.grid(row=2, column=0)

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter label here...", width=240)
        self.entry3.grid(row=2, column=1)
        self.entry3.bind("<Return>", lambda event: self.edit_label_to_line(line_obj, config))

        self.label4 = ctk.CTkLabel(self, text="Line Color (optional):")
        self.label4.grid(row=3, column=0)

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter color or hex code here...", width=240)
        self.entry4.grid(row=3, column=1)
        self.entry4.bind("<Return>", lambda event: self.edit_color_to_line(line_obj))
    
        self.button1 = ctk.CTkButton(self, text="Edit Another Line", command=lambda: self.edit_another_line(line_obj, config))
        self.button1.grid(row=4, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editiing Lines", command=lambda: self.edit_line_to_config(line_obj, config, line_ID))
        self.button2.grid(row=4, column=1)

    def edit_serial_to_line(self, axis: Literal["x", "y"], serial_name, line_obj, config, event=None):
        for serial in config.serial_variables:
            if serial_name == serial.variable_name:
                serial_var = serial
        if axis == "x":
            line_obj.x_serial = serial_var
        elif axis == "y":
            line_obj.y_serial = serial_var

    def edit_label_to_line(self, line_obj, config, event=None):
        label = self.entry3.get()
        valid_label = True
        for char in label:
            if char == "\\":
                valid_label = False
        for line_var in config.lines:
            if label == line_var.label:
                valid_label = False
        if valid_label:
            line_obj.label = label
        else:
            error_message = "The label \"{label}\" is invalid or already exists."
            error_title = "Invalid Line Label"
            open_line_label_warning(error_message, error_title, label)

    def edit_color_to_line(self, line_obj, event=None):
        color = self.entry4.get().lower()
        if color in colors:
            line_obj.color = color
        elif color_codes.is_hex_color(color):
            line_obj.color = color
        else:
            error_message = "The color code \"{color}\" is invalid."
            error_title = "Invalid Line Color"
            open_line_color_warning(error_message, error_title, color)

    def edit_line_to_config(self, line_obj, config, line_ID, event=None):
        self.edit_line_to_plots(line_obj, config, line_ID)
        config.lines[line_ID] = line_obj
        self.destroy()

    def edit_another_line(self, line_obj, config, line_ID, event=None):
        self.edit_line_to_config(line_obj, config, line_ID)
        new_edit_line_window = edit_basic_line_list(config)
        new_edit_line_window.mainloop()

    def edit_line_to_plots(self, line_obj, config, line_ID):
        old_line = config.lines[line_ID]

        new_units = True
        if old_line.x_serial.variable_units == line_obj.x_serial.variable_units and old_line.y_serial.variable_units == line_obj.y_serial.variable_units:
            new_units = False

        for plot_obj in config.plots:
            if old_line in plot_obj.lines and not new_units:
                config.plots[config.plots.index(plot_obj)].lines[plot_obj.lines.index(old_line)] = line_obj
            elif old_line in plot_obj.lines and new_units and len(plot_obj.lines) == 1:
                config.plots[config.plots.index(plot_obj)].lines[plot_obj.lines.index(old_line)] = line_obj
            elif old_line in plot_obj.lines and new_units and len(plot_obj.lines) > 1:
                config.plots[config.plots.index(plot_obj)].lines.remove(old_line)

class delete_lines(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Delete Lines")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap("Resources/serial_port_icon_blue.ico"))
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

        self.serial_vars = config.serial_variables

        self.populate_delete_list(config)

        self.lift()

    def populate_delete_list(self, config):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        label_font = ctk.CTkFont(family="Helvetica", size=12)
        
        for row_idx, line_obj in enumerate(config.lines):
            parameters = [
                line_obj.label,
                line_obj.x_serial.variable_name,
                line_obj.y_serial.variable_name,
                line_obj.color
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, line_var=line_obj: self.delete_line(line_var, config))
                    label.configure(cursor="hand2")
        
    def delete_line(self, line_obj, config):
        for line_var in config.lines:
            if line_obj == line_var:
                config.lines.remove(line_var)
                for plot_obj in config.plots:
                    if line_obj in plot_obj.lines:
                        config.plots[config.plots.index(plot_obj)].lines = [
                            L for L in config.plots[config.plots.index(plot_obj)].lines if L != line_obj
                        ]
            self.populate_delete_list(config)

def open_line_label_warning(error_message, error_title, label):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, label=label)
    error_win.mainloop()

def open_line_color_warning(error_message, error_title, color):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, color=color)
    error_win.mainloop()