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
global LOG_DIR
LOG_DIR = "experiment_logs"
os.makedirs(LOG_DIR, exist_ok=True) #Ensure folder exists
global CSV
CSV = os.path.join(LOG_DIR, "trial_metadata.csv")