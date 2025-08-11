import serial
import serial.tools.list_ports
import csv
import json
import time
from datetime import datetime
import os


# === STEP 1: Detect Arduino Port ===
def find_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Arduino" in p.description or "ttyACM" in p.device or "ttyUSB" in p.device:
            return p.device
    return None

# === STEP 2: Prompt for and Save Metadata ===
def save_metadata(log_dir):
    material = input("Material used (e.g., PETG): ")

    geometry = input("Preform geometry (ie. cyl, sq, 7ch): ")

    preform_diameter = input("Preform diameter in mm (default = 20): ")
    try:
        preform_diameter = float(preform_diameter) if preform_diameter.strip() else 20.0
    except:
        None 

    material_color = input("Material color: ")

    temperature = input("Temperature in °C (optional): ")
    try:
        temperature = float(temperature) if temperature.strip() else None
    except:
        None # If input is not a number, save as string by default

    drawdown_ratio = input("Drawdown ratio (DR) (optional): ")
    try:
        drawdown_ratio = float(drawdown_ratio) if drawdown_ratio.strip() else None
    except:
        None # If input is not a number, save as string by default

    trial_number = input("Trial number for this setup (ie. 001): ")

    operator = input("Operator name: ")
    notes = input("Enter any notes (optional): ").replace(",",";") # Take out commas and replace them with something else

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

    # Write Metadata and Headers into CSV
    with open(csv_filename, 'w', newline='') as f:
        for key, value in metadata.items():
            if value is None:
                value = ""
            f.write(f"# {key}: {value}\n")
        f.write("Time(s),Feed(mm/min),Wind(m/min),Diameter(um),Predicted_diameter(um)\n")
    print(f"Metadata and headers written to: {csv_filename}")
    return csv_filename

# === STEP 3: Log Serial Data (Filter + Print Non-Data Lines) ===
def log_serial_data(port, baud=115200, csv_filename='Unnamed_trial'):
    try:
        with serial.Serial(port, baud, timeout=1) as ser, open(csv_filename, 'a', newline='') as csvfile:
            print(f"\nLogging started. Press Ctrl+C to stop.\nSaving to: {csv_filename}")
            writer = csv.writer(csvfile)
            """ writer.writerow([
                "Time(s)",
                "Feed(mm/min)",
                "Wind(m/min)",
                "Diameter(um)",
                "Predicted_diameter(um)"
            ]) """
            
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
        print(f"\nLogging stopped by user. Saved to {csv_filename}")
    except Exception as e:
        print("Error:", e)

# === Run Everything ===
def main():
    #Setup Output Directory
    log_dir = "Thermal Draw Trials\ThesisExperiments\PETGexperiment_logs"
    os.makedirs(log_dir, exist_ok=True)

    port = find_port()
    if not port:
        print("No Arduino found.")
    else:
        csv_filename = save_metadata(log_dir)

        input("Press Enter to begin logging...")

        log_serial_data(port,csv_filename=csv_filename)

if __name__ == "__main__":
    main()