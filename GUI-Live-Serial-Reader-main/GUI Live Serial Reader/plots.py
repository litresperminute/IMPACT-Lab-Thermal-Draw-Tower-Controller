import customtkinter as ctk
from typing import Literal
from lines import line
from file_manager import icon_path

global plots
plots = []

global legend_positions
legend_positions = ["best", "upper right", "upper left", "lower left", "lower right", "right", "center left", "center right", "lower center", "upper center", "center"]

class plot:
    def __init__(self, lines: list, plot_title: str, x_label: str, y_label: str, legend_position: str, plot_position: tuple[int, int]):
        self.lines = lines
        self.plot_title = plot_title
        self.x_label = x_label
        self.y_label = y_label
        self.legend_position = legend_position
        self.plot_position = plot_position
        plots.append(self)

    def __eq__(self, other):
        if isinstance(other, plot):
            if(
                other.lines == self.lines and
                other.plot_title == self.plot_title and
                other.x_label == self.x_label and
                other.y_label == self.y_label and
                other.legend_position == self.legend_position and
                other.plot_position == self.plot_position
            ):
                return True
        return False

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

    def plot_from_dict(sub_data):
        # Snippet to convert JSON format into line objects
        line_data = sub_data["lines"]
        lines = []
        for line_var in line_data:
            line_obj = line.line_from_dict(line_var)
            lines.append(line_obj)

        return plot(lines, sub_data["title"], sub_data["x_label"], sub_data["y_label"], sub_data["legend pos"], sub_data["plot pos"])

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
            error_message = "Add lines first in order to create a plot."
            error_title = "No Lines Exist"
            line_error(error_message, error_title)
            self.destroy()

        plot_obj = plot([], "", "", "", "", (0,0))

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter plot title...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.add_plot_title(plot_obj, config))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter x-axis label...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.add_axis_label(plot_obj, "x"))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter y-axis label...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.add_axis_label(plot_obj, "y"))

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter legend position...", width=240)
        self.entry4.grid(row=3, column=0)
        self.entry4.bind("<Return>", lambda event: self.add_legend_position(plot_obj))

        self.entry5 = ctk.CTkEntry(self, placeholder_text="Enter plot position as (x, y)...", width=240)
        self.entry5.grid(row=4, column=0)
        self.entry5.bind("<Return>", lambda event: self.add_plot_position(plot_obj, config))

        self.lines_frame = ctk.CTkScrollableFrame(self, height=75, width=250)
        self.lines_frame._scrollbar.configure(height=0)
        self.lines_frame.grid(row=5, column=0, sticky='nsew', padx=15)

        self.button1 = ctk.CTkButton(self, text="Add Another Plot", command=lambda: self.add_another_plot(plot_obj, config))
        self.button1.grid(row=6, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Adding Plots", command=lambda: self.add_plot_to_config(plot_obj, config))
        self.button2.grid(row=7, column=0)

        self.line_checkboxes = []
        for line_obj in config.lines:
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.lines_frame, text=f"Label: {line_obj.label}, X-Var: {line_obj.x_serial.variable_name} ({line_obj.x_serial.variable_units}), Y-Var: {line_obj.y_serial.variable_name} ({line_obj.y_serial.variable_units})", variable=var, onvalue=1, offvalue=0)
            checkbox.pack(anchor='w')
            self.line_checkboxes.append([var, line_obj])

    def add_plot_title(self, plot_obj, config, event=None):
        plot_title = self.entry1.get().strip()
        valid_title = True

        if not plot_title:
            valid_title = False

        for plot_var in config.plots:
            if plot_var.plot_title == plot_title:
                valid_title = False

        if valid_title:
            plot_obj.plot_title = plot_title
            self.entry2.focus_set()
        else:
            error_message = "The plot title \"{plot_title}\" is invalid or already exists."
            error_title = "Invalid Plot Title"
            plot_error1(error_message, error_title, plot_title)

    def add_axis_label(self, plot_obj, axis: Literal["x", "y"], event=None):
        valid_axis = True
        if axis == "x":
            axis_label = self.entry2.get().strip()
            if not axis_label:
                valid_axis = False
            if valid_axis:
                plot_obj.x_label = axis_label
                self.entry3.focus_set()
            else:
                error_message = "Axis-{axis} label is blank!"
                error_title = "Invalid Axis Label"
                plot_error4(error_message, error_title, axis)
        elif axis == "y":
            axis_label = self.entry3.get().strip()
            if not axis_label:
                valid_axis = False
            if valid_axis:
                plot_obj.y_label = axis_label
                self.entry4.focus_set()
            else:
                error_message = "Axis-{axis} label is blank!"
                error_title = "Invalid Axis Label"
                plot_error4(error_message, error_title, axis)

    def add_legend_position(self, plot_obj, event=None):
        legend_pos = self.entry4.get().strip()
        if legend_pos in legend_positions:
            plot_obj.legend_position = legend_pos
            self.entry5.focus_set()
        else:
            error_message = "The legend position \"{legend_pos}\" is invalid."
            error_title = "Invalid Legend Position"
            plot_error2(error_message, error_title, legend_pos)

    def get_selected_lines(self, plot_obj):
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
            plot_error3(error_message, error_title)
            return False
        else:
            plot_obj.lines = selected_lines
            return plot_obj
        
    def add_plot_position(self, plot_obj, config, event=None):
        plot_pos = self.entry5.get().strip()
        valid_pos = True
        if plot_pos and plot_pos[0] == '(' and plot_pos[-1] == ')':
            plot_pos = [num.strip() for num in plot_pos[1:-1].split(",")]
        else:
            valid_pos = False
        for num in plot_pos:
            if num.isdigit and num[0] != "-":
                plot_pos[plot_pos.index(num)] = int(num)
            else:
                valid_pos = False
        if valid_pos and len(plot_pos) != 2:
            valid_pos = False

        if valid_pos:
            for config_plot in config.plots:
                if plot_pos == config_plot.plot_position:
                    valid_pos = False

        max_plot_pos = calculate_valid_plot_positions(config, True)

        if valid_pos and plot_pos[0] > max_plot_pos[0]:
            valid_pos = False
        elif valid_pos and plot_pos[1] > max_plot_pos[1]:
            valid_pos = False

        if valid_pos:
            plot_obj.plot_position = plot_pos
        else:
            error_message = "Invalid plot position!"
            error_title = "Invalid Plot Position"
            plot_error3(error_message, error_title)

    def add_plot_to_config(self, plot_obj, config, event=None):
        plot_obj = self.get_selected_lines(plot_obj)
        if plot_obj:
            config.plots.append(plot_obj)
            self.destroy()
            return True
        return False

    def add_another_plot(self, plot_obj, config, event=None):
        valid_plot = self.add_plot_to_config(plot_obj, config)
        if valid_plot:
            new_add_plot_win = add_plots(config)
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
    def __init__(self, plot_obj, config):
        super().__init__()
        self.title("Live Serial Reader - Edit Plot")
        self.geometry("435x300")
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(icon_path))
        self.grid_columnconfigure(0, weight=1)
        self.lift()

        if not len(config.lines):
            error_message = "Add lines first in order to edit plots."
            error_title = "No Lines Exist"
            line_error(error_message, error_title)
            self.destroy()

        self.plot_ID = config.plots.index(plot_obj)
        self.plot_x_units = plot_obj.lines[0].x_serial.variable_units
        self.plot_y_units = plot_obj.lines[0].y_serial.variable_units

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Enter plot title...", width=240)
        self.entry1.grid(row=0, column=0)
        self.entry1.bind("<Return>", lambda event: self.edit_plot_title(plot_obj, config))

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Enter x-axis label...", width=240)
        self.entry2.grid(row=1, column=0)
        self.entry2.bind("<Return>", lambda event: self.edit_axis_label(plot_obj, "x"))

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Enter y-axis label...", width=240)
        self.entry3.grid(row=2, column=0)
        self.entry3.bind("<Return>", lambda event: self.edit_axis_label(plot_obj, "y"))

        self.entry4 = ctk.CTkEntry(self, placeholder_text="Enter legend position...", width=240)
        self.entry4.grid(row=3, column=0)
        self.entry4.bind("<Return>", lambda event: self.edit_legend_position(plot_obj))

        self.entry5 = ctk.CTkEntry(self, placeholder_text="Enter plot position as (x, y)...", width=240)
        self.entry5.grid(row=4, column=0)
        self.entry5.bind("<Return>", lambda event: self.edit_plot_position(plot_obj, config))

        self.lines_frame = ctk.CTkScrollableFrame(self, height=75, width=250)
        self.lines_frame._scrollbar.configure(height=0)
        self.lines_frame.grid(row=5, column=0, sticky='nsew', padx=15)

        self.button1 = ctk.CTkButton(self, text="Edit Another Plot", command=lambda: self.edit_another_plot(plot_obj, config))
        self.button1.grid(row=6, column=0)

        self.button2 = ctk.CTkButton(self, text="Finish Editing Plots", command=lambda: self.edit_plot_to_config(plot_obj, config))
        self.button2.grid(row=7, column=0)

        self.line_checkboxes = []
        for line_obj in config.lines:
            if line_obj in plot_obj.lines:
                var = ctk.BooleanVar(value=True)
            else:
                var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.lines_frame, text=f"Label: {line_obj.label}, X-Var: {line_obj.x_serial.variable_name} ({line_obj.x_serial.variable_units}), Y-Var: {line_obj.y_serial.variable_name} ({line_obj.y_serial.variable_units})", variable=var, onvalue=1, offvalue=0)
            checkbox.pack(anchor='w')
            self.line_checkboxes.append([var, line_obj])

    def edit_plot_title(self, plot_obj, config, event=None):
        plot_title = self.entry1.get().strip()
        valid_title = True

        if not plot_title:
            valid_title = False

        for plot_var in config.plots:
            if plot_var.plot_title == plot_title or plot_title == "":
                valid_title = False
        if valid_title:
            plot_obj.plot_title = plot_title
            self.entry2.focus_set()
        else:
            error_message = "The plot title \"{plot_title}\" is invalid or already exists."
            error_title = "Invalid Plot Title"
            plot_error1(error_message, error_title, plot_title)

    def edit_axis_label(self, plot_obj, axis: Literal["x", "y"], event=None):
        valid_axis = True
        if axis == "x":
            axis_label = self.entry2.get().strip()
            if not axis_label:
                valid_axis = False
            if valid_axis:
                plot_obj.x_label = axis_label
                self.entry3.focus_set()
            else:
                error_message = "Axis-{axis} label is blank!"
                error_title = "Invalid Axis Label"
                plot_error4(error_message, error_title, axis)
        elif axis == "y":
            axis_label = self.entry3.get().strip()
            if not axis_label:
                valid_axis = False
            if valid_axis:
                plot_obj.y_label = axis_label
                self.entry4.focus_set()
            else:
                error_message = "Axis-{axis} label is blank!"
                error_title = "Invalid Axis Label"
                plot_error4(error_message, error_title, axis)

    def edit_legend_position(self, plot_obj, event=None):
        legend_pos = self.entry4.get().strip()
        if legend_pos in legend_positions:
            plot_obj.legend_position = legend_pos
        else:
            error_message = "The legend position \"{legend_pos}\" is invalid."
            error_title = "Invalid Legend Position"
            plot_error2(error_message, error_title, legend_pos)

    def get_selected_lines(self, plot_obj):
        selected_lines = [self.line_checkboxes[i][1] for i, var in enumerate(self.line_checkboxes) if var[0].get()]
        valid_lines = True
        if any(line_obj in selected_lines for line_obj in plot_obj.lines):
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
            plot_error3(error_message, error_title)
            return False
        else:
            plot_obj.lines = selected_lines
            return plot_obj
        
    def edit_plot_position(self, plot_obj, config, event=None):
        plot_pos = self.entry5.get().strip()
        valid_pos = True

        if plot_pos and plot_pos[0] == '(' and plot_pos[-1] == ')':
            plot_pos = [num.strip() for num in plot_pos[1:-1].split(",")]
        else:
            valid_pos = False
        for num in plot_pos:
            if num.isdigit and num[0] != "-":
                plot_pos[plot_pos.index(num)] = int(num)
            else:
                valid_pos = False
        if valid_pos and len(plot_pos) != 2:
            valid_pos = False

        max_plot_pos = calculate_valid_plot_positions(config, False)

        if valid_pos and plot_pos[0] > max_plot_pos[0]:
            valid_pos = False
        elif valid_pos and plot_pos[1] > max_plot_pos[1]:
            valid_pos = False

        for plot_var in config.plots:
            if valid_pos and plot_pos == plot_var.plot_position:
                config.plots[config.plots.index(plot_var)].plot_position = plot_obj.plot_position
                
        if valid_pos:
            plot_obj.plot_position = plot_pos
        else:
            error_message = "Invalid plot position!"
            error_title = "Invalid Plot Position"
            plot_error3(error_message, error_title)

    def edit_plot_to_config(self, plot_obj, config, event=None):
        plot_obj = self.get_selected_lines(plot_obj)
        if plot_obj:
            config.plots[self.plot_ID] = plot_obj
            self.destroy()
            return True
        return False
    
    def edit_another_plot(self, plot_obj, config, event=None):
        valid_plot = self.edit_plot_to_config(plot_obj, config)
        if valid_plot:
            new_edit_plot_win = edit_plot(config)
            new_edit_plot_win.mainloop()

def plot_error1(error_message, error_title, plot_title):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, plot_title=plot_title)
    error_win.mainloop()

def plot_error2(error_message, error_title, legend_pos):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, legend_pos=legend_pos)
    error_win.mainloop()

def plot_error3(error_message, error_title):
    from warning_window import error_window
    error_win = error_window(error_message, error_title)
    error_win.mainloop()

def plot_error4(error_message, error_title, axis):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, axis=axis)
    error_win.mainloop()

def line_error(error_message, error_title):
    from warning_window import error_window
    error_win = error_window(error_message, error_title)
    error_win.mainloop()

def is_square(x):
    if x >= 0:
        sr = int(x ** 0.5)
        return (sr * sr == x)
    return False

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