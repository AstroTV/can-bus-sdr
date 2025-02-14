import can
import pandas as pd
import sys
import os
import time

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
    can_frame_df = pd.read_csv(path, nrows=0)
    can_frame = can_frame_df.columns[1]
    print(can_frame)
    with can.Bus(interface='socketcan', channel='can0',) as bus:
        id = int(can_frame.split(":")[0][3:],base=16)
        payload = bytes.fromhex(can_frame.split(":")[1])
        msg = can.Message(arbitration_id=id, data=payload)
        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")

        except can.CanError:
            print("Message NOT sent")
    time.sleep(0.01)