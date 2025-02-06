global configurations
configurations = []

class configuration:
    def __init__(self, configuration_name: str, serial_variables: int, plots: int, baud_rate: int, com_port: int, csv_file: str):
        self.configuration_name = configuration_name
        self.serial_variables = serial_variables
        self.plots = plots
        self.baud_rate = baud_rate
        self.com_port = com_port
        self.csv_file = csv_file

        configurations.append(self)

thermal_draw = configuration("Thermal Drawing", 5, 3, 115200, 7, "data.csv")
test_config = configuration("meep", 6, 1, 115200, 3, "wot.csv")