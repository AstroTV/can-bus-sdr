from rtlsdr import RtlSdr,limit_time
import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess
from threading import Thread

def sdr_setup():
    sdr = RtlSdr() 
    sdr.sample_rate = 2.4e6 # Hz
    sdr.center_freq = 15e6   # Hz
    sdr.set_direct_sampling('q')
    sdr.set_agc_mode(True)
    return sdr

def write_to_file_thread(samples,starttime,endtime,):
    n_samples = len(samples)
    with open(sdr.filename,'a') as file:
        db_values = 20 * np.log10(np.abs(samples))
        time_axis = np.linspace(starttime,endtime, n_samples + 1)[1:]
        for i in range(n_samples):
            file.write(f"{time_axis[i]};{db_values[i]}\n")

@limit_time(1)
def write_samples_to_file(samples, sdr):
    endtime = time.time()
    file_write_thread = Thread(target=write_to_file_thread, args=[samples, sdr.starttime, endtime])
    file_write_thread.start()
    sdr.starttime = endtime
    

if __name__ == "__main__":
    filename = f"{time.time()}-sdr-samples.csv"
    sdr = sdr_setup()
    # Get rid of initial empty samples
    x = sdr.read_samples(2048) 
    sdr.filename = filename
    sdr.starttime = time.time()
    candump_file = open(f"{sdr.starttime}-candump.txt", "w")
    p_candump =subprocess.Popen(["candump", "-ta","can1"], stdout=candump_file) 
    p_cangen = subprocess.Popen(["cangen","can0"])
    # Star async reading
    sdr.read_samples_async(write_samples_to_file,1024,sdr)
    sdr.close()
    p_cangen.terminate()
    p_candump.terminate()
    candump_file.close()
    