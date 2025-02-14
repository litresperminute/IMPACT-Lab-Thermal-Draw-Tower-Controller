import customtkinter as ctk
from serial_variables import serial_variable

global configurations
configurations = []

class configuration:
    def __init__(self, configuration_name: str, serial_variables: list, plots: int, baud_rate: int, com_port: int, csv_file: str):
        # Configuration Object Attributes
        self.configuration_name = configuration_name
        self.serial_variables = serial_variables
        self.plots = plots
        self.baud_rate = baud_rate
        self.com_port = com_port
        self.csv_file = csv_file

        # Appends New Configuration Objects to the List
        configurations.append(self)

    def to_dict(self):
        """ Convert configuration object to dictionary """
        converted_serials = []
        for serial_var in self.serial_variables:
            converted_serial = serial_var.serial_to_dict()
            converted_serials.append(converted_serial)

        return {
            "configuration_name": self.configuration_name,
            "serial_variables": converted_serials,
            "plots": self.plots,
            "baud_rate": self.baud_rate,
            "com_port": self.com_port,
            "csv_file": self.csv_file
        }
    
    def from_dict(data):
        """ Create configuration object from dictionary """
        serial_data = data["serial_variables"]
        serial_vars = []
        for serial in serial_data:
            serial_var = serial_variable.serial_from_dict(serial)
            serial_vars.append(serial_var)

        return configuration(data["configuration_name"], serial_vars, data["plots"], data["baud_rate"], data["com_port"], data["csv_file"])

#thermal_draw = configuration("Thermal Drawing", 5, 3, 115200, 7, "data.csv")
#test_config = configuration("meep", 6, 1, 115200, 3, "wot.csv")
#long_config = configuration("super duper ultra excessively long and gigantic name", 1, 1, 115200, 1, "womp.csv")