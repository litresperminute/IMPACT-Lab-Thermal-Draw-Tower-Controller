#### WARNING: the number of padding columns has to be hte same for each dataset 
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

#PETG_cyl20.0_clear_DR50.0_001.csv
#PETG_cyl20.0_clear_DR50.0_002.csv
#PETG_cyl20.0_clear_DR50.0_003.csv
#PETG_cyl20.0_Clear_DR50.0_003b.csv
#PETG_cyl20.0_clear_DR50.0_004.csv

# === Settings ===
log_dir = "experiment_logs"
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)
experiment_ids = [
    {"filename": "PETG_cyl20.0_clear_DR50.0_002.csv", "start_time": 300, "label": "Trial A"},
    {"filename": "PETG_cyl20.0_clear_DR50.0_001.csv", "start_time": 200, "label": "Trial B"},
    {"filename": "PETG_cyl20.0_clear_DR50.0_003.csv", "start_time": 0, "label": "Trial C"},
    {"filename": "PETG_cyl20.0_clear_DR50.0_004.csv", "start_time": 0, "label": "Trial D"}
]

segment_duration = 200 #seonds

# === Plotting ===
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8, 8), sharex=True)
labels = ["1mm/min","2mm/min","4mm/min","5mm/min"]
lines = [] # store line handles here

for i, exp in enumerate(experiment_ids):
    #Load Exp ID
    filepath = os.path.join(log_dir, exp["filename"])
    df = pd.read_csv(filepath, skiprows=10)

    # Slice and normalize time
    seg = df[(df["Time(s)"] >= exp["start_time"]) & (df["Time(s)"] <= exp["start_time"] + segment_duration)].copy()
    seg["Time(s)"] -= seg["Time(s)"].iloc[0]

    ax = axes[i]
    line, = ax.plot(seg["Time(s)"], seg["Diameter(um)"], label=labels[i],color=colors[i])
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
fig_path = os.path.join(fig_dir, f"Temperature_diameter_plot.png")
#plt.savefig(fig_path) #OPTIONAL SVG EXPORT (need to rename filename to .svg)
plt.savefig(fig_path, dpi=300)
#plt.ion()
plt.show()
print(f"Figure saved to: {fig_path}")