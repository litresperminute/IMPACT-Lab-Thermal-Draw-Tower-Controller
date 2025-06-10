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

# === STEP 1: Prompt for Metadata ===
experiment_id = input("Enter experiment ID (e.g., draw_test_003): ")

material = input("Enter material used (e.g., PETG): ")
material_color = input("Enter material color: ")

preform_diameter = input("Enter preform diameter in mm (default = 20): ")
preform_diameter = float(preform_diameter) if preform_diameter.strip() else 20.0

temperature = input("Enter temperature in °C (optional): ")
temperature = float(temperature) if temperature.strip() else None

drawdown_ratio = input("Enter drawdown ratio (DR) (optional): ")
drawdown_ratio = float(drawdown_ratio) if drawdown_ratio.strip() else None

perator = input("Enter your name: ")

notes = input("Enter any notes (optional): ")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
csv_filename = os.path.join(log_dir, f"{material}{experiment_id}.csv")
json_filename = os.path.join(log_dir, f"{material}{experiment_id}_metadata.json")

# === STEP 2: Detect Arduino Port ===
def find_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "ttyACM" in p.device or "ttyUSB" in p.device:
            return p.device
    return None

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
        print("\nLogging stopped by user.")
    except Exception as e:
        print("Error:", e)


# === STEP 4: Save Metadata to JSON ===
def save_metadata():
    metadata = {
        "experiment_id": experiment_id,
        "material": material,
        "material_color": material_color,
        "preform_diameter": preform_diameter,
        "temperature_C": temperature,
        "drawdown_ratio": drawdown_ratio,
        "operator": operator,
        "start_time": timestamp,
        "notes": notes
    }
    with open(json_filename, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to: {json_filename}")

# === Run Everything ===
port = find_port()
if not port:
    print("No Arduino found.")
else:
    save_metadata()
    log_serial_data(port)
