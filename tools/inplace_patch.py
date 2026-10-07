import os
import subprocess
import shutil

def run_inplace_patch():
    print("[*] Starting in-place surgical modification of ext4 system.raw.img...")
    
    # 1. Copy original system.raw.img
    src_raw = 'extracted_webpad/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    
    print(f"[*] Copying {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)
    
    # 2. Build debugfs command list
    cmds = [
        # Remove Provisioning Wizard (prevents infinite setup wizard hang)
        "rm /priv-app/Provision/Provision.apk",
        "rmdir /priv-app/Provision",
        
        # Remove Phicomm Remote Server
        "rm /priv-app/PhiTvRemoteServer/PhiTvRemoteServer.apk",
        "rmdir /priv-app/PhiTvRemoteServer",
        
        # Remove mining and bloatware
        "rm /app/Dig/Dig.apk",
        "rmdir /app/Dig/oat/arm",
        "rmdir /app/Dig/oat",
        "rmdir /app/Dig",
        "rm /app/PhiCalendar/PhiCalendar.apk",
        "rmdir /app/PhiCalendar",
        "rm /app/PhiTvManager/PhiTvManager.apk",
        "rmdir /app/PhiTvManager",
        "rm /app/PhiTvMusic/PhiTvMusic.apk",
        "rmdir /app/PhiTvMusic",
        "rm /app/PhiTvVideoPlayer/PhiTvVideoPlayer.apk",
        "rmdir /app/PhiTvVideoPlayer",
        "rm /app/PhiNasImagePlayer/PhiNasImagePlayer.apk",
        "rmdir /app/PhiNasImagePlayer",
        "rm /app/TvPhotoScreenSaver/TvPhotoScreenSaver.apk",
        "rmdir /app/TvPhotoScreenSaver",
        "rm /app/BasicDreams/BasicDreams.apk",
        "rmdir /app/BasicDreams/oat/arm",
        "rmdir /app/BasicDreams/oat",
        "rmdir /app/BasicDreams",
        "rm /app/PhotoTable/PhotoTable.apk",
        "rmdir /app/PhotoTable/oat/arm",
        "rmdir /app/PhotoTable/oat",
        "rmdir /app/PhotoTable",
        "rm /app/sogou/sogou.apk",
        "rmdir /app/sogou/lib/arm",
        "rmdir /app/sogou/lib",
        "rmdir /app/sogou",
        "rm /app/es/es.apk",
        "rmdir /app/es",
        "rm /app/search/search.apk",
        "rmdir /app/search",
        "rm /app/launcher/launcher.apk",
        "rmdir /app/launcher",
        "rm /app/market/market.apk",
        "rmdir /app/market",
        
        # Add Reboot.apk (One-click U-Disk boot)
        "mkdir /app/Reboot",
        "write tools/Reboot.apk /app/Reboot/Reboot.apk",
        "set_inode_field /app/Reboot mode 040755",
        "set_inode_field /app/Reboot/Reboot.apk mode 0100644",
        
        # Add RootExplorer
        "mkdir /app/RootExplorer",
        "write tools/RootExplorer.apk /app/RootExplorer/RootExplorer.apk",
        "set_inode_field /app/RootExplorer mode 040755",
        "set_inode_field /app/RootExplorer/RootExplorer.apk mode 0100644",
        
        # Add Terminal
        "mkdir /app/Terminal",
        "write tools/Terminal.apk /app/Terminal/Terminal.apk",
        "set_inode_field /app/Terminal mode 040755",
        "set_inode_field /app/Terminal/Terminal.apk mode 0100644",
        
        # Update /build.prop
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0",
        
        # Add /bin/reboot-update
        "write build_rom/system_root/bin/reboot-update /bin/reboot-update",
        "set_inode_field /bin/reboot-update mode 0100755",
        "set_inode_field /bin/reboot-update uid 0",
        "set_inode_field /bin/reboot-update gid 2000"
    ]
    
    cmd_script_path = "tools/debugfs_cmds.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Running {len(cmds)} debugfs modifications...")
    wsl_cmd = f"wsl debugfs -w -f tools/debugfs_cmds.txt build_rom/system.raw.img"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("[!] Stderr:", res.stderr)
        
    # Ensure exact physical block size (327680 * 4096 = 1342177280)
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)
        
    # e2fsck validation
    print("[*] Running e2fsck check...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on modified system.raw.img!")
        
    print("[+] In-place ext4 modification complete & verified!")

if __name__ == '__main__':
    run_inplace_patch()
