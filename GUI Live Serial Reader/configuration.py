import customtkinter as ctk
from serial_variables import serial_variable
from lines import line
from plots import plot

global configurations
configurations = []

class configuration:
    def __init__(self, configuration_name: str, serial_variables: list, plots: list, baud_rate: int, com_port: int, csv_file: str, lines: list):
        # Configuration Object Attributes
        self.configuration_name = configuration_name
        self.serial_variables = serial_variables
        self.plots = plots
        self.baud_rate = baud_rate
        self.com_port = com_port
        self.csv_file = csv_file
        self.lines = lines

        # Appends New Configuration Objects to the List
        configurations.append(self)

    def to_dict(self):
        """ Convert configuration object to dictionary """
        # Snippet to convert serial variable objects to JSON format
        converted_serials = []
        for serial_var in self.serial_variables:
            converted_serial = serial_var.serial_to_dict()
            converted_serials.append(converted_serial)

        # Snippet to convert line objects to JSON format
        converted_lines = []
        for line_obj in self.lines:
            converted_line = line_obj.line_to_dict()
            converted_lines.append(converted_line)

        # Snippet to convert plot objects to JSON format
        converted_plots = []
        for plot_obj in self.plots:
            converted_plot = plot_obj.plot_to_dict()
            converted_plots.append(converted_plot)

        return {
            "configuration_name": self.configuration_name,
            "serial_variables": converted_serials,
            "plots": converted_plots,
            "baud_rate": self.baud_rate,
            "com_port": self.com_port,
            "csv_file": self.csv_file,
            "lines": converted_lines
        }
    
    def from_dict(data):
        """ Create configuration object from dictionary """
        # Snippet to convert JSON format into serial variable objects
        converted_serials = data["serial_variables"]
        serial_objs = []
        for converted_serial in converted_serials:
            serial_obj = serial_variable.serial_from_dict(converted_serial)
            serial_objs.append(serial_obj)

        # Snippet to convert JSON format into line objects
        converted_lines = data["lines"]
        lines = []
        for converted_line in converted_lines:
            line_obj = line.line_from_dict(converted_line, serial_objs)
            lines.append(line_obj)

        # Snippet to convert JSON format into plot objects
        converted_plots = data["plots"]
        plots = []
        for converted_plot in converted_plots:
            plot_obj = plot.plot_from_dict(converted_plot, lines)
            plots.append(plot_obj)

        return configuration(data["configuration_name"], serial_objs, plots, data["baud_rate"], data["com_port"], data["csv_file"], lines)
    
    def double_check_lines(self):
        for line_obj in self.lines:
            if not line_obj.is_valid_line():
                self.lines.remove(line_obj)
                # print(f"A line has been removed from config!")

    def double_check_plots(self):
        for plot_obj in self.plots:
            plot_obj.remove_incompatible_lines()
            if not len(plot_obj.lines):
                self.plots.remove(plot_obj)
                # print(f"A plot has been removed from config!")

    def remove_lineless_plots(self):
        for plot_obj in self.plots:
            if not len(plot_obj.lines):
                self.plots.remove(plot_obj)