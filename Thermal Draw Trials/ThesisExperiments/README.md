# Generated with much help from ChatGPT because my coding is not so great :'>
# 📈 Thesis Experiment Logger

This tool logs serial data from an Arduino and saves it into a structured `.csv` file with matching experiment metadata in `.json` format. It is designed for high-quality, reproducible data collection for thesis or research work.

---

## 🛠️ Features

- Automatically detects the Arduino COM port
- Prompts you for experiment metadata
- Filters out non-data serial messages (e.g., status/debug prints)
- Saves:
  - A `.csv` data log with column headers
  - A `.json` metadata file with full experiment context
- Clean and customizable — no external UI required

---

## 🚀 How to Use

### 1. 🧪 Prepare Your Arduino
Make sure your Arduino is connected and actively sending comma-separated serial data in this format:

```
Time(s),Feed(mm/min),Wind(m/min),Diameter(um),Predicted_diameter(um)
```

You can include other status/debug messages — they’ll be shown in the terminal but not saved to the CSV.

---

### 2. ▶️ Run the Script

Open a terminal in the project folder and run:

```bash
python drawlogger.py
```

You will be prompted to enter:

- Experiment ID (used as the filename)
- Material
- Material color
- Operator name
- Notes (optional)
- Preform diameter (defaults to 20mm if left blank)

Once you enter this info, the script will begin logging data in real time. When you’re done, press **Ctrl+C** to stop.

---

### 3. 📁 Output Files

For each experiment, the following will be created in your working directory:

- `experiment_id.csv` — raw serial data with headers
- `experiment_id_metadata.json` — metadata (material, operator, diameter, notes, etc.)

Example:
```
draw_test_007.csv
draw_test_007_metadata.json
```

---

## 🧼 Notes

- The script ignores serial lines that don’t match the expected data format (5 comma-separated values)
- The Arduino must not be connected to another serial monitor at the same time (e.g., VSCode Serial Monitor)
- If no Arduino is detected, the script will alert you and exit

---

## 📦 Dependencies

Install Python packages using:

```bash
pip install pyserial
```

---

## 📚 Customization Ideas

- Save experiments into subfolders
- Automatically generate experiment IDs
- Add real-time plotting while logging

---

## 👨‍🔬 Developed by Luka Morita
Feel free to modify this script to fit your lab’s workflow or thesis needs.