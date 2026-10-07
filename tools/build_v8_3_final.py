import os
import subprocess
import shutil

def build_v8_3_final():
    print("="*60)
    print("  Packaging N1 NextGen TV v8.3 Final Master (0 Bloat, 0 Crypt Error)")
    print("="*60)
    
    out_img = "N1_NextGen_TV_v8.3_FinalMaster.img"
    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img}")

if __name__ == '__main__':
    build_v8_3_final()
