import ctypes
import customtkinter as ctk
from typing import Literal
from lines import line
from resource_manager import icon_path
from input_check import name_check, int_check, label_check

# def check_numeric_legend_pos(position_tuple: str):
#     position_tuple.strip().strip("()").split(",")
#     if len(position_tuple) == 2:
#         position_tuple[0] = position_tuple[0].strip()
#         position_tuple[1] = position_tuple[1].strip()
#         if not position_tuple[0].startswith("-", "+") and position_tuple[0].isdecimal():
#             position_tuple[0] = float(position_tuple[0])
#         if not position_tuple[1].startswith("-", "+") and position_tuple[1].isdecimal():
#             position_tuple[1] = float(position_tuple[1])
#         if position_tuple[0] <= 1 and position_tuple[0] >= 0 and position_tuple[1] <= 1 and position_tuple[1] >= 0:
#             return f"({str(position_tuple[0])}, {str(position_tuple[1])})"
#     else:
#         return False

global legend_positions
legend_positions = ["best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"]

class plot:
    def __init__(self, lines: list, plot_title: str, x_label: str, y_label: str, legend_position: str, plot_position: list[int, int]):
        self.lines = lines
        self.plot_title = plot_title
        self.x_label = x_label
        self.y_label = y_label
        self.legend_position = legend_position
        self.plot_position = plot_position

    def __eq__(self, other):
        if isinstance(other, plot):
            if(
                all(next((True for other_line_obj in self.lines if other_line_obj == line_obj), False) for line_obj in self.lines) and 
                len(other.lines) == len(self.lines) and
                other.plot_title == self.plot_title and
                other.x_label == self.x_label and
                other.y_label == self.y_label and
                other.legend_position == self.legend_position and
                other.plot_position == self.plot_position
            ):
                return True
        return False

    def __hash__(self):
        hash_list = [line_obj for line_obj in self.lines]
        plot_position_tuple = tuple(self.plot_position)
        hash_list += [self.plot_title, self.x_label, self.y_label, self.legend_position, plot_position_tuple]
        hash_tuple = tuple(hash_list)
        return hash(hash_tuple)

    def plot_to_dict(self):
        # Snippet to convert line objects to JSON format
        converted_lines = []
        for line_obj in self.lines:
            converted_line = line_obj.line_to_dict()
            converted_lines.append(converted_line)

        return {
            "lines": converted_lines,
            "title": self.plot_title,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "legend pos": self.legend_position,
            "plot pos": self.plot_position
        }

    def plot_from_dict(json_plot, lines=None):
        # Snippet to convert JSON format into line objects
        plot_lines = []

        if lines is not None:
            for plot_line in json_plot["lines"]:
                plot_line = next((line_obj for line_obj in lines if line_obj == line.line_from_dict(plot_line)))
                plot_lines.append(plot_line)
        else:
            plot_lines = [line.line_from_dict(plot_line) for plot_line in json_plot["lines"]]

        return plot(plot_lines, json_plot["title"], json_plot["x_label"], json_plot["y_label"], json_plot["legend pos"], json_plot["plot pos"])

    def update_plot(self, new_plot_title: str, new_x_label: str, new_y_label: str, new_legend_position: str, new_plot_position: list[int,int]):
        self.plot_title = new_plot_title
        self.x_label = new_x_label
        self.y_label = new_y_label
        self.legend_position = new_legend_position
        self.plot_position = new_plot_position

    def get_plot_units(self):
        x_units = ''
        y_units = ''
        if not self.lines:
            return x_units, y_units
        for line_obj in self.lines:
            if not line_obj.x_serial.variable_units.strip():
                x_units = ''
                y_units = ''
                return x_units, y_units
            elif not x_units:
                x_units = line_obj.x_serial.variable_units.strip()
            elif x_units == line_obj.x_serial.variable_units.strip():
                continue
            else:
                x_units = ''
                y_units = ''
                return x_units, y_units
            if not line_obj.y_serial.variable_units.strip():
                x_units = ''
                y_units = ''
                return x_units, y_units
            elif not y_units:
                y_units = line_obj.y_serial.variable_units.strip()
            elif y_units == line_obj.y_serial.variable_units.strip():
                continue
            else:
                x_units = ''
                y_units = ''
                return x_units, y_units
        return x_units, y_units
    
    def remove_incompatible_lines(self):
        x_units = ''
        y_units = ''
        if not self.lines:
            return
        for line_obj in self.lines:
            remove_line = False
            if not line_obj.x_serial.variable_units.strip():
                remove_line = True
            elif not x_units:
                x_units = line_obj.x_serial.variable_units.strip()
            elif line_obj.x_serial.variable_units.strip() != x_units:
                remove_line = True
            if not line_obj.y_serial.variable_units.strip():
                remove_line = True
            elif not y_units:
                y_units = line_obj.y_serial.variable_units.strip()
            elif line_obj.y_serial.variable_units.strip() != y_units:
                remove_line = True
            if remove_line:
                # print(f"Incompatible line detected! Plot (x,y) units: {x_units, y_units}")
                self.lines.remove(line_obj)
        return
        
