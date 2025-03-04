import customtkinter as ctk
from serial_variables import serial_variable
from lines import line

global configurations
configurations = []

class configuration:
    def __init__(self, configuration_name: str, serial_variables: list, plots: int, baud_rate: int, com_port: int, csv_file: str, lines: list):
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

        return {
            "configuration_name": self.configuration_name,
            "serial_variables": converted_serials,
            "plots": self.plots,
            "baud_rate": self.baud_rate,
            "com_port": self.com_port,
            "csv_file": self.csv_file,
            "lines": converted_lines
        }
    
    def from_dict(data):
        """ Create configuration object from dictionary """

        # Snippet to convert JSON format into serial variable objects
        serial_data = data["serial_variables"]
        serial_vars = []
        for serial_var in serial_data:
            serial_obj = serial_variable.serial_from_dict(serial_var)
            serial_vars.append(serial_obj)

        # Snippet to convert JSON format into line objects
        line_data = data["lines"]
        lines = []
        for line_var in line_data:
            line_obj = line.line_from_dict(line_var)
            lines.append(line_obj)

        return configuration(data["configuration_name"], serial_vars, data["plots"], data["baud_rate"], data["com_port"], data["csv_file"], lines)