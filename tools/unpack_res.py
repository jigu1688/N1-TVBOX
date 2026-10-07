import struct
import os

def unpack_aml_res(logo_path, out_dir):
    print(f"[*] Unpacking {logo_path} to {out_dir}...")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(logo_path, 'rb') as f:
        hdr = f.read(64)
        crc, ver, magic, size, count, align = struct.unpack('<II8sIII', hdr[:28])
        print(f"[+] Magic: {magic}, Ver: {ver}, Count: {count}, Size: {size}")
        
        # Item format v2 (64 bytes each):
        # Magic (4), Hdr_CRC (4), Size (4), DataOffset (4), Entry (4), NextItemOffset (4), Data_CRC (4), Index (1), Type1 (1), Type2 (1), Type3 (1), Name (32)
        items = []
        for i in range(count):
            item_raw = f.read(64)
            if len(item_raw) < 64: break
            magic_item, hdr_crc, item_sz, data_off, entry, next_off, data_crc, idx, t1, t2, t3 = struct.unpack('<IIIIIIIBBBB', item_raw[:32])
            name = item_raw[32:64].rstrip(b'\x00').decode('latin1', errors='ignore')
            items.append((name, data_off, item_sz))
            print(f"  [{i}] {name:<20} off={data_off:<8} sz={item_sz}")
            
        for name, data_off, item_sz in items:
            f.seek(data_off)
            data = f.read(item_sz)
            with open(os.path.join(out_dir, name), 'wb') as out_f:
                out_f.write(data)

if __name__ == '__main__':
    unpack_aml_res('extracted_aml/logo.PARTITION', 'extracted_aml/logo_unpacked')
    unpack_aml_res('extracted_webpad/logo.PARTITION', 'extracted_webpad/logo_unpacked')
