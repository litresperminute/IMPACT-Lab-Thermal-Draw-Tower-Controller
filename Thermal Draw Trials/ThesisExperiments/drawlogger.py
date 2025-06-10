import serial
import serial.tools.list_ports
import csv
import json
import time
from datetime import datetime
import os

# === Setup Output Directory ===
log_dir = "experiment_logs"
os.makedirs(log_dir, exist_ok=True)


# === STEP 1: Detect Arduino Port ===
def find_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "ttyACM" in p.device or "ttyUSB" in p.device:
            return p.device
    return None

# === STEP 2: Prompt for and Save Metadata ===
def save_metadata():
    material = input("Material used (e.g., PETG): ")

    geometry = input("Preform geometry (ie. cyl, sq, 7ch): ")

    preform_diameter = input("Preform diameter in mm (default = 20): ")
    preform_diameter = float(preform_diameter) if preform_diameter.strip() else 20.0

    material_color = input("Material color: ")

    temperature = input("Temperature in °C (optional): ")
    temperature = float(temperature) if temperature.strip() else None

    drawdown_ratio = input("Drawdown ratio (DR) (optional): ")
    drawdown_ratio = float(drawdown_ratio) if drawdown_ratio.strip() else None

    trial_number = input("Trial number for this setup: ")

    operator = input("Operator name: ")

    notes = input("Enter any notes (optional): ")

    file_name = f"{material}_{geometry}{preform_diameter}_{material_color}_DR{drawdown_ratio}_{trial_number}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_filename = os.path.join(log_dir, f"{file_name}.csv")
    json_filename = os.path.join(log_dir, f"META-{file_name}.json")
    
    metadata = {
        "material": material,
        "geometry": geometry,
        # "experiment_id": experiment_id,
        "preform_diameter": preform_diameter,
        "material_color": material_color,
        "temperature_C": temperature,
        "drawdown_ratio": drawdown_ratio,
        "trial_number": trial_number,
        "operator": operator,
        "start_time": timestamp,
        "notes": notes
    }


    with open(json_filename, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to: {json_filename}")

# === STEP 3: Log Serial Data (Filter + Print Non-Data Lines) ===
def log_serial_data(port, baud=115200):
    try:
        with serial.Serial(port, baud, timeout=1) as ser, open(csv_filename, 'w', newline='') as csvfile:
            print(f"\nLogging started. Press Ctrl+C to stop.\nSaving to: {csv_filename}")
            writer = csv.writer(csvfile)
            writer.writerow([
                "Time(s)",
                "Feed(mm/min)",
                "Wind(m/min)",
                "Diameter(um)",
                "Predicted_diameter(um)"
            ])
            
            start_time = time.time()
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(line)
                    if time.time() - start_time < 2:
                        continue  # skip first 2 seconds of readings
                    parts = line.split(",")
                    if len(parts) == 5:
                        writer.writerow(parts)
    except KeyboardInterrupt:
        print(f"\nLogging stopped by user. Saved to {csv_filename}.csv")
    except Exception as e:
        print("Error:", e)

# === Run Everything ===
def main():
    port = find_port()
    if not port:
        print("No Arduino found.")
    else:
        save_metadata()

        input("Press Enter to begin logging...")

        log_serial_data(port)


main()