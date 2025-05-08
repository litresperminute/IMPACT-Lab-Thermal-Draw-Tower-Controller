from configuration import configuration, configurations
from file_manager import CONFIG_FILE
import json
import os

def load_configurations():
    """ Load configuration objects from JSON file """
    configurations.clear()
    try:
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)

            for config in data:
                configuration.from_dict(config)

            return data
    except  (FileNotFoundError, json.JSONDecodeError):
        return [] 
    
def save_configurations(configs):
    """ Saves configuration object changes to JSON file """
    with open(CONFIG_FILE, "w") as file:
        json.dump([cfg.to_dict() for cfg in configs], file, indent=4)

def find_file(filename, start_dir=os.path.expanduser("~")):
    for root, _, files, in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None