class add_plots(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Add Plot")
        self.geometry("435x300")
        self.resizable(True, True)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        if not len(config.lines):
            error_message = "Add lines first in order to create a plot!"
            error_title = "No Lines Exist"
            error_function(error_message, error_title)
            self.destroy()

        self.config = config
        self.lines = []
        self.plot_title = ""
        self.x_label = ""
        self.y_label = ""
        self.legend_position = ""
        self.plot_position = (0, 0)

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter plot title...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.change_focus(2, event))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter x-axis label...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.change_focus(3, event))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter y-axis label...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.change_focus(4, event))

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter legend position...", width=240)
        self.entry4.grid(row=3, column=0)
        self.entry4.bind("<Return>", lambda event: self.change_focus(5, event))

        self.entry5 = ctk.CTkEntry(self, placeholder_text="Enter plot position as (x, y)...", width=240)
        self.entry5.grid(row=4, column=0)

        self.lines_frame = ctk.CTkScrollableFrame(self, height=75, width=250)
        self.lines_frame._scrollbar.configure(height=0)
        self.lines_frame.grid(row=5, column=0, sticky='nsew', padx=15)

        self.button1 = ctk.CTkButton(self, text="Add Another Plot", command=self.add_another_plot)
        self.button1.grid(row=6, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Plots", command=self.add_plot_to_config)
        self.button2.grid(row=7, column=0)

        self.line_checkboxes = []
        for line_obj in config.lines:
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.lines_frame, text=f"Label: {line_obj.get_label()}, X-Var: {line_obj.x_serial.variable_name} ({line_obj.x_serial.variable_units}), Y-Var: {line_obj.y_serial.variable_name} ({line_obj.y_serial.variable_units})", variable=var, onvalue=1, offvalue=0)
            checkbox.pack(anchor='w')
            self.line_checkboxes.append([var, line_obj])

    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 2:
            self.entry2.focus_set()
        elif entry_box_num == 3:
            self.entry3.focus_set()
        elif entry_box_num == 4:
            self.entry4.focus_set()
        elif entry_box_num == 5:
            self.entry5.focus_set()

    def add_plot_title(self):
        plot_title = self.entry1.get().strip()
        valid_title = name_check(plot_title)
        if valid_title:
            self.plot_title = plot_title
            return True
        else:
            error_message = f'The plot title "{plot_title}" is invalid or already exists!'
            error_title = "Invalid Plot Title"
            error_function(error_message, error_title, plot_title=plot_title)
            return False

    def add_axis_label(self, axis: Literal["x", "y"]):
        if axis == "x":
            axis_label = self.entry2.get().strip()
            valid_axis = name_check(axis_label)
            if valid_axis:
                self.x_label = axis_label
                return True
        elif axis == "y":
            axis_label = self.entry3.get().strip()
            valid_axis = name_check(axis_label)
            if valid_axis:
                self.y_label = axis_label
            return True
        else:
            error_message = f"Axis-{axis} label is blank or invalid!"
            error_title = "Invalid Axis Label"
            error_function(error_message, error_title, axis=axis)
            return False

    def add_legend_position(self):
        legend_pos = self.entry4.get().strip().lower()
        if legend_pos in legend_positions:
            self.legend_position = legend_pos
            return True
        else:
            error_message = f'The legend position "{legend_pos}" is invalid!'
            error_title = "Invalid Legend Position"
            error_function(error_message, error_title, legend_pos=legend_pos)
            return False

    def get_selected_lines(self):
        valid_lines = True
        selected_lines = [self.line_checkboxes[i][1] for i, var in enumerate(self.line_checkboxes) if var[0].get()]
        x_unit = ""
        y_unit = ""
        for line_obj in selected_lines:
            if not x_unit and not y_unit and line_obj.x_serial.variable_units and line_obj.y_serial.variable_units:
                x_unit = line_obj.x_serial.variable_units
                y_unit = line_obj.y_serial.variable_units
            elif x_unit != line_obj.x_serial.variable_units or y_unit != line_obj.y_serial.variable_units:
                valid_lines = False
        if not valid_lines:
            error_message = "The selected lines have mismatching x or y units!"
            error_title = "Mismatched Plot Units"
            error_function(error_message, error_title)
            return False
        else:
            self.lines = selected_lines
            return True
        
    def add_plot_position(self):
        plot_pos = self.entry5.get().strip()
        valid_pos = True
        if plot_pos and plot_pos[0] == '(' and plot_pos[-1] == ')':
            plot_pos = [num.strip() for num in plot_pos[1:-1].split(",")]
        else:
            valid_pos = False
        for num in plot_pos:
            if int_check(num):
                plot_pos[plot_pos.index(num)] = int(num)
            else:
                valid_pos = False
        if valid_pos and len(plot_pos) != 2:
            valid_pos = False

        if valid_pos:
            for plot_obj in self.config.plots:
                if plot_pos == plot_obj.plot_position:
                    valid_pos = False

        max_plot_pos = calculate_valid_plot_positions(self.config, True)

        if valid_pos and plot_pos[0] > max_plot_pos[0]:
            valid_pos = False
        elif valid_pos and plot_pos[1] > max_plot_pos[1]:
            valid_pos = False

        if valid_pos:
            self.plot_position = plot_pos
            return True
        else:
            error_message = "Invalid plot position!"
            error_title = "Invalid Plot Position"
            error_function(error_message, error_title)
            return False

    def add_plot_to_config(self, event=None):
        valid_units = self.get_selected_lines()
        if valid_units and self.add_plot_title() and self.add_axis_label("x") and self.add_axis_label("y") and self.add_legend_position() and self.add_plot_position():
            new_plot_obj = plot(self.lines, self.plot_title, self.x_label, self.y_label, self.legend_position, self.plot_position)
            self.config.plots.append(new_plot_obj)
            self.destroy()
            return True
        return False

    def add_another_plot(self, event=None):
        if self.add_plot_to_config():
            new_add_plot_win = add_plots(self.config)
            new_add_plot_win.mainloop()        

