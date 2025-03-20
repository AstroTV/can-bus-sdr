import crc

payload = "00000010010000010000000110011001100100111010010110111010101011100110101000011011011"
# output = int("110111100000011",base=2)
output = int("100011011110111",base=2)

possible_polys = []
for poly in range(0x0, 0xFFFF):
    result = crc.new_crc(payload, poly=poly)
    if result == output:
        print(f"Found poly 0x{poly:4x}")
        possible_polys.append(poly)