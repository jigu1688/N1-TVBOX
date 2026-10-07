import struct
import os

with open('N1_mod_by_webpad_v2.2_20180920.img', 'rb') as f:
    data = f.read()

# Amlogic package contains partitions with headers
pos = 0
found = []
while True:
    idx = data.find(b'ANDROID!', pos)
    if idx == -1: break
    print(f"Found ANDROID! header at {idx}")
    found.append(idx)
    pos = idx + 8

for idx in found:
    hdr = data[idx:idx+2048]
    k_size = struct.unpack_from('<I', hdr, 8)[0]
    r_size = struct.unpack_from('<I', hdr, 16)[0]
    print(f"Kernel size: {k_size}, Ramdisk size: {r_size}")
    cmdline = hdr[64:576].split(b'\0')[0]
    print("Cmdline:", cmdline)
