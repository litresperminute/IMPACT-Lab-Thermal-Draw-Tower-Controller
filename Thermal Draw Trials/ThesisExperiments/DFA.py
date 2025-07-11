import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit

def dfa(signal, window_sizes):
    """
    Perform Detrended Fluctuation Analysis (DFA) on a 1D signal.
    
    Parameters:
    - signal: 1D array-like (the time series)
    - window_sizes: list of integers (window sizes to test)

    Returns:
    - flucts: list of RMS fluctuations for each window size
    - alpha: estimated scaling exponent from log-log fit
    """
    # Step 1: Integrated signal (cumulative sum after mean subtraction)
    signal = np.array(signal)
    signal -= np.mean(signal)
    profile = np.cumsum(signal)

    flucts = []

    # Step 2: Loop over window sizes
    for win in window_sizes:
        if win >= len(profile) // 2:
            continue  # avoid too-large windows
        n_segments = len(profile) // win
        rms = []

        for i in range(n_segments):
            seg = profile[i * win:(i + 1) * win]
            x = np.arange(win)
            # Linear detrending
            coeffs = polyfit(x, seg, deg=1)
            trend = coeffs[0] + coeffs[1] * x
            rms.append(np.sqrt(np.mean((seg - trend)**2)))

        flucts.append(np.mean(rms))

    # Step 3: Log-log plot and slope estimation
    log_win = np.log10(window_sizes[:len(flucts)])
    log_fluct = np.log10(flucts)
    alpha, _ = polyfit(log_win, log_fluct, deg=1)

    # Plot
    plt.figure(figsize=(6, 4))
    plt.plot(log_win, log_fluct, 'o-', label=f'α ≈ {alpha:.3f}')
    plt.xlabel("log10(Window size)")
    plt.ylabel("log10(Fluctuation)")
    plt.title("DFA: Detrended Fluctuation Analysis")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return flucts, alpha

# === Example usage ===
# Load your data
df = pd.read_csv("experiment_logs/PETG_oct20.0_black_DR50.0_001.csv", comment="#")
signal = df["Diameter(um)"].dropna().values

# Window sizes (logarithmic or linear spacing)
window_sizes = np.unique(np.logspace(1, np.log10(len(signal)//4), 20, dtype=int))

# Run DFA
fluctuations, scaling_exponent = dfa(signal, window_sizes)
print(f"Estimated scaling exponent (α): {scaling_exponent:.3f}")
