## CSV METADATA INJECTOR
## This script will take a .csv's metadata .json file and add it to the .csv's first row

import os
import json

folder_path = os.path.join(os.path.dirname(__file__), "experiment_logs")

for file in os.listdir(folder_path):
    if file.endswith(".json"):
        json_path = os.path.join(folder_path, file)
        csv_name = file.replace("_metadata.json", ".csv")
        csv_path = os.path.join(folder_path, csv_name)

        if not os.path.exists(csv_path):
            continue

        # Read metadata from JSON
        with open(json_path, 'r') as jf:
            metadata = json.load(jf)

        # Read original CSV content
        with open(csv_path, 'r') as cf:
            csv_lines = cf.readlines()

        # Create metadata comment lines
        metadata_lines = []
        for key, value in metadata.items():
            if value is None:
                value = ""
            metadata_lines.append(f"# {key}: {value}\n")

        # Prepend metadata and overwrite CSV
        with open(csv_path, 'w') as cf:
            cf.writelines(metadata_lines + csv_lines)
