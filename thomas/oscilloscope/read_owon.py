### read data from a Peaktech 1337 Oscilloscope (OWON)
import usb.core
import usb.util
from matplotlib import pyplot as plt

dev = usb.core.find(idVendor=0x5345, idProduct=0x1234)
# taken from results of print(dev)
BULK_IN_ENDPOINT = 0x81
BULK_OUT_ENDPOINT = 0x01

if dev is None:
    raise ValueError('Device not found')
else:
    print(dev)
    dev.set_configuration()

def send(cmd):
    dev.write(BULK_OUT_ENDPOINT,cmd)
    result = (dev.read(BULK_IN_ENDPOINT,604,1000))
    print(len(result))
    return result

def get_id():
    return send('*IDN?').tobytes().decode('utf-8')

def get_data(ch):
    # first 4 bytes indicate the number of data bytes following
    rawdata = send(':DATA:WAVE:SCREen:CH{}?'.format(ch))
    print(f"Received {len(rawdata)} bytes")
    data = []
    for idx in range(4,len(rawdata),2):
        # take 2 bytes and convert them to signed integer using "little-endian"
        point = int().from_bytes([rawdata[idx], rawdata[idx+1]],'little',signed=True)
        data.append(point/4096)  # data as 12 bit
    return data

def get_header():
    # first 4 bytes indicate the number of data bytes following
    header = send(':DATA:WAVE:SCREen:HEAD?')
    header = header[4:].tobytes().decode('utf-8')
    return header

def save_data(ffname,data):
    f = open(ffname,'w')
    f.write('\n'.join(map(str, data)))
    f.close
    
def print_data(data):

    # Create the plot
    plt.plot(data)

    # Add titles and labels
    plt.title('OWON HDS2202S Plot')
    plt.xlabel('t[s]')
    plt.ylabel('V[mV]')

    # Show the plot
    plt.show()

# print(get_id())
header = get_header()
print(header)
data = get_data(1)
print(f"Received {len(data)} floats")
save_data('Osci.dat',data)
print_data(data)
### end of code
