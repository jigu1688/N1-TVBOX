import subprocess
import os
import shutil

def clean_data_partition():
    print("[*] Creating 100% Pure Clean data.PARTITION...")
    src_data = 'extracted_webpad/data.raw.img'
    dst_data = 'build_rom/data.raw.img'
    shutil.copy2(src_data, dst_data)
    
    # Debugfs commands to delete all outdated third party apps from data
    cmds = [
        "rm /app/com.fanshi.tvbrowser-1/base.apk",
        "rmdir /app/com.fanshi.tvbrowser-1",
        
        "rm /app/com.mxtech.videoplayer.pro-1/base.apk",
        "rmdir /app/com.mxtech.videoplayer.pro-1",
        
        "rm /app/com.pplive.androidxl-1/base.apk",
        "rmdir /app/com.pplive.androidxl-1",
        
        "rm /app/com.speedsoftware.rootexplorer-1/base.apk",
        "rmdir /app/com.speedsoftware.rootexplorer-1",
        
        "rm /app/com.sumavision.ivideoforstb-1/base.apk",
        "rmdir /app/com.sumavision.ivideoforstb-1",
        
        "rm /app/com.tcl.gitv-1/base.apk",
        "rmdir /app/com.tcl.gitv-1",
        
        "rm /app/com.xctv2018.mytv-1/base.apk",
        "rmdir /app/com.xctv2018.mytv-1",
        
        "rm /app/dpplay.com-1/base.apk",
        "rmdir /app/dpplay.com-1",
        
        "rm /app/fr.petrus.tools.reboot-1/base.apk",
        "rmdir /app/fr.petrus.tools.reboot-1",
        
        "rm /app/jackpal.androidterm-2/base.apk",
        "rmdir /app/jackpal.androidterm-2",
        
        "rmdir /app"
    ]
    
    cmd_file = "tools/debugfs_clean_data.txt"
    with open(cmd_file, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Purging {len(cmds)} data bloatware items via debugfs...")
    subprocess.run(f"wsl debugfs -w -f tools/debugfs_clean_data.txt build_rom/data.raw.img", shell=True, check=True)
    
    # Run e2fsck
    print("[*] Verifying clean data filesystem...")
    subprocess.run("wsl e2fsck -f -y build_rom/data.raw.img", shell=True, check=True)
    
    # Convert to Sparse data.PARTITION
    dst_partition = "build_rom/package/data.PARTITION"
    print(f"[*] Generating sparse {dst_partition}...")
    subprocess.run(f"python tools/img2simg.py build_rom/data.raw.img {dst_partition}", shell=True, check=True)
    print("[+] Successfully created pure clean data.PARTITION!")

if __name__ == '__main__':
    clean_data_partition()
