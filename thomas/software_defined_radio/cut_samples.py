import pandas as pd
import sys
import matplotlib.pyplot as plt
import os

def compute_crc(bits):
    poly = 0x4599
    crc = 0x0000
    for bit in bits:
        crc = (crc << 1) | int(bit)
        if crc & 0x8000:
            crc ^= poly
        crc &= 0x7FFF
    return crc

def bit_stuff(bits):
    stuffed = []
    count = 0
    last = None
    for bit in bits:
        stuffed.append(bit)
        if bit == last:
            count +=1
            if count == 5:
                stuffed.append('0' if bit == '1' else '1')
                count = 0
        else:
            count = 1
            last = bit
    return stuffed

def frame_to_bits(id, payload):
    length = len(payload)
    # Base frame: SOF, ID, Control, Data
    base = [
        '0',  # SOF
        f"{id:011b}",  # 11-bit ID (MSB first)
        '0' + '0' + '0' + f"{length:04b}",  # Control field
        ''.join(f"{b:08b}" for b in payload)  # Data bytes
    ]
    bits = ''.join(base)
    
    # Compute CRC and append
    crc = compute_crc(bits)
    bits += f"{crc:015b}"
    
    # Bit stuffing
    stuffed = bit_stuff(bits)
    
    # Frame end components
    return stuffed + ['1']*3 + ['1']*7  # CRC delim + ACK + EOF

if len(sys.argv) != 2:
    print("Usage: python cut_samples.py <FOLDER WITH CSV>")
    exit(1)

folder = sys.argv[1]
if not os.path.isdir(folder):
    print("Usage: python cut_samples.py <FOLDER WITH CSV>")
    exit(2)

paths = os.listdir(folder)

for path in paths:
    path = folder + "/" + path

    # Get the CAN Frame from the first row of the CSV file
    df = pd.read_csv(path, delimiter=";", nrows=0)
    can_frame = df.columns[1]
    can_id = int(can_frame.split(":")[0][3:],base=16)
    can_payload = bytes.fromhex(can_frame.split(":")[1])
    can_bits = frame_to_bits(can_id, can_payload)
    bitsstring = "".join(can_bits)

    # Load the data from CSV file
    df = pd.read_csv(path, delimiter=';', skiprows=[0])

    # Calculate the mean and standard deviation of the noise
    noise_mean = df['Amplitude'].mean()
    noise_std = df['Amplitude'].std()

    print(f"Mean: {noise_mean}, Stdev: {noise_std}")

    # Define a threshold to detect the signal
    threshold = noise_mean + 4 * noise_std

    # Find the start and end of the signal with gaps
    signal_indices = df[df['Amplitude'] > threshold].index

    if not signal_indices.empty:
        signal_start = signal_indices[0]
        signal_end = signal_indices[-1]
        # Add a buffer before and after the signal
        signal_start = max(0,signal_start - 50)
        signal_end = min(len(df['Amplitude']), signal_end + 50)

        print(f"Signal starts at index: {signal_start}")
        print(f"Signal ends at index: {signal_end}")
        frame_len = signal_end - signal_start
        if frame_len < 340 or frame_len > 800:
            print(f"Frame length ({frame_len}) not in sanity range - skipping")
            continue
        plt.plot(df['Amplitude'][signal_start:signal_end])
        plt.title(f"0x{can_id:x} {can_payload.hex()}\n {bitsstring}")
        plt.xlabel("Time [ms]")
        plt.ylabel("A [dB]")
        plt.show()
        df["Timestamp"].drop()
        df["Amplitude"] = df['Amplitude'][signal_start:signal_end]

        df.to_csv("cut/" + path)
        
    else:
        print("No signal detected above the threshold.")

