import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FILENAME = "dataayrılıksözlü.csv"   # same CSV saved by your acquisition script
FMAX = 10000.0           # analyze 0–5000 Hz

def main():
    # 1. Load data
    df = pd.read_csv(FILENAME)
    t = df["time_s"].values
    V = df["voltage"].values

    N = len(V)
    if N < 2:
        raise RuntimeError("Not enough data points in CSV.")

    print(f"Loaded {N} samples from {FILENAME}")

    # 2. Estimate sampling rate
    dt = np.mean(np.diff(t))
    fs = 1.0 / dt
    print(f"Estimated sampling rate: {fs:.2f} Hz")

    # 3. Detrend (remove DC) and apply Hann window
    V_detrended = V - np.mean(V)
    window = np.hanning(N)
    V_win = V_detrended * window

    # Coherent gain of Hann window (for amplitude correction)
    # This keeps amplitudes closer to true values
    coherent_gain = np.mean(window)

    # 4. FFT (one-sided, real)
    fft_vals = np.fft.rfft(V_win)
    freqs = np.fft.rfftfreq(N, d=dt)

    # 5. Amplitude spectrum (single-sided)
    # Base scaling: divide by N and coherent gain
    amplitude = np.abs(fft_vals) / (N * coherent_gain)

    # Factor of 2 for single-sided spectrum (except DC & Nyquist)
    if N % 2 == 0:
        amplitude[1:-1] *= 2.0
    else:
        amplitude[1:] *= 2.0

    # 6. Restrict to 0–FMAX Hz
    mask = (freqs >= 0) & (freqs <= FMAX)
    freqs_band = freqs[mask]
    amps_band = amplitude[mask]

    # 7. Find top 10 peaks in this band (ignoring DC bin at 0 Hz)
    if len(freqs_band) <= 1:
        print("Not enough frequency bins in 0–5000 Hz to analyze.")
        return

    # ignore DC for peak search
    start_idx = 1  # skip index 0 (0 Hz)
    amps_for_peaks = amps_band[start_idx:]
    freqs_for_peaks = freqs_band[start_idx:]

    # If there are fewer than 10 bins, just use all
    n_peaks = min(10, len(amps_for_peaks))

    # Get indices of the n_peaks largest amplitudes
    peak_indices = np.argpartition(-amps_for_peaks, n_peaks - 1)[:n_peaks]
    # Sort those peaks by amplitude descending
    peak_indices = peak_indices[np.argsort(-amps_for_peaks[peak_indices])]

    print("\nTop 10 frequencies in 0–5000 Hz (by amplitude):")
    for i, idx in enumerate(peak_indices):
        f = freqs_for_peaks[idx]
        a = amps_for_peaks[idx]
        print(f"{i+1:2d}: {f:9.2f} Hz, amplitude = {a:.6g} V")

    # 8. Plot amplitude spectrum 0–5000 Hz
    plt.figure()
    plt.plot(freqs_band, amps_band)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title("Amplitude Spectrum (0–5000 Hz, Hann window)")
    plt.grid(True)
    plt.xlim(0, FMAX)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

