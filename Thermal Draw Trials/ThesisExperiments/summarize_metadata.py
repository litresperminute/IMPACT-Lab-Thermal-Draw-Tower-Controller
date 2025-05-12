import os
import json
import pandas as pd

log_dir = "experiment_logs"  # adjust path as needed
metadata_records = []

for root, dirs, files in os.walk(log_dir):
    for file in files:
        if file.endswith("metadata.json"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                data = json.load(f)
                data["folder"] = os.path.basename(root)
                metadata_records.append(data)

df = pd.DataFrame(metadata_records)
df.sort_values("experiment_id", inplace=True)
df.to_csv("experiment_metadata_summary.csv", index=False)

print("Saved summary to experiment_metadata_summary.csv")
