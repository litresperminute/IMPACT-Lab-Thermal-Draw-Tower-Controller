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

        # Raise Error for Duplicate Configuration Names
        #for config in configurations[:-1]:
            #if configurations[-1].configuration_name == config.configuration_name:
                #self.openDuplicateWarning(configurations[-1], config)

    #def openDuplicateWarning(self, newConfig, duplicateConfig):
        #open_duplicate_warning_window(newConfig, duplicateConfig)


#def open_duplicate_warning_window(newConfig, duplicateConfig):
    #from duplicate_warning_window import duplicateWarningWindow
    #warning_win = duplicateWarningWindow(newConfig, duplicateConfig)
    #warning_win.mainloop()

thermal_draw = configuration("Thermal Drawing", 5, 3, 115200, 7, "data.csv")
test_config = configuration("meep", 6, 1, 115200, 3, "wot.csv")