import os
import subprocess
import shutil

def build_v4_with_t1_remote_and_clean_data():
    print("="*60)
    print("  Building NextGen TV v4.0 with T1 Remote Pairing & Clean Data")
    print("="*60)
    
    # 1. Update logo.PARTITION (clean TV logo)
    shutil.copy2('extracted_webpad/logo.PARTITION', 'build_rom/package/logo.PARTITION')
    
    # 2. Re-convert clean data.raw.img to data.PARTITION
    print("[*] Converting clean data.raw.img -> data.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/data.raw.img build_rom/package/data.PARTITION", shell=True, check=True)
    
    # 3. Add T1 Provision.apk (Bluetooth Remote Pairing Wizard) to system.raw.img
    src_raw = 'extracted_aml/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    print(f"[*] Resetting pure official base {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)
    
    cmds = [
        # --- PHASE 1: Purge Phicomm Mining, Bloat & Backdoors ---
        "rm /app/Dig/Dig.apk",
        "rmdir /app/Dig/oat/arm",
        "rmdir /app/Dig/oat",
        "rmdir /app/Dig",
        
        "rm /priv-app/PhiCDN/PhiCDN.apk",
        "rmdir /priv-app/PhiCDN/oat/arm",
        "rmdir /priv-app/PhiCDN/oat",
        "rmdir /priv-app/PhiCDN",
        
        "rm /priv-app/DataTracker/DataTracker.apk",
        "rmdir /priv-app/DataTracker/oat/arm",
        "rmdir /priv-app/DataTracker/oat",
        "rmdir /priv-app/DataTracker",
        
        "rm /priv-app/PhiOTAUpgrade/PhiOTAUpgrade.apk",
        "rmdir /priv-app/PhiOTAUpgrade/oat/arm",
        "rmdir /priv-app/PhiOTAUpgrade/oat",
        "rmdir /priv-app/PhiOTAUpgrade",
        
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
        
        "rm /priv-app/PhiLauncher/PhiLauncher.apk",
        "rmdir /priv-app/PhiLauncher/oat/arm",
        "rmdir /priv-app/PhiLauncher/oat",
        "rmdir /priv-app/PhiLauncher",
        
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
        
        # --- PHASE 2: Inject T1 Official Bluetooth Remote Pairing Wizard ---
        "mkdir /priv-app/Provision",
        "write extracted_webpad/system_root/priv-app/Provision/Provision.apk /priv-app/Provision/Provision.apk",
        "set_inode_field /priv-app/Provision mode 040755",
        "set_inode_field /priv-app/Provision/Provision.apk mode 0100644",
        "set_inode_field /priv-app/Provision/Provision.apk uid 0",
        "set_inode_field /priv-app/Provision/Provision.apk gid 0",
        
        # --- PHASE 3: Inject Modern TV Launchers into /system/app ---
        "mkdir /app/launcher",
        "write extracted_webpad/system_root/app/launcher/launcher.apk /app/launcher/launcher.apk",
        "set_inode_field /app/launcher mode 040755",
        "set_inode_field /app/launcher/launcher.apk mode 0100644",
        
        "mkdir /app/tvlauncher",
        "write extracted_webpad/system_root/app/tvlauncher/tvlauncher.apk /app/tvlauncher/tvlauncher.apk",
        "set_inode_field /app/tvlauncher mode 040755",
        "set_inode_field /app/tvlauncher/tvlauncher.apk mode 0100644",
        
        "mkdir /app/Lighthome",
        "write extracted_webpad/system_root/app/Lighthome/Lighthome.apk /app/Lighthome/Lighthome.apk",
        "set_inode_field /app/Lighthome mode 040755",
        "set_inode_field /app/Lighthome/Lighthome.apk mode 0100644",
        
        # --- PHASE 4: Inject Geek Utilities & One-Click U-Disk Boot ---
        "mkdir /app/Reboot",
        "write tools/Reboot.apk /app/Reboot/Reboot.apk",
        "set_inode_field /app/Reboot mode 040755",
        "set_inode_field /app/Reboot/Reboot.apk mode 0100644",
        
        "mkdir /app/RootExplorer",
        "write tools/RootExplorer.apk /app/RootExplorer/RootExplorer.apk",
        "set_inode_field /app/RootExplorer mode 040755",
        "set_inode_field /app/RootExplorer/RootExplorer.apk mode 0100644",
        
        "mkdir /app/Terminal",
        "write tools/Terminal.apk /app/Terminal/Terminal.apk",
        "set_inode_field /app/Terminal mode 040755",
        "set_inode_field /app/Terminal/Terminal.apk mode 0100644",
        
        "write build_rom/system_root/bin/reboot-update /bin/reboot-update",
        "set_inode_field /bin/reboot-update mode 0100755",
        "set_inode_field /bin/reboot-update uid 0",
        "set_inode_field /bin/reboot-update gid 2000",
        
        # --- PHASE 5: Inject Native Root Architecture ---
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
        
        # --- PHASE 6: Inject Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]
    
    cmd_script_path = "tools/debugfs_t1_remote.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Applying {len(cmds)} surgical modifications...")
    wsl_cmd = f"wsl debugfs -w -f tools/debugfs_t1_remote.txt build_rom/system.raw.img"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    
    # 4. Ensure physical size
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)
        
    # 5. e2fsck verification
    print("[*] Running e2fsck system verification...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on system.raw.img!")
        
    # 6. Generate Sparse system.PARTITION
    print("[*] Generating Android Sparse system.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/system.raw.img build_rom/package/system.PARTITION", shell=True, check=True)
    
    # 7. Package final image
    out_img = "N1_NextGen_TV_v4.0_T1Remote_Clean.img"
    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img}")

if __name__ == '__main__':
    build_v4_with_t1_remote_and_clean_data()
