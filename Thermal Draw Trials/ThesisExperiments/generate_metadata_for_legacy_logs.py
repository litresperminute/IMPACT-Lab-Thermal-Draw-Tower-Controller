import os
import json
import pandas as pd

log_dir = "experiment_logs"
expected_columns = [
    "Time(s)",
    "Feed(mm/min)",
    "Wind(m/min)",
    "Diameter(um)",
    "Predicted_diameter(um)"
]

def prompt_metadata(exp_id):
    print(f"\nCreating metadata for: {exp_id}")
    material = input("Material (e.g., PETG): ")
    color = input("Material color (e.g., natural, black): ")
    diameter_input = input("Preform diameter in mm [default = 20]: ")
    preform_diameter = float(diameter_input) if diameter_input.strip() else 20.0
    temperature = input("Enter temperature in °C (optional): ")
    temperature = float(temperature) if temperature.strip() else None
    drawdown_ratio = input("Enter drawdown ratio (DR) (optional): ")
    drawdown_ratio = float(drawdown_ratio) if drawdown_ratio.strip() else None
    operator = input("Operator name: ")
    notes = input("Any notes? (optional): ")

    return {
        "experiment_id": exp_id,
        "material": material,
        "material_color": color,
        "preform_diameter_mm": preform_diameter,
        "temperature_C": temperature,
        "drawdown_ratio": drawdown_ratio,
        "operator": operator,
        "start_time": "Unknown",
        "notes": notes
    }

def standardize_and_save_csv(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".xlsx":
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    if df.shape[1] == 5:
        df.columns = expected_columns
        df.to_csv(output_path, index=False)
        print(f"Standardized and saved CSV: {output_path}")
    else:
        print(f"⚠️  Skipped {input_path} — unexpected number of columns.")

def main():
    files = [f for f in os.listdir(log_dir) if f.endswith(".csv") or f.endswith(".xlsx")]
    for file in files:
        base_name = os.path.splitext(file)[0]
        input_path = os.path.join(log_dir, file)
        output_csv_path = os.path.join(log_dir, f"{base_name}.csv")
        metadata_path = os.path.join(log_dir, f"{base_name}_metadata.json")

        if not os.path.exists(output_csv_path) or file.endswith(".xlsx"):
            standardize_and_save_csv(input_path, output_csv_path)

        if not os.path.exists(metadata_path):
            metadata = prompt_metadata(base_name)
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)
            print(f"Saved metadata to {metadata_path}")
        else:
            print(f"Metadata already exists for {base_name}, skipping.")

if __name__ == "__main__":
    main()