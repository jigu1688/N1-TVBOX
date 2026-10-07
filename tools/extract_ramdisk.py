import gzip
import io

# Read the boot image ramdisk
with open('N1_mod_by_webpad_v2.2_20180920.img', 'rb') as f:
    f.seek(2068524)
    hdr = f.read(2048)
    # page size is usually 2048
    # kernel starts at 2048, size is 7688192
    k_pages = (7688192 + 2047) // 2048
    f.seek(2068524 + 2048 + k_pages * 2048)
    ramdisk_data = f.read(6500352)

# Check if gzip
if ramdisk_data[:2] == b'\x1f\x8b':
    print("Ramdisk is GZIP!")
    decomp = gzip.decompress(ramdisk_data)
    print("Decompressed size:", len(decomp))
    if b'webpad' in decomp:
        print("webpad found in decompressed ramdisk!")
        idx = decomp.find(b'webpad')
        print(decomp[max(0, idx-100):idx+200])
    if b'daemonsu' in decomp:
        print("daemonsu found in decompressed ramdisk!")
else:
    print("Not gzip, first bytes:", ramdisk_data[:16])
