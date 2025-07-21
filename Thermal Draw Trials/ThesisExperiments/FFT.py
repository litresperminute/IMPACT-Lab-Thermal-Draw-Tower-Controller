import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load CSV (assumes metadata lines start with "#")
df = pd.read_csv("experiment_logs\PETG_oct90deg-annealed20.0_black_DR50.0_001.csv", comment="#")

# === Set analysis parameters
signal_col = "Diameter(um)"
time_col = "Time(s)"
start_time =  750.0   # in seconds
end_time = 1000.0     # in seconds

# === Select segment
df_segment = df[(df[time_col] >= start_time) & (df[time_col] <= end_time)].copy()

# === Extract signal and time
time = df_segment[time_col].values
signal = df_segment[signal_col].values

# === Estimate sampling rate
time_diffs = np.diff(time)
if not np.allclose(time_diffs, time_diffs[0], atol=1e-3):
    print("Warning: Non-uniform time steps detected — FFT may be less accurate.")
dt = np.mean(time_diffs)
fs = 1 / dt  # sampling frequency (Hz). Should be 5hz. 

# === Perform FFT
N = len(signal)
freqs = np.fft.rfftfreq(N, d=dt)  # real-valued FFT frequency bins
fft_values = np.fft.rfft(signal)
amplitudes = np.abs(fft_values) * 2 / N  # normalize amplitude





####METRICS
# 0. Trim amplitudes
amplitudes = amplitudes[5:]
freqs = freqs[5:]
# 1. Total power
total_power = np.sum(amplitudes**2)

# 2. Spectral centroid
centroid = np.sum(freqs * amplitudes) / np.sum(amplitudes)

# 3. Spectral spread
spread = np.sqrt(np.sum(((freqs - centroid)**2) * amplitudes) / np.sum(amplitudes))

# 4. Peak frequency
peak_freq = freqs[np.argmax(amplitudes)]

# 5. Low/high frequency power ratio (cutoff at 10 Hz)
low_mask = freqs < 10
high_mask = freqs >= 10
low_power = np.sum(amplitudes[low_mask]**2)
high_power = np.sum(amplitudes[high_mask]**2)
low_high_ratio = low_power / high_power if high_power > 0 else np.nan

# Print results
print(f"Total Spectral Power:       {total_power:.3f}")
print(f"Spectral Centroid:          {centroid:.3f} Hz")
print(f"Spectral Spread:            {spread:.3f} Hz")
print(f"Peak Frequency:             {peak_freq:.3f} Hz")
print(f"Low-to-High Freq Power Ratio (<10 Hz / ≥10 Hz): {low_high_ratio:.3f}")




# === Plot frequency spectrum
plt.figure(figsize=(10, 5))
plt.plot(freqs, amplitudes, label="FFT Amplitude Spectrum",color="b")
plt.ylim(0,50)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (µm)")
plt.title(f"FFT of Diameter Signal ({start_time}s to {end_time}s)")
plt.grid(True)
plt.tight_layout()
plt.show()
