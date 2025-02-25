import pandas as pd
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python cutprocess_logic_analyser_csv.py <CSV>")
    exit(1)

folder = sys.argv[1]
if not sys.argv[1].endswith('.csv'):
    print("Usage: python process_logic_analyser_csv.py <CSV>")
    exit(2)

# Get the CAN frames fromt he top of the CSV files
can_frames = pd.read_csv("logic_frames.csv")["CAN Frame"]
print(can_frames)

print(f"Found {len(can_frames)} frames")

df = pd.read_csv(sys.argv[1])
print(df)
values = df["Channel 1"].to_numpy()
timestamps = df["Time [s]"].to_numpy()
start = timestamps[0]
end = timestamps[-1]
duration = end - start

length = len(timestamps)

# cutting samples
frames = []
cut_values = [values[0]]
cut_timestamps = [timestamps[0]]
for i in range(1,length):
    if timestamps[i] - cut_timestamps[-1] > 0.009:
        frames.append(list([cut_timestamps,cut_values]))
        cut_values = []
        cut_timestamps = []
        cut_values.append(values[i-1])
        cut_timestamps.append(timestamps[i]-0.000001)
        cut_values.append(values[i])
        cut_timestamps.append(timestamps[i])
    else:
        cut_values.append(values[i])
        cut_timestamps.append(timestamps[i])

# Drop the first frame as it is only '1' bits
frames = frames[1:]

print(f"Found {len(frames)} frames")

for i,frame in enumerate(frames):
    timestamps = frame[0]
    values = frame[1]
    new_values = [values[0]]
    new_timestamps = [timestamps[0]]

    for j in range(1,len(values)):
        # add the last value very shortly before the next one
        new_values.append(values[j-1])
        new_timestamps.append(timestamps[j] - 0.0000001)
        new_values.append(values[j])
        new_timestamps.append(timestamps[j])

    fig = plt.figure(figsize=(16,12))
    plt.plot( new_timestamps, new_values,)
    plt.xlabel("Time [s]")
    plt.ylabel("Logic Value")
    plt.title(can_frames[i])
    path = f"plots/logic/{can_frames[i]}.png"
    plt.savefig(path)
    plt.close()
    del(fig)
