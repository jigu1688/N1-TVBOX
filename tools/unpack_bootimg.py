import struct
import os
import gzip

BOOT_MAGIC = b"ANDROID!"

def unpack_bootimg(boot_path, out_dir):
    print(f"[*] Unpacking boot image {boot_path} to {out_dir}...")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with open(boot_path, 'rb') as f:
        hdr = f.read(2048)
        if not hdr.startswith(BOOT_MAGIC):
            raise ValueError("Not a valid Android boot image")
            
        (magic, kernel_size, kernel_addr, ramdisk_size, ramdisk_addr,
         second_size, second_addr, tags_addr, page_size, dt_size,
         os_version) = struct.unpack('<8sIIIIIIIIII', hdr[:48])
         
        name = hdr[48:64].split(b'\x00')[0].decode('utf-8', errors='ignore')
        cmdline = hdr[64:576].split(b'\x00')[0].decode('utf-8', errors='ignore')
        extra_cmdline = hdr[608:1632].split(b'\x00')[0].decode('utf-8', errors='ignore')
        full_cmdline = (cmdline + " " + extra_cmdline).strip()
        
        print(f"[+] Boot Info:")
        print(f"    Page Size   : {page_size}")
        print(f"    Kernel Size : {kernel_size} (addr: {hex(kernel_addr)})")
        print(f"    Ramdisk Size: {ramdisk_size} (addr: {hex(ramdisk_addr)})")
        print(f"    DTB Size    : {dt_size}")
        print(f"    Cmdline     : {full_cmdline[:100]}...")
        
        # Save header metadata
        with open(os.path.join(out_dir, "boot_info.txt"), "w", encoding="utf-8") as info_f:
            info_f.write(f"kernel_size={kernel_size}\nkernel_addr={hex(kernel_addr)}\n")
            info_f.write(f"ramdisk_size={ramdisk_size}\nramdisk_addr={hex(ramdisk_addr)}\n")
            info_f.write(f"second_size={second_size}\nsecond_addr={hex(second_addr)}\n")
            info_f.write(f"tags_addr={hex(tags_addr)}\npage_size={page_size}\n")
            info_f.write(f"dt_size={dt_size}\nos_version={os_version}\n")
            info_f.write(f"name={name}\ncmdline={full_cmdline}\n")
            
        def get_page_offset(pages_count):
            return pages_count * page_size
            
        def pages_needed(size):
            return (size + page_size - 1) // page_size
            
        # Pages layout:
        # 1 page header
        # kernel pages
        # ramdisk pages
        # second pages
        # dt pages
        
        offset = page_size
        
        # 1. Kernel
        f.seek(offset)
        kernel_data = f.read(kernel_size)
        with open(os.path.join(out_dir, "kernel"), "wb") as kf:
            kf.write(kernel_data)
        offset += pages_needed(kernel_size) * page_size
        
        # 2. Ramdisk
        f.seek(offset)
        ramdisk_data = f.read(ramdisk_size)
        with open(os.path.join(out_dir, "ramdisk.cpio.gz"), "wb") as rf:
            rf.write(ramdisk_data)
        offset += pages_needed(ramdisk_size) * page_size
        
        # 3. Second
        if second_size > 0:
            f.seek(offset)
            second_data = f.read(second_size)
            with open(os.path.join(out_dir, "second.bin"), "wb") as sf:
                sf.write(second_data)
            offset += pages_needed(second_size) * page_size
            
        # 4. DTB
        if dt_size > 0:
            f.seek(offset)
            dt_data = f.read(dt_size)
            with open(os.path.join(out_dir, "dtb.img"), "wb") as df:
                df.write(dt_data)
                
    print("[+] boot.PARTITION unpacked successfully!")
    
    # Try decompressing ramdisk
    ramdisk_dir = os.path.join(out_dir, "ramdisk_root")
    if not os.path.exists(ramdisk_dir):
        os.makedirs(ramdisk_dir)
        
    try:
        with gzip.open(os.path.join(out_dir, "ramdisk.cpio.gz"), 'rb') as gz_in:
            with open(os.path.join(out_dir, "ramdisk.cpio"), 'wb') as cpio_out:
                cpio_out.write(gz_in.read())
        print(f"[+] Ramdisk un-gzipped to {out_dir}/ramdisk.cpio")
    except Exception as e:
        print(f"[!] Warning: Gzip decompress failed: {e}")

if __name__ == '__main__':
    unpack_bootimg('extracted_aml/boot.PARTITION', 'extracted_aml/boot_unpacked')
