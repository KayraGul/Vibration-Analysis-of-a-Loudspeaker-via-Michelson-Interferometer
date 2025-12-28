import serial
import numpy as np
import time
import matplotlib.pyplot as plt

# ===== CONFIGURATION =====
PORT = "COM7"         
BAUD = 2000000
OUTFILE = "data.csv"
DURATION_S = 10.0     
# =========================

def decode_safe_protocol(raw_bytes):
    """
    Decodes the 7-bit 'Safe Protocol'.
    Format:
      High Byte: 1aaaaaaa (MSB set)
      Low Byte:  0bbbbbbb (MSB clear)
    Value = (aaaaaaa << 7) | bbbbbbb
    """
    print(f"Decoding {len(raw_bytes)} bytes...")
    
    # Convert buffer to numpy uint8 array for fast processing
    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    
    # Create output array (max possible size is len/2)
    samples = np.zeros(len(arr) // 2, dtype=np.uint16)
    count = 0
    
    i = 0
    # Loop through the byte array
    while i < len(arr) - 1:
        high = arr[i]
        
        # Check if this is a valid Header Byte (Bit 7 is 1)
        if high & 0x80: 
            low = arr[i+1]
            
            # Check if next is a valid Data Byte (Bit 7 is 0)
            if not (low & 0x80):
                # Reconstruct the 10-bit value
                # (High & 0x7F) strips the flag bit
                val = ((high & 0x7F) << 7) | low
                samples[count] = val
                count += 1
                i += 2 # Move past this pair
                continue
        
        # If we get here, it was a bad byte or sync error. Skip 1 byte.
        i += 1

    print(f"Successfully decoded {count} samples.")
    return samples[:count]

def read_samples():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except serial.SerialException as e:
        print(f"Error: {e}")
        return np.array([], dtype=np.uint16)

    print("Connecting...")
    time.sleep(2)
    ser.reset_input_buffer()
    
    print("Triggering capture...")
    ser.write(b'S')

    raw_data = bytearray()
    start_wall = time.time()
    MAX_TIME = DURATION_S * 1.5
    
    print(f"Streaming for {DURATION_S}s...")

    while True:
        if time.time() - start_wall > MAX_TIME:
            print("Global timeout.")
            break

        waiting = ser.in_waiting
        if waiting > 0:
            chunk = ser.read(waiting)
            raw_data.extend(chunk)
            
            # Check for End Marker (0xFF 0xFF)
            if len(raw_data) >= 2 and raw_data[-1] == 0xFF and raw_data[-2] == 0xFF:
                print("End marker received.")
                raw_data = raw_data[:-2]
                break
        else:
            time.sleep(0.002)

    ser.close()
    
    return decode_safe_protocol(raw_data)

def process_and_plot(samples):
    if len(samples) == 0:
        print("No samples.")
        return

    N = len(samples)
    fs = N / DURATION_S 
    print(f"Sampling Rate: {fs:.2f} Hz")

    t = np.linspace(0, DURATION_S, N, endpoint=False)
    V = samples * (5.0 / 1023.0) 

    # Save to CSV
    print(f"Saving {OUTFILE}...")
    np.savetxt(OUTFILE, np.column_stack([t, V]), delimiter=",", header="time_s,voltage", comments="")

    # Plot
    plt.figure(figsize=(12, 5))
    # Decimate for viewing if large
    step = 1 if N < 10000 else 10
    plt.plot(t[::step], V[::step], lw=0.5)
    
    plt.title(f"Clean ADC Capture: {fs:.0f} Hz")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    data = read_samples()
    process_and_plot(data)