class edit_plots_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Plots")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.lift()

        headers = ["Plot Title", "X-Label", "Y-Label", "Position"]
        header_font = ctk.CTkFont(family="Helvetica", size=12, weight="bold")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky='ew', padx=10)

        for i in range(len(headers)):
            self.header_frame.grid_columnconfigure(i, weight=1)

        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.header_frame, text=header, font=header_font)
            label.grid(row=0, column=col, sticky="ew", padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="gray")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        self.plot_objs = config.plots
        self.populate_plot_list(config)

    def populate_plot_list(self, config):
        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, plot_obj in enumerate(config.plots):
            parameters = [
                plot_obj.plot_title,
                plot_obj.x_label,
                plot_obj.y_label,
                f"({plot_obj.plot_position[0]}, {plot_obj.plot_position[1]})"
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, plot_var=plot_obj: self.edit_plot(plot_var, config))
                    label.configure(cursor="hand2")

    def edit_plot(self, plot_obj, config):
        self.destroy()
        edit_win = edit_plot(plot_obj, config)
        edit_win.mainloop()

class edit_plot(ctk.CTkToplevel):
    def __init__(self, plot_obj: plot, config):
        super().__init__()
        self.title("Live Serial Reader - Edit Plot")
        self.geometry("435x300")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        if not len(config.lines):
            error_message = "Add lines first in order to edit plots!"
            error_title = "No Lines Exist"
            error_function(error_message, error_title)
            self.destroy()

        self.config = config
        self.plot_obj = plot_obj
        self.lines = plot_obj.lines
        self.plot_title = plot_obj.plot_title
        self.x_label = plot_obj.x_label
        self.y_label = plot_obj.y_label
        self.legend_position = plot_obj.legend_position
        self.plot_position = plot_obj.plot_position
        self.plot_x_units, self.plot_y_units = plot_obj.get_plot_units()

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter plot title...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.change_focus(2, event))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter x-axis label...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.change_focus(3, event))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter y-axis label...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.change_focus(4, event))

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter legend position...", width=240)
        self.entry4.grid(row=3, column=0)
        self.entry4.bind("<Return>", lambda event: self.change_focus(5, event))

        self.entry5 = ctk.CTkEntry(self, placeholder_text="Enter plot position as (x, y)...", width=240)
        self.entry5.grid(row=4, column=0)

        self.lines_frame = ctk.CTkScrollableFrame(self, height=75, width=250)
        self.lines_frame._scrollbar.configure(height=0)
        self.lines_frame.grid(row=5, column=0, sticky='nsew', padx=15)

        self.button1 = ctk.CTkButton(self, text="Edit Another Plot", command=self.edit_another_plot)
        self.button1.grid(row=6, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editing Plots", command=self.edit_plot_to_config)
        self.button2.grid(row=7, column=0)

        self.line_checkboxes = []
        for line_obj in config.lines:
            if line_obj in plot_obj.lines:
                var = ctk.BooleanVar(value=True)
            else:
                var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.lines_frame, text=f"Label: {line_obj.get_label()}, X-Var: {line_obj.x_serial.variable_name} ({line_obj.x_serial.variable_units}), Y-Var: {line_obj.y_serial.variable_name} ({line_obj.y_serial.variable_units})", variable=var, onvalue=1, offvalue=0)
            checkbox.pack(anchor='w')
            self.line_checkboxes.append([var, line_obj])

    def change_focus(self, entry_box_num: int, event):
        if entry_box_num == 2:
            self.entry2.focus_set()
        elif entry_box_num == 3:
            self.entry3.focus_set()
        elif entry_box_num == 4:
            self.entry4.focus_set()
        elif entry_box_num == 5:
            self.entry5.focus_set()

    def edit_plot_title(self):
        plot_title = self.entry1.get().strip()
        valid_title = name_check(plot_title)
        if valid_title:
            self.plot_title = plot_title
            return True
        elif plot_title == "":
            return True
        else:
            error_message = f'The plot title "{plot_title}" is invalid or already exists!'
            error_title = "Invalid Plot Title"
            error_function(error_message, error_title, plot_title=plot_title)
            return False

    def edit_axis_label(self, axis: Literal["x", "y"]):
        if axis == "x":
            axis_label = self.entry2.get().strip()
            valid_axis = name_check(axis_label)
            if valid_axis:
                self.x_label = axis_label
                return True
            elif axis_label == "":
                return True
        elif axis == "y":
            axis_label = self.entry3.get().strip()
            valid_axis = name_check(axis_label)
            if valid_axis:
                self.y_label = axis_label
                return True
            elif axis_label == "":
                return True
        else:
            error_message = "The axis label entered is invalid!"
            error_title = "Invalid Plot Axis Label"
            error_function(error_message, error_title)
            return False

    def edit_legend_position(self):
        legend_position = self.entry4.get().strip()
        if legend_position in legend_positions:
            self.legend_position = legend_position
            return True
        elif legend_position == "":
            return True
        else:
            error_message = f'The legend position "{legend_position}" is invalid!'
            error_title = "Invalid Legend Position"
            error_function(error_message, error_title, legend_position=legend_position)
            return False

    def get_selected_lines(self):
        selected_lines = [self.line_checkboxes[i][1] for i, var in enumerate(self.line_checkboxes) if var[0].get()]
        valid_lines = True
        if any(line_obj in selected_lines for line_obj in self.plot_obj.lines):
            x_unit = self.plot_x_units
            y_unit = self.plot_y_units
        else:
            x_unit = selected_lines[0].x_serial.variable_units
            y_unit = selected_lines[0].y_serial.variable_units

        for line_obj in selected_lines:
            if line_obj.x_serial.variable_units != x_unit or line_obj.y_serial.variable_units != y_unit:
                valid_lines = False
        if not valid_lines:
            error_message = "The selected lines have mismatching x or y units!"
            error_title = "Mismatched Plot Units"
            error_function(error_message, error_title)
            return False
        else:
            self.lines = selected_lines
            return True
        
    def edit_plot_position(self):
        plot_pos = self.entry5.get().strip()
        valid_pos = True

        if plot_pos and plot_pos[0] == '(' and plot_pos[-1] == ')':
            plot_pos = [num.strip() for num in plot_pos[1:-1].split(",")]
        else:
            valid_pos = False
        for num in plot_pos:
            if int_check(num):
                plot_pos[plot_pos.index(num)] = int(num)
            else:
                valid_pos = False
        if valid_pos and len(plot_pos) != 2:
            valid_pos = False

        max_plot_pos = calculate_valid_plot_positions(self.config, False)

        if valid_pos and plot_pos[0] > max_plot_pos[0]:
            valid_pos = False
        elif valid_pos and plot_pos[1] > max_plot_pos[1]:
            valid_pos = False

        for plot_var in self.config.plots:
            if valid_pos and plot_pos == plot_var.plot_position:
                plot_var.plot_position = self.plot_position
        if valid_pos:
            self.plot_position = plot_pos
            return True
        else:
            error_message = "Invalid plot position!"
            error_title = "Invalid Plot Position"
            error_function(error_message, error_title)
            return False

    def edit_plot_to_config(self, event=None):
        valid_units = self.get_selected_lines()
        if valid_units and self.edit_plot_title() and self.edit_axis_label("x") and self.edit_axis_label("y") and self.edit_legend_position():
            if self.edit_plot_position:     
                self.plot_obj.lines = self.lines
                self.plot_obj.plot_title = self.plot_title
                self.plot_obj.x_label = self.x_label
                self.plot_obj.y_label = self.y_label
                self.plot_obj.legend_position = self.legend_position
                self.plot_obj.plot_position = self.plot_position
                self.destroy()
                return True
        return False
    
    def edit_another_plot(self, event=None):
        if self.edit_plot_to_config():
            new_edit_plot_win = edit_plots_list(self.config)
            new_edit_plot_win.mainloop()

