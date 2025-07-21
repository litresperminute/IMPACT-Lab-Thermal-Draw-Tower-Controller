import pandas as pd

# === Load your CSV (assumes metadata starts with "#")
df = pd.read_csv("experiment_logs/PETG 160C DR50 Feed Rate Testing.csv", comment="#")

# === Set analysis parameters
signal_col = "Diameter(um)"
window_sizes = [5, 25, 50, 100, 250, 500]  # rolling window sizes

# === Define time segment to analyze
start_time = 900.0   # in seconds
end_time = 1100.0     # in seconds

# === Filter data by time segment
df_segment = df[(df["Time(s)"] >= start_time) & (df["Time(s)"] <= end_time)].copy()

print(f"Analyzing diameter noise from {start_time}s to {end_time}s:")

# === Loop through each window size and compute detrended std
for window_size in window_sizes:
    # Step 1: Rolling average (trend)
    df_segment["trend"] = df_segment[signal_col].rolling(window=window_size, center=True).mean()

    # Step 2: Residuals
    df_segment["residual"] = df_segment[signal_col] - df_segment["trend"]

    # Step 3: Std dev of residuals
    detrended_std = df_segment["residual"].dropna().std()

    print(f"  Window={window_size:>4}: Detrended Noise Std Dev = {detrended_std:.3f} µm")
