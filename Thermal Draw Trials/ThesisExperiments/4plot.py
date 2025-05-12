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

#downsample data to every 10th data point
#df = df.iloc[::10, :]

# === Define feedrate segments ===
ranges = [(400, 600), (900, 1100), (1200, 1400), (1600, 1800)]
x_segments = []
y_segments = []

for start, end in ranges:
    seg = df[(df["Time(s)"] >= start) & (df["Time(s)"] <= end)].copy()
    
    # Normalize time: subtract the first timestamp
    seg["Time(s)"] = seg["Time(s)"] - seg["Time(s)"].iloc[0]
    
    x_segments.append(seg["Time(s)"].to_numpy())
    y_segments.append(seg["Diameter(um)"].to_numpy())


# === Plotting ===

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8, 8), sharex=True)
labels = ["Feedrate: 1 mm/min", "Feedrate: 2 mm/min", "Feedrate: 4 mm/min", "Feedrate: 5 mm/min"]
lines = [] # store line handles here

for i, ax in enumerate(axes):
    line, = ax.plot(x_segments[i], y_segments[i], label=labels[i],color=colors[i])
    lines.append(line)
    ax.axhline(y=400, color='red', linestyle='--', linewidth=1.2, label='Target Dia. = 400 μm')
    ax.legend(loc='upper right', fontsize=10, edgecolor='white', facecolor='white', framealpha=0.5)
    ax.grid(False)
    ax.set_ylim(200,1050)
    ax.set_xlim(0,205)
    # Customize ticks
    ax.minorticks_on()
    ax.tick_params(which='major',axis='both', direction='in', length=6, width=1, labelsize=11)
    ax.tick_params(which='minor',axis='both', direction='in', length=2, width=0.8)
    ax.set_xticks(np.arange(0, 201, 20))  # X ticks every 20s (adjust as needed)

# Global labels
fig.text(0.55, 0.04, 'Time (s)', ha='center', fontsize=14)
fig.text(0.04, 0.55  , 'Diameter (μm)', va='center', rotation='vertical', fontsize=14)

# Shared legend
#fig.legend(handles=lines + [target_line], loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0), frameon=False, fontsize=10)

# Layout
plt.tight_layout(rect=[0.06, 0.06, 1, 0.96])  # leave space at top for legend

# === Save & Show ===
fig_path = os.path.join(fig_dir, f"{experiment_id}_diameter_plot.png")
#plt.savefig(fig_path) #OPTIONAL SVG EXPORT (need to rename filename to .svg)
plt.savefig(fig_path, dpi=300)
#plt.ion()
plt.show()
print(f"Figure saved to: {fig_path}")