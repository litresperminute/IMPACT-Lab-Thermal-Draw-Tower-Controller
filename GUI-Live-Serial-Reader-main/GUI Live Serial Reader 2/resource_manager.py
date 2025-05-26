import os
global script_dir
script_dir = os.path.dirname(os.path.abspath(__file__))
global icon_path
icon_path = os.path.join(script_dir, "Resources", "serial_port_icon_blue.ico")
global error_icon_path
error_icon_path = os.path.join(script_dir, "Resources", "error_icon.png")
global CONFIG_FILE
CONFIG_FILE = os.path.join(script_dir, "configurations.json")
global CURRENT_CONFIG
CURRENT_CONFIG = os.path.join(script_dir, "current_config.json")
global COMMUNICATION
COMMUNICATION = os.path.join(script_dir, "communication.json")
global CSV
CSV = os.path.join(script_dir, "trial_metadata.csv")