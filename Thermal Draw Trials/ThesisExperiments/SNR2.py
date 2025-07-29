import pandas as pd
import os

# === Configuration: Files and time segments ===
analysis_plan = [

    {
        "filename": "experiment_logs/kp_0.01, ki_0.005.csv",
        "start_time": 100.0,
        "end_time": 300.0
    }
    
    # Add more entries here as needed
]

# === Parameters ===
signal_col = "Diameter(um)"
time_col = "Time(s)"
window_sizes = [5, 25, 50, 100, 250, 500]
target_diameter = 381  # Target fiber diameter in µm

# === Results list
results = []

# === Loop through each file
for plan in analysis_plan:
    file = plan["filename"]
    start_time = plan["start_time"]
    end_time = plan["end_time"]

    print(f"\nAnalyzing file: {file}")
    print(f"  Time segment: {start_time}s to {end_time}s")

    # Load and segment the file
    df = pd.read_csv(file, comment="#")
    df_segment = df[(df[time_col] >= start_time) & (df[time_col] <= end_time)].copy()

    if df_segment.empty:
        print("  Warning: No data in specified time range.")
        continue

    # Calculate bias (mean deviation from target)
    bias = df_segment[signal_col].mean() - target_diameter

    # Loop through each window size
    for window_size in window_sizes:
        # Rolling average (trend)
        df_segment["trend"] = df_segment[signal_col].rolling(window=window_size, center=True).mean()

        # Residuals
        df_segment["residual"] = df_segment[signal_col] - df_segment["trend"]

        # Std dev of residuals (detrended noise)
        detrended_std = df_segment["residual"].dropna().std()

        print(f"    Window={window_size:>4}: Std = {detrended_std:.3f} µm | Bias = {bias:.3f} µm")

        # Store result
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
