import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# === Configure Experiment IDs ===
experiment_ids = [
    "PETG001",
    "PETG1",
    "CLEAR PETG NO FEEDBACK 160C DR50"
]

log_dir = "experiment_logs"
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)

# === Plot Setup ===
plt.figure(figsize=(8, 5))

for exp_id in experiment_ids:
    csv_path = os.path.join(log_dir, f"{exp_id}.csv")
    json_path = os.path.join(log_dir, f"{exp_id}_metadata.json")

    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        print(f"Missing file(s) for: {exp_id}")
        continue

    df = pd.read_csv(csv_path)
    with open(json_path, "r") as f:
        meta = json.load(f)

    label = f"{meta.get('material', '')} - {exp_id} ({meta.get('material_color', '')})"
    plt.plot(df["Time(s)"], df["Diameter(um)"], label=label)

plt.title("Draw Trial Comparison")
plt.xlabel("Time (s)")
plt.ylabel("Diameter (μm)")
plt.legend()
plt.grid(True)
plt.tight_layout()

fig_path = os.path.join(fig_dir, "draw_trial_comparison.png")
plt.savefig(fig_path, dpi=300)
plt.show()

print(f"Plot saved to: {fig_path}")