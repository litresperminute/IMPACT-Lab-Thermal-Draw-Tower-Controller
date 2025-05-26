from configuration import configuration, configurations
from resource_manager import CONFIG_FILE, CSV
import csv
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
    except (FileNotFoundError, json.JSONDecodeError):
        return [] 
    
def save_configurations(configs):
    """ Saves configuration object changes to JSON file """
    with open(CONFIG_FILE, "w") as file:
        json.dump([cfg.to_dict() for cfg in configs], file, indent=4)

def update_metadata(data_row: list[str], csv_recording: bool, communication_dict: dict):
    if csv_recording:
        print(f"NEW TRIAL 3 - {communication_dict['new_trial']}")
        with open(CSV, "a", newline="") as file:
            writer = csv.writer(file)
            if communication_dict['new_trial']:
                trial_num = [str(communication_dict['trial_num'])]
                writer.writerow(trial_num)
                communication_dict['new_trial'] = False
            else:
                print(f"I AM CONFUSED!")
            writer.writerow(data_row)
    return
    
def erase_csv():
    with open(CSV, "w", newline="") as file:
        pass
    
def is_csv_empty():
    csv_size = os.path.getsize(CSV)
    if not csv_size:
        return True
    return False

def find_file(filename, start_dir=os.path.expanduser("~")):
    for root, _, files, in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None