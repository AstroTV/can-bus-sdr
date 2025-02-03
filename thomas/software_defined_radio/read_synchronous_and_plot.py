from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

sdr = RtlSdr()
sdr.sample_rate = 2.4e6 # Hz
sdr.center_freq = 15e6   # Hz
sdr.set_direct_sampling('q')
sdr.set_agc_mode(True)

number_of_samples = 2048 * 1024
print("Discarding intial 2048 samples as they are empty")
x = sdr.read_samples(2048) # get rid of initial empty samples
print(f"Reading {number_of_samples} samples")
x = sdr.read_samples(number_of_samples)
db_values = 20 * np.log10(np.abs(x))
time_axis = np.linspace(0,number_of_samples/sdr.sample_rate, int(number_of_samples))

plt.plot(time_axis/0.001, db_values)
# plt.plot(time_axis/0.001, x.imag)
# plt.legend(["I", "Q"])
plt.xlabel("Time [ms]")
plt.ylabel("A [dB]")
plt.ylim(-50, 0)
plt.savefig("rtlsdr-gain.svg", bbox_inches='tight')
plt.show()

sdr.close()
