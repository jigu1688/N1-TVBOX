import os
import struct
import shutil

def unpack_aml_image(img_path, output_dir):
    print(f"[*] Opening {img_path}...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(img_path, 'rb') as f:
        hdr = f.read(64)
        magic, version, magic2, crc, flags, item_align, item_count = struct.unpack('<IIIIIII', hdr[:28])
        print(f"[+] Magic: {hex(magic)}, Version: {version}, Item Count: {item_count}, Align: {item_align}")
        
        entries = []
        for i in range(item_count):
            entry_raw = f.read(576)
            item_id, item_flag = struct.unpack('<II', entry_raw[:8])
            item_offset, item_size = struct.unpack('<QQ', entry_raw[16:32])
            main_type = entry_raw[32:288].rstrip(b'\x00').decode('latin1')
            sub_type = entry_raw[288:544].rstrip(b'\x00').decode('latin1')
            entries.append({
                'index': i,
                'id': item_id,
                'flag': item_flag,
                'offset': item_offset,
                'size': item_size,
                'main_type': main_type,
                'sub_type': sub_type,
                'entry_raw': entry_raw
            })
            
        print(f"[*] Extracting {len(entries)} items to {output_dir}...")
        
        # Save image info/table
        with open(os.path.join(output_dir, "aml_image_info.txt"), "w", encoding="utf-8") as info_f:
            info_f.write(f"magic={hex(magic)}\nversion={version}\nmagic2={hex(magic2)}\ncrc={hex(crc)}\n")
            info_f.write(f"item_align={item_align}\nitem_count={item_count}\n\n")
            for e in entries:
                info_f.write(f"item_{e['index']}: id={e['id']}, offset={e['offset']}, size={e['size']}, main_type={e['main_type']}, sub_type={e['sub_type']}\n")
                
        for e in entries:
            # Generate sensible filenames
            # If main_type is PARTITION, sub_type is partition name e.g. system.PARTITION or system.img
            filename = f"{e['main_type']}_{e['sub_type']}.bin"
            if e['main_type'] == 'PARTITION':
                filename = f"{e['sub_type']}.PARTITION"
            elif e['main_type'] == 'VERIFY':
                filename = f"{e['sub_type']}.VERIFY"
            elif e['main_type'] == 'USB':
                filename = f"usb_{e['sub_type']}.bin"
            elif e['main_type'] == 'UBOOT':
                filename = f"uboot_{e['sub_type']}.bin"
            elif e['main_type'] == 'ini':
                filename = f"{e['sub_type']}.ini"
            elif e['main_type'] == 'xml':
                filename = f"{e['sub_type']}.xml"
            elif e['main_type'] == 'conf':
                filename = f"{e['sub_type']}.conf"
            elif e['main_type'] == 'dtb':
                filename = f"{e['sub_type']}.dtb"
                
            e['extracted_filename'] = filename
            out_file_path = os.path.join(output_dir, filename)
            
            f.seek(e['offset'])
            data = f.read(e['size'])
            with open(out_file_path, 'wb') as out_f:
                out_f.write(data)
                
            print(f"  [>] Extracted {filename:<25} ({e['size'] / 1024 / 1024:.2f} MB, {e['size']} bytes)")

    print("[+] Unpack completed successfully!")

if __name__ == '__main__':
    unpack_aml_image('aml_upgrade_package.img', 'extracted_aml')
