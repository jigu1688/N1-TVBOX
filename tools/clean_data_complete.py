import os
import subprocess
import shutil

def clean_data_complete():
    print("="*60)
    print("  Complete Data Partition Deep Cleaning & Geometry Fix")
    print("="*60)
    
    # 1. Reset from extracted_webpad/data.raw.img
    shutil.copy2('extracted_webpad/data.raw.img', 'build_rom/data.raw.img')
    
    # 2. Fix physical size to match superblock exactly (1344768 * 4096)
    with open('build_rom/data.raw.img', 'r+b') as f:
        f.truncate(1344768 * 4096)
        
    # 3. List all files inside /app using debugfs
    res = subprocess.run('wsl debugfs -R "ls -l /app" build_rom/data.raw.img', shell=True, capture_output=True, text=True)
    dirs = []
    for line in res.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 9:
            name = parts[8]
            if name not in ('.', '..', 'lost+found'):
                dirs.append(name)
                
    print(f"[*] Found {len(dirs)} app directories to wipe: {dirs}")
    
    cmds = []
    for d in dirs:
        # try deleting potential files in arm, arm64, oat, etc.
        for arch in ['arm', 'arm64']:
            cmds.append(f"rm /app/{d}/oat/{arch}/base.odex")
            cmds.append(f"rm /app/{d}/oat/{arch}/base.vdex")
            cmds.append(f"rmdir /app/{d}/oat/{arch}")
            
            # also check lib
            for l in ['libffmpeg.so', 'libavcodec.so', 'libloader.mx.so', 'libmxass.so', 'libmxutil.so', 'libmxvp.so', 'libswresample.so', 'libswscale.so']:
                cmds.append(f"rm /app/{d}/lib/{arch}/{l}")
            cmds.append(f"rmdir /app/{d}/lib/{arch}")
            
        cmds.append(f"rm /app/{d}/base.apk")
        cmds.append(f"rmdir /app/{d}/oat")
        cmds.append(f"rmdir /app/{d}/lib")
        cmds.append(f"rmdir /app/{d}")
        
    with open("tools/wipe_apps_debugfs.txt", "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Executing {len(cmds)} deletion commands on data.raw.img...")
    subprocess.run("wsl debugfs -w -f tools/wipe_apps_debugfs.txt build_rom/data.raw.img", shell=True)
    
    # 4. Run e2fsck verification
    print("[*] Running e2fsck on data.raw.img...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/data.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on data.raw.img!")
        
    # 5. Generate sparse data.PARTITION
    print("[*] Generating Android Sparse data.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/data.raw.img build_rom/package/data.PARTITION", shell=True, check=True)
    print("[+] data.PARTITION successfully generated and 100% verified!")

if __name__ == '__main__':
    clean_data_complete()
