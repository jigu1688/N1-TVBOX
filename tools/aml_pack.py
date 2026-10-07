import struct
import zlib
import hashlib
import os
import sys

def update_verify_file(part_path, verify_path):
    if not os.path.exists(part_path):
        return
    print(f"[*] Updating {verify_path} from {part_path}...")
    with open(part_path, 'rb') as f:
        sha1 = hashlib.sha1()
        while chunk := f.read(1024 * 1024):
            sha1.update(chunk)
            
    content = f"sha1sum {sha1.hexdigest()}".encode('latin1')
    with open(verify_path, 'wb') as f:
        f.write(content)
    print(f"    -> {content.decode('latin1')}")

def pack_aml_image(items_dir, output_img_path):
    print(f"[*] Packaging Amlogic Upgrade Image to {output_img_path}...")
    
    # 1. Update all .VERIFY files
    verify_mappings = [
        ("_aml_dtb.PARTITION", "_aml_dtb.VERIFY"),
        ("boot.PARTITION", "boot.VERIFY"),
        ("bootloader.PARTITION", "bootloader.VERIFY"),
        ("data.PARTITION", "data.VERIFY"),
        ("logo.PARTITION", "logo.VERIFY"),
        ("recovery.PARTITION", "recovery.VERIFY"),
        ("system.PARTITION", "system.VERIFY")
    ]
    for part, vf in verify_mappings:
        p_path = os.path.join(items_dir, part)
        v_path = os.path.join(items_dir, vf)
        if os.path.exists(p_path):
            update_verify_file(p_path, v_path)
            
    partition_tail = b'\x01\x00\x00\x00' + b'\x00' * 28
    dtb_tail = b'\x00\x00\x00\x00\x01\x00\x02\x00' + b'\x00' * 24
    zero_tail = b'\x00' * 32
    
    # Complete 21-item TOC definition matching Amlogic Webpad standard
    items_def = [
        (0, 0, "USB", "DDR", "usb_DDR.bin", None, zero_tail),
        (1, 0, "USB", "UBOOT", "usb_UBOOT.bin", None, zero_tail),
        (2, 0, "PARTITION", "_aml_dtb", "_aml_dtb.PARTITION", None, partition_tail),
        (3, 0, "VERIFY", "_aml_dtb", "_aml_dtb.VERIFY", None, zero_tail),
        (4, 0, "UBOOT", "aml_sdc_burn", "uboot_aml_sdc_burn.bin", None, zero_tail),
        (5, 0, "ini", "aml_sdc_burn", "aml_sdc_burn.ini", None, zero_tail),
        (6, 0, "PARTITION", "boot", "boot.PARTITION", None, partition_tail),
        (7, 0, "VERIFY", "boot", "boot.VERIFY", None, zero_tail),
        (8, 0, "PARTITION", "bootloader", "bootloader.PARTITION", None, partition_tail),
        (9, 0, "VERIFY", "bootloader", "bootloader.VERIFY", None, zero_tail),
        (10, 254, "PARTITION", "data", "data.PARTITION", None, partition_tail),
        (11, 0, "VERIFY", "data", "data.VERIFY", None, zero_tail),
        (12, 0, "PARTITION", "logo", "logo.PARTITION", None, partition_tail),
        (13, 0, "VERIFY", "logo", "logo.VERIFY", None, zero_tail),
        (14, 0, "xml", "manifest", "manifest.xml", None, zero_tail),
        (15, 0, "dtb", "meson1", "meson1.dtb", 2, dtb_tail),
        (16, 0, "conf", "platform", "platform.conf", None, zero_tail),
        (17, 0, "PARTITION", "recovery", "recovery.PARTITION", None, partition_tail),
        (18, 0, "VERIFY", "recovery", "recovery.VERIFY", None, zero_tail),
        (19, 254, "PARTITION", "system", "system.PARTITION", None, partition_tail),
        (20, 0, "VERIFY", "system", "system.VERIFY", None, zero_tail)
    ]
    
    item_count = len(items_def)
    magic = 0x27b51956
    version = 2
    item_align = 4
    header_size = 64
    toc_size = item_count * 576
    payload_start = header_size + toc_size
    if payload_start % item_align != 0:
        payload_start += (item_align - (payload_start % item_align))
        
    toc_entries = []
    current_offset = payload_start
    
    for item_id, img_type, main_type, sub_type, filename, shared_id, tail_bytes in items_def:
        filepath = os.path.join(items_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Required item file missing: {filepath}")
            
        file_size = os.path.getsize(filepath)
        
        if shared_id is not None:
            item_offset = toc_entries[shared_id]['offset']
            item_size = toc_entries[shared_id]['size']
            print(f"  [+] {main_type:<12} / {sub_type:<15} : {filename:<25} (SHARED off={item_offset})")
        else:
            if current_offset % item_align != 0:
                current_offset += (item_align - (current_offset % item_align))
            item_offset = current_offset
            item_size = file_size
            current_offset += file_size
            print(f"  [+] {main_type:<12} / {sub_type:<15} : {filename:<25} ({file_size / 1024 / 1024:.2f} MB, img_type={img_type})")
            
        toc_entries.append({
            'id': item_id,
            'img_type': img_type,
            'item_offset_in_toc': 0,
            'offset': item_offset,
            'size': item_size,
            'main_type': main_type,
            'sub_type': sub_type,
            'filepath': filepath,
            'shared_id': shared_id,
            'tail_bytes': tail_bytes
        })
        
    total_file_size = current_offset
    print(f"[*] Total package size: {total_file_size / 1024 / 1024:.2f} MB ({total_file_size} bytes)")
    
    with open(output_img_path, 'wb') as f_out:
        hdr_data = bytearray(64)
        struct.pack_into('<III', hdr_data, 0, 0, version, magic)
        struct.pack_into('<Q', hdr_data, 12, total_file_size)
        struct.pack_into('<II', hdr_data, 20, item_align, item_count)
        f_out.write(hdr_data)
        
        for e in toc_entries:
            entry_bytes = bytearray(576)
            struct.pack_into('<II', entry_bytes, 0, e['id'], e['img_type'])
            struct.pack_into('<Q', entry_bytes, 8, e['item_offset_in_toc'])
            struct.pack_into('<Q', entry_bytes, 16, e['offset'])
            struct.pack_into('<Q', entry_bytes, 24, e['size'])
            
            main_b = e['main_type'].encode('latin1')[:255]
            entry_bytes[32:32+len(main_b)] = main_b
            
            sub_b = e['sub_type'].encode('latin1')[:255]
            entry_bytes[288:288+len(sub_b)] = sub_b
            
            entry_bytes[544:576] = e['tail_bytes']
            f_out.write(entry_bytes)
            
        pad_len = payload_start - f_out.tell()
        if pad_len > 0:
            f_out.write(b'\x00' * pad_len)
            
        for e in toc_entries:
            if e['shared_id'] is not None:
                continue
            curr_pos = f_out.tell()
            if curr_pos < e['offset']:
                f_out.write(b'\x00' * (e['offset'] - curr_pos))
                
            with open(e['filepath'], 'rb') as f_in:
                while chunk := f_in.read(1024 * 1024):
                    f_out.write(chunk)
                    
    print("[*] Calculating AmlCRC checksum...")
    with open(output_img_path, 'r+b') as f:
        f.seek(4)
        c = 0
        while chunk := f.read(1024 * 1024):
            c = zlib.crc32(chunk, c)
        final_crc = (~c) & 0xffffffff
        print(f"[+] Computed AmlCRC: {hex(final_crc)}")
        f.seek(0)
        f.write(struct.pack('<I', final_crc))
        
    print(f"[+] Output ready: {output_img_path}")

if __name__ == '__main__':
    items_dir = sys.argv[1] if len(sys.argv) > 1 else 'build_rom/package'
    out_img = sys.argv[2] if len(sys.argv) > 2 else 'N1_NextGen_TV_v3.1_Super.img'
    pack_aml_image(items_dir, out_img)
