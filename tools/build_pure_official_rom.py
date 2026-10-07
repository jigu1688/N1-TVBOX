import os
import subprocess
import shutil

def build_pure_official_rom():
    print("="*60)
    print("  Building 100% Pure Official Stock TV ROM (v2.0 Guaranteed)")
    print("="*60)
    
    # 1. Update logo.PARTITION (remove Phicomm Butler advertisement)
    src_logo = 'extracted_webpad/logo.PARTITION'
    dst_logo = 'build_rom/package/logo.PARTITION'
    if os.path.exists(src_logo):
        shutil.copy2(src_logo, dst_logo)
        print(f"[+] Replaced logo.PARTITION with clean TV logo")
        
    # 2. Start from extracted_aml/system.raw.img (Official V2.19 Stock ext4 image)
    src_raw = 'extracted_aml/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    print(f"[*] Copying pure official base {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)
    
    # 3. Build debugfs command list for pure official base
    cmds = [
        # --- PHASE 1: Purge Phicomm Mining, Bloat & Backdoors ---
        # 1. Mining client
        "rm /app/Dig/Dig.apk",
        "rmdir /app/Dig/oat/arm",
        "rmdir /app/Dig/oat",
        "rmdir /app/Dig",
        
        # 2. Phicomm Shared CDN
        "rm /priv-app/PhiCDN/PhiCDN.apk",
        "rmdir /priv-app/PhiCDN/oat/arm",
        "rmdir /priv-app/PhiCDN/oat",
        "rmdir /priv-app/PhiCDN",
        
        # 3. Data Tracker & Telemetry
        "rm /priv-app/DataTracker/DataTracker.apk",
        "rmdir /priv-app/DataTracker/oat/arm",
        "rmdir /priv-app/DataTracker/oat",
        "rmdir /priv-app/DataTracker",
        
        # 4. Forced OTA Upgrader
        "rm /priv-app/PhiOTAUpgrade/PhiOTAUpgrade.apk",
        "rmdir /priv-app/PhiOTAUpgrade/oat/arm",
        "rmdir /priv-app/PhiOTAUpgrade/oat",
        "rmdir /priv-app/PhiOTAUpgrade",
        
        # 5. Phicomm Cloud Box & Downloader & Account
        "rm /priv-app/PhiCloudBox/PhiCloudBox.apk",
        "rmdir /priv-app/PhiCloudBox/oat/arm",
        "rmdir /priv-app/PhiCloudBox/oat",
        "rmdir /priv-app/PhiCloudBox",
        
        "rm /priv-app/PhiDownloader/PhiDownloader.apk",
        "rmdir /priv-app/PhiDownloader/oat/arm",
        "rmdir /priv-app/PhiDownloader/oat",
        "rmdir /priv-app/PhiDownloader",
        
        "rm /priv-app/PhiTvAccount/PhiTvAccount.apk",
        "rmdir /priv-app/PhiTvAccount/oat/arm",
        "rmdir /priv-app/PhiTvAccount/oat",
        "rmdir /priv-app/PhiTvAccount",
        
        "rm /priv-app/PhiTvRemoteServer/PhiTvRemoteServer.apk",
        "rmdir /priv-app/PhiTvRemoteServer/oat/arm",
        "rmdir /priv-app/PhiTvRemoteServer/oat",
        "rmdir /priv-app/PhiTvRemoteServer",
        
        "rm /priv-app/PhiDiskFormat/PhiDiskFormat.apk",
        "rmdir /priv-app/PhiDiskFormat/oat/arm",
        "rmdir /priv-app/PhiDiskFormat/oat",
        "rmdir /priv-app/PhiDiskFormat",
        
        "rm /priv-app/PhiFactoryTest/PhiFactoryTest.apk",
        "rmdir /priv-app/PhiFactoryTest/oat/arm",
        "rmdir /priv-app/PhiFactoryTest/oat",
        "rmdir /priv-app/PhiFactoryTest",
        
        # 6. Official Mining NAS Butler Launcher (replace with TV Launcher)
        "rm /priv-app/PhiLauncher/PhiLauncher.apk",
        "rmdir /priv-app/PhiLauncher/oat/arm",
        "rmdir /priv-app/PhiLauncher/oat",
        "rmdir /priv-app/PhiLauncher",
        
        # 7. Unused Phicomm Media Players
        "rm /app/PhiNasDMS/PhiNasDMS.apk",
        "rmdir /app/PhiNasDMS/oat/arm",
        "rmdir /app/PhiNasDMS/oat",
        "rmdir /app/PhiNasDMS",
        
        "rm /app/PhiNasImagePlayer/PhiNasImagePlayer.apk",
        "rmdir /app/PhiNasImagePlayer/oat/arm",
        "rmdir /app/PhiNasImagePlayer/oat",
        "rmdir /app/PhiNasImagePlayer",
        
        "rm /app/PhiTvMusic/PhiTvMusic.apk",
        "rmdir /app/PhiTvMusic/oat/arm",
        "rmdir /app/PhiTvMusic/oat",
        "rmdir /app/PhiTvMusic",
        
        "rm /app/PhiTvVideoPlayer/PhiTvVideoPlayer.apk",
        "rmdir /app/PhiTvVideoPlayer/oat/arm",
        "rmdir /app/PhiTvVideoPlayer/oat",
        "rmdir /app/PhiTvVideoPlayer",
        
        # --- PHASE 2: Inject Modern TV Launchers into /system/app ---
        # 1. launcher (Dangbei Launcher - guaranteed arm64 compatibility)
        "mkdir /app/launcher",
        "write extracted_webpad/system_root/app/launcher/launcher.apk /app/launcher/launcher.apk",
        "set_inode_field /app/launcher mode 040755",
        "set_inode_field /app/launcher/launcher.apk mode 0100644",
        
        # 2. tvlauncher (TV Launcher Pro)
        "mkdir /app/tvlauncher",
        "write extracted_webpad/system_root/app/tvlauncher/tvlauncher.apk /app/tvlauncher/tvlauncher.apk",
        "set_inode_field /app/tvlauncher mode 040755",
        "set_inode_field /app/tvlauncher/tvlauncher.apk mode 0100644",
        
        # 3. Lighthome (Lightweight Home)
        "mkdir /app/Lighthome",
        "write extracted_webpad/system_root/app/Lighthome/Lighthome.apk /app/Lighthome/Lighthome.apk",
        "set_inode_field /app/Lighthome mode 040755",
        "set_inode_field /app/Lighthome/Lighthome.apk mode 0100644",
        
        # --- PHASE 3: Inject Geek Utilities & One-Click U-Disk Boot ---
        # 1. Reboot.apk (One-click U-Disk Boot / Recovery / PowerOff)
        "mkdir /app/Reboot",
        "write tools/Reboot.apk /app/Reboot/Reboot.apk",
        "set_inode_field /app/Reboot mode 040755",
        "set_inode_field /app/Reboot/Reboot.apk mode 0100644",
        
        # 2. RootExplorer
        "mkdir /app/RootExplorer",
        "write tools/RootExplorer.apk /app/RootExplorer/RootExplorer.apk",
        "set_inode_field /app/RootExplorer mode 040755",
        "set_inode_field /app/RootExplorer/RootExplorer.apk mode 0100644",
        
        # 3. Terminal Emulator
        "mkdir /app/Terminal",
        "write tools/Terminal.apk /app/Terminal/Terminal.apk",
        "set_inode_field /app/Terminal mode 040755",
        "set_inode_field /app/Terminal/Terminal.apk mode 0100644",
        
        # 4. /bin/reboot-update
        "write build_rom/system_root/bin/reboot-update /bin/reboot-update",
        "set_inode_field /bin/reboot-update mode 0100755",
        "set_inode_field /bin/reboot-update uid 0",
        "set_inode_field /bin/reboot-update gid 2000",
        
        # --- PHASE 4: Inject Native Root Architecture ---
        "write build_rom/system_root/xbin/su /xbin/su",
        "set_inode_field /xbin/su mode 0104755",
        "set_inode_field /xbin/su uid 0",
        "set_inode_field /xbin/su gid 2000",
        
        "write build_rom/system_root/xbin/daemonsu /xbin/daemonsu",
        "set_inode_field /xbin/daemonsu mode 0100755",
        "set_inode_field /xbin/daemonsu uid 0",
        "set_inode_field /xbin/daemonsu gid 2000",
        
        "write build_rom/system_root/xbin/supolicy /xbin/supolicy",
        "set_inode_field /xbin/supolicy mode 0100755",
        "set_inode_field /xbin/supolicy uid 0",
        "set_inode_field /xbin/supolicy gid 2000",
        
        "write build_rom/system_root/xbin/busybox /xbin/busybox",
        "set_inode_field /xbin/busybox mode 0100755",
        "set_inode_field /xbin/busybox uid 0",
        "set_inode_field /xbin/busybox gid 2000",
        
        "write build_rom/system_root/bin/webpad /bin/webpad",
        "set_inode_field /bin/webpad mode 0100755",
        "set_inode_field /bin/webpad uid 0",
        "set_inode_field /bin/webpad gid 2000",
        
        "write build_rom/system_root/bin/webpadinit.sh /bin/webpadinit.sh",
        "set_inode_field /bin/webpadinit.sh mode 0100755",
        "set_inode_field /bin/webpadinit.sh uid 0",
        "set_inode_field /bin/webpadinit.sh gid 2000",
        
        "write build_rom/system_root/etc/init/daemonsu.rc /etc/init/daemonsu.rc",
        "set_inode_field /etc/init/daemonsu.rc mode 0100644",
        "set_inode_field /etc/init/daemonsu.rc uid 0",
        "set_inode_field /etc/init/daemonsu.rc gid 0",
        
        # --- PHASE 5: Inject High Performance & Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]
    
    cmd_script_path = "tools/debugfs_official_pure_v2.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Applying {len(cmds)} surgical modifications to official base...")
    wsl_cmd = f"wsl debugfs -w -f tools/debugfs_official_pure_v2.txt build_rom/system.raw.img"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    
    # 4. Ensure exact physical size (327680 blocks * 4096 = 1342177280 bytes)
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)
        
    # 5. Run e2fsck verification
    print("[*] Running e2fsck filesystem verification...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck verification failed on official system image!")
        
    # 6. Convert to Sparse system.PARTITION
    print("[*] Generating Android Sparse system.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/system.raw.img build_rom/package/system.PARTITION", shell=True, check=True)
    
    # 7. Package final Pure Official Firmware Image
    out_img = "N1_NextGen_Official_Pure_v3.0_Final.img"
    print(f"[*] Packaging 100% Pure Official Firmware Image: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    
    print("="*60)
    print(f"[+] SUCCESS! Generated: {out_img}")
    print("="*60)

if __name__ == '__main__':
    build_pure_official_rom()
