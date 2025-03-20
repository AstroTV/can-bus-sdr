def new_crc(bits:str, poly = 0xc599) -> int:
    data_bytes = int(bits, 2).to_bytes((len(bits) + 7) // 8, 'big')
    crc = 0
    for byte in data_bytes:
        crc ^= byte << 7
        for _ in range(8):
            crc <<= 1
            if crc & 0x8000:
                crc ^= poly

    return crc & 0x7fff

def bit_stuff(bits:str) -> list[str]:
    stuffed = []
    for bit in bits:
        if len(stuffed) > 4:
            if stuffed[-5:] == ['0','0','0','0','0']:
                stuffed.append('1')
            elif stuffed[-5:] == ['1','1','1','1','1']:
                stuffed.append('0')
        stuffed.append(bit)
    return stuffed

def frame_to_bits(id:int, payload:bytes) -> str:
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
    crc = new_crc(bits)
    bits += f"{crc:015b}"
    # Bit stuffing
    stuffed = bit_stuff(bits)
    
    # Frame end components
    stuffed += ['1'] + ['0'] + ['1'] + ['1']*7 + ['1']*3  # CRC delim + ACK + EOF + IFS
    result = "".join(stuffed)
    return result

#id = 0x24
#payload = b'\x0c\xcc\x9d\x2d\xd5\x73\x50\xdb'
#print(frame_to_bits(id, payload))
result = new_crc("0000000000001100000000000010010000010000000110011001100100111010010110111010101011100110101000011011011")
print(f"{result:b}")