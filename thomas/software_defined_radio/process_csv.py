import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import os


def plot(values, time_axis, filename, show=False):
    plt.plot(time_axis, values)
    plt.xlabel("Time [ms]")
    plt.ylabel("A [dB]")
    if show == True:
        plt.show()
    plt.savefig(f"plots/{filename}")
    plt.clf()
    plt.close()

def export(values, time_axis, filename):
     with open(filename, "w") as file:
          file.write("Timestamp;Amplitude\n")
          for i in range(len(values)):
               file.write(f"{time_axis[i]};{values[i]}\n")

def main():
    if len(sys.argv) != 2:# or not sys.argv[1].endswith(".csv"):
        print("Usage: python process_csv.py <example.csv>")
        exit(1)
    filenames = []
    if os.path.isdir(sys.argv[1]):
         filenames = [sys.argv[1] + "/" + file for file in os.listdir(sys.argv[1]) if file.endswith(".csv")]
    elif sys.argv[1].endswith(".csv"):
        filenames = sys.argv[1]
    
    for filename in filenames:
        ds = pd.read_csv(filename,delimiter=';', skiprows=[0])
        values = ds['Amplitude'].to_numpy()
        timestamps = ds['Timestamp'].to_numpy()
        median = np.median(values)
        plot(values,timestamps, filename.split("/")[-1][:-3] + "png")
    exit(0)
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
                   export(values[start:stop],timestamps[start:stop], f"frame-{i}.csv")

if __name__ == "__main__":
    main()