class delete_plot_list(ctk.CTkToplevel):
    def __init__(self, config):
        super().__init__()
        self.title("Live Serial Reader - Delete Plots")
        self.geometry("435x200")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(self.iconbitmap(icon_path)))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        headers = ["Plot Title", "Number of Lines", "Plot Position"]
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

        self.populate_delete_list(config)

        self.lift()

    def populate_delete_list(self, config):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        label_font = ctk.CTkFont(family="Helvetica", size=12)

        for row_idx, plot_obj in enumerate(config.plots):
            parameters = [
                plot_obj.plot_title,
                str(len(plot_obj.lines)),
                f"({plot_obj.plot_position[0]}, {plot_obj.plot_position[1]})"
            ]

            for col, parameter in enumerate(parameters):
                if parameter != parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                elif parameter == parameters[0]:
                    label = ctk.CTkLabel(self.scroll_frame, text=parameter, font=label_font)
                    label.grid(row=row_idx * 2, column=col, sticky="ew", padx=5)
                    label.bind("<Button-1>", lambda event, plot_var=plot_obj: self.delete_plot(plot_var, config))
                    label.configure(cursor="hand2")

    def delete_plot(self, plot_obj, config):
        for plot_var in config.plots:
            if plot_obj == plot_var:
                config.plots.remove(plot_var)
        max_plot_pos = calculate_valid_plot_positions(config, False)
        p = 0
        for x in range(0, max_plot_pos[0] + 1):
            if p >= len(config.plots):
                break
            for y in range(0, max_plot_pos[1] + 1):
                if p >= len(config.plots):
                    break
                else:
                    config.plots[p].plot_position = (x, y)
                    p += 1
        self.populate_delete_list(config)

def is_square(x):
    if x >= 0:
        sr = int(x ** 0.5)
        return (sr * sr == x)
    return False

def calculate_valid_plot_positions(config, new_plot: bool):
        if new_plot:
            total_plots = len(config.plots) + 1
            best_pair = 0
        elif not new_plot:
            total_plots = len(config.plots)
            best_pair = 0

        # Checks if total plots is odd number and not square
        if total_plots % 2 != 0 and not is_square(total_plots):
            total_plots += 1
        # Checks if total plots is odd number and square
        elif total_plots % 2 != 0 and is_square(total_plots):
            best_pair = (total_plots ** 0.5, total_plots ** 0.5)
            max_matrix_xy = (int(best_pair[0]-1), int(best_pair[1]-1))
            return max_matrix_xy

        best_pair = (total_plots, 1)
        min_sum = total_plots + 1
        for i in range(1, int(total_plots ** 0.5) + 1):
            if total_plots % i == 0:
                j = total_plots // i
                if i + j < min_sum:
                    min_sum = i + j
                    best_pair = (j, i)
        max_matrix_xy = (int(best_pair[0]-1), int(best_pair[1]-1))
        return max_matrix_xy

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, **kwargs)
    error_win.mainloop()