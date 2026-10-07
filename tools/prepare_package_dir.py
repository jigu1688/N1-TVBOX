import os
import shutil

def prepare_package(src_dir, dst_dir):
    print(f"[*] Preparing package files in {dst_dir}...")
    os.makedirs(dst_dir, exist_ok=True)
    
    files = [
        "usb_DDR.bin",
        "usb_UBOOT.bin",
        "_aml_dtb.PARTITION",
        "_aml_dtb.VERIFY",
        "uboot_aml_sdc_burn.bin",
        "aml_sdc_burn.ini",
        "boot.PARTITION",
        "boot.VERIFY",
        "bootloader.PARTITION",
        "bootloader.VERIFY",
        "logo.PARTITION",
        "logo.VERIFY",
        "manifest.xml",
        "meson1.dtb",
        "platform.conf",
        "recovery.PARTITION",
        "recovery.VERIFY",
        "system.VERIFY"
    ]
    
    for f in files:
        src_path = os.path.join(src_dir, f)
        dst_path = os.path.join(dst_dir, f)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  [+] Copied {f}")
        else:
            print(f"  [!] Missing {f} in {src_dir}")
            
    print("[+] Package directory prepared!")

if __name__ == '__main__':
    prepare_package('extracted_aml', 'build_rom/package')
