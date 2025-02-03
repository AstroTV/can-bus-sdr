with open('S1.BIN','rb') as file:
    rawdata = file.read()
    print(f"Read {len(rawdata)} bytes")
    data = []
    # Discard first 
    for idx in range(4,len(rawdata),2):
        # take 2 bytes and convert them to signed integer using "little-endian"
        point = int().from_bytes([rawdata[idx], rawdata[idx+1]],'little',signed=True)
        data.append(point/4096)  # data as 12 bit