import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt


def plot(values, time_axis, filename, show=False):
    plt.plot(time_axis, values)
    plt.xlabel("Time [ms]")
    plt.ylabel("A [dB]")
    if show == True:
        plt.show()
    plt.savefig(f"plots/{filename}")
    plt.clf()
    plt.close()

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python process_csv.py <example.csv>")
        exit(1)
    filename = sys.argv[1]
    ds = pd.read_csv(filename,delimiter=';')
    values = ds['Amplitude'].to_numpy()
    timestamps = ds['Timestamp'].to_numpy()
    median = np.median(values)
    no_signal_counter = 0
    start_of_frame_indices = []
    end_of_frame_indices = []
    frame_active = False
    for i in range(len(values)):
        if values[i] < -18:
            no_signal_counter += 1
            if frame_active and no_signal_counter > 100:
                frame_active = False
                end_of_frame_indices.append(i-100)
        else:
            no_signal_counter = 0
            if frame_active == False:
                frame_active = True
                start_of_frame_indices.append(i)
            
    
    print(f"Found {len(start_of_frame_indices)} frames.")
    for i in range(len(start_of_frame_indices)):
                   # Add a bit of buffer before and after the frame to increase visibility in the plot
                   start = start_of_frame_indices[i]-20
                   stop = end_of_frame_indices[i]+20
                   plot(values[start:stop],timestamps[start:stop], f"frame-{i}.png")

if __name__ == "__main__":
    main()