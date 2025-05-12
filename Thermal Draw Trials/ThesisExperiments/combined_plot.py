import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib as mpl
import seaborn as sns
import os
import json
#Specify some matplotlib defaults
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 14
#Try a color from seaborn
colors = sns.color_palette("pastel6",4)

# === Settings ===
experiment_id = 'PETG 160C DR50 Feed Rate Testing'
log_dir = "experiment_logs"
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)

# === Load Data ===
csv_path = os.path.join(log_dir, f"{experiment_id}.csv")
print("Looking in:", csv_path)
json_path = os.path.join(log_dir, f"{experiment_id}_metadata.json")

df = pd.read_csv(csv_path)
with open(json_path, "r") as f:
    meta = json.load(f)
    
# === Define feedrate time ranges and labels ===
ranges = [(400, 600), (900, 1100), (1200, 1400), (1600, 1800)]
labels = ["Feedrate: 10 mm/min", "Feedrate: 20 mm/min", "Feedrate: 30 mm/min", "Feedrate: 40 mm/min"]

x_segments = []
y_segments = []

# === Slice, normalize, and store data ===
for start, end in ranges:
    seg = df[(df["Time(s)"] >= start) & (df["Time(s)"] <= end)].copy()
    seg["Time(s)"] = seg["Time(s)"] - seg["Time(s)"].iloc[0]  # normalize time to 0
    x_segments.append(seg["Time(s)"].to_numpy())
    y_segments.append(seg["Diameter(um)"].to_numpy())

# === Plot all segments on one figure ===
fig, ax = plt.subplots(figsize=(8, 5))
lines = []

for i in range(len(x_segments)):
    line, = ax.plot(x_segments[i], y_segments[i], label=labels[i])
    lines.append(line)

# Add target line
target_line = ax.axhline(y=400, color='red', linestyle='--', linewidth=1.2, label='Target = 400μm')

# Aesthetics
ax.set_xlabel("Normalized Time (s)")
ax.set_ylabel("Diameter (μm)")
ax.set_ylim(200, 1200)
ax.grid(True)

# Shared legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

plt.tight_layout(rect=[0, 0, 1, 1.1])  # make room for legend
plt.show()
