import customtkinter as ctk

global configurations
configurations = []

class configuration:
    def __init__(self, configuration_name: str, serial_variables: int, plots: int, baud_rate: int, com_port: int, csv_file: str):
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
        return {
            "configuration_name": self.configuration_name,
            "serial_variables": self.serial_variables,
            "plots": self.plots,
            "baud_rate": self.baud_rate,
            "com_port": self.com_port,
            "csv_file": self.csv_file
        }
    
    def from_dict(data):
        """ Create configuration object from dictionary """
        return configuration(data["configuration_name"], data["serial_variables"], data["plots"], data["baud_rate"], data["com_port"], data["csv_file"])

#thermal_draw = configuration("Thermal Drawing", 5, 3, 115200, 7, "data.csv")
#test_config = configuration("meep", 6, 1, 115200, 3, "wot.csv")
#long_config = configuration("super duper ultra excessively long and gigantic name", 1, 1, 115200, 1, "womp.csv")