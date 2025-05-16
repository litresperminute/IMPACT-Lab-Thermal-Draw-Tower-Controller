import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import numpy as np

# === Settings ===

experiment_id = input("Experiment ID: ") # CLEAR PETG NO FEEDBACK 160C DR50
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

# === Plotting ===

xmin,xmax = [0,1970]
ymin,ymax = [0,1000]

plt.figure(figsize=(6, 4))
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.autoscale(enable=False)
plt.plot(df["Time(s)"], df["Diameter(um)"], label="Measured Diameter", linewidth=1)
plt.axhline(y=400, color='red', linestyle='--', linewidth=1.2, label='Target = 400μm')
plt.title(f"{meta['material']} ({meta['material_color']})")
plt.xlabel("Time (s)")
plt.ylabel("Diameter (μm)")
plt.legend()
plt.grid(False)
plt.tight_layout()


#Define where you want ticks
xticks = np.arange(xmin,(xmax+1),(xmax/4))
yticks = np.arange(ymin,(ymax+1),(ymax/4))
#xticks = np.arange()
#yticks = np.arange()

plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=5, bottom=True, top=False, left=True, right=False)
plt.tick_params(direction='in', which='major', length=10, bottom=True, top=False, left=True, right=False)
plt.xticks(xticks)
plt.yticks(yticks)


# === Save & Show ===
fig_path = os.path.join(fig_dir, f"{experiment_id}_diameter_plot.png")
#plt.savefig(fig_path)
plt.savefig(fig_path, dpi=300)
#plt.ion()
plt.show()
plt.close('all')         # closes all open figures

print(f"Figure saved to: {fig_path}")