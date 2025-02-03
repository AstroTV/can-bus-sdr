from scapy.all import *
from bitstring import BitArray
load_layer("can")

# Create a CAN frame
frame = CAN(identifier=0x123, data=b'\x01\x02\x03\x04\x05\x06\x07\x08')

# Convert to bitwise form
bitwise_frame = raw(frame)
print(bitwise_frame)
print(BitArray(bitwise_frame).bin)