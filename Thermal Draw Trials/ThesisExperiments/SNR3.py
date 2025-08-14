import pandas as pd
import os

# === Configuration: Files and time segments ===
analysis_plan = [
    {
        "filename": "experiment_logs/PETG_oct20.0_black_DR50.0_011.csv",
        "start_time": 200.0,
        "end_time": 800.0
    }
]

# === Parameters ===
signal_col = "Diameter(um)"
time_col = "Time(s)"
window_sizes = [5, 25, 50, 100, 250, 500]
target_diameter = 400  # Target fiber diameter in µm

# === Results list
results = []

# === Loop through each file
for plan in analysis_plan:
    file = plan["filename"]
    start_time = plan["start_time"]
    end_time = plan["end_time"]

    print(f"\nAnalyzing file: {file}")
    print(f"  Time segment: {start_time}s to {end_time}s")

    # Load entire file
    df = pd.read_csv(file, comment="#")

    # Bias is computed only within time window (raw signal)
    df_bias_segment = df[(df[time_col] >= start_time) & (df[time_col] <= end_time)].copy()
    if df_bias_segment.empty:
        print("  Warning: No data in specified time range.")
        continue

    bias = df_bias_segment[signal_col].mean() - target_diameter

    # Loop through each window size
    for window_size in window_sizes:
        df_copy = df.copy()

        # Compute trend using centered rolling average on the full data
        df_copy["trend"] = df_copy[signal_col].rolling(window=window_size, center=True).mean()
        df_copy["residual"] = df_copy[signal_col] - df_copy["trend"]

        # Truncate *after* rolling average to preserve center info
        df_segment = df_copy[(df_copy[time_col] >= start_time) & (df_copy[time_col] <= end_time)].copy()

        # Drop NaNs (from rolling) before calculating std
        detrended_std = df_segment["residual"].dropna().std()

        print(f"    Window={window_size:>4}: Std = {detrended_std:.3f} µm | Bias = {bias:.3f} µm")

        results.append({
            "filename": os.path.basename(file),
            "start_time": start_time,
            "end_time": end_time,
            "window_size": window_size,
            "detrended_std_um": round(detrended_std, 4),
            "bias_um": round(bias, 4)
        })

# === Save all results to CSV
output_df = pd.DataFrame(results)
output_df.to_csv("detrended_noise_and_bias_summary.csv", index=False)
print("\n✅ Results saved to 'detrended_noise_and_bias_summary.csv'")
