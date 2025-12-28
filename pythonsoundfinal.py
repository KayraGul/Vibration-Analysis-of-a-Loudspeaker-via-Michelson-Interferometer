import numpy as np
import pandas as pd
import scipy.io.wavfile as wavfile
import scipy.signal as signal

# ===== CONFIGURATION =====
CSV_FILE = "dataasrın3.csv"       # Input file
WAV_FILE = "asrın3.wav"     # Output file

# Human Voice Range usually falls between 85 Hz and 255 Hz (Fundamental)
# but harmonics go up to 3-4 kHz.
CUTOFF_LOW = 100.0           # Remove power hum (50/60Hz) and DC offset

CUTOFF_HIGH = 3000.0        # Telephones cut off at 3.4kHz; 4k is safe for voice.

ORDER = 5                   # Filter steepness (higher = sharper cut)
# =========================

def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Creates a Butterworth bandpass filter.
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    # Safety check for high cut
    if high >= 1.0:
        high = 0.99
        
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def main():
    print(f"Loading {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    t = df["time_s"].values
    V = df["voltage"].values

    # 1. Calculate precise Sampling Rate (fs)
    # We use the average time difference between samples
    dt = np.mean(np.diff(t))
    fs = 1.0 / dt
    print(f"Detected Sampling Rate: {fs:.2f} Hz")

    # 2. Check Nyquist Limits
    if CUTOFF_HIGH > fs / 2:
        print(f"Warning: High cutoff ({CUTOFF_HIGH} Hz) is above Nyquist ({fs/2:.0f} Hz).")
        print(f"Clamping high cutoff to {fs/2 * 0.95:.0f} Hz.")
        real_high = fs / 2 * 0.95
    else:
        real_high = CUTOFF_HIGH

    # 3. Apply Butterworth Bandpass Filter
    # 'filtfilt' applies the filter forward and backward to ensure 
    # zero phase shift (audio doesn't get "smeared" in time).
    print(f"Filtering ({CUTOFF_LOW} Hz - {real_high} Hz)...")
    b, a = butter_bandpass(CUTOFF_LOW, real_high, fs, ORDER)
    V_filtered = signal.filtfilt(b, a, V)

    # 4. Normalize to -1.0 to 1.0 range
    # This maximizes volume without clipping
    max_val = np.max(np.abs(V_filtered))
    if max_val == 0:
        print("Error: Signal is silent after filtering.")
        return

    # Normalize to roughly 90% volume (-3dB)
    V_norm = V_filtered / max_val * 0.9

    # 5. Convert to 16-bit PCM Integer
    audio_int16 = (V_norm * 32767).astype(np.int16)

    # 6. Save WAV file
    # We cast fs to int because WAV standard requires integer rates
    print(f"Saving {WAV_FILE}...")
    wavfile.write(WAV_FILE, int(fs), audio_int16)
    print("Done! You can now play the file.")

if __name__ == "__main__":
    main()