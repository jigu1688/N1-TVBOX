import os
import subprocess
import shutil

def build_v7_media_fixed():
    print("="*60)
    print("  Building NextGen TV v7.1 (KODI + MX Player Native Libs Fixed)")
    print("="*60)
    
    # 1. Update logo.PARTITION (clean TV logo)
    shutil.copy2('extracted_webpad/logo.PARTITION', 'build_rom/package/logo.PARTITION')
    
    # 2. Reset base system.raw.img from extracted_aml/system.raw.img
    src_raw = 'extracted_aml/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    print(f"[*] Copying pure official base {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)
    
    # 3. Prepare modified keylayout files with POWER WAKE
    os.makedirs('build_rom/system_root/usr/keylayout', exist_ok=True)
    with open('extracted_aml/system_root/usr/keylayout/Generic.kl', 'r', encoding='latin1') as f:
        kl_generic = f.read().replace('key 116   POWER', 'key 116   POWER                 WAKE')
    with open('build_rom/system_root/usr/keylayout/Generic.kl', 'w', encoding='latin1', newline='\n') as f:
        f.write(kl_generic)
        
    with open('extracted_aml/system_root/usr/keylayout/Vendor_0001_Product_0001.kl', 'r', encoding='latin1') as f:
        kl_vendor = f.read().replace('key 116   POWER', 'key 116   POWER                 WAKE')
    with open('build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl', 'w', encoding='latin1', newline='\n') as f:
        f.write(kl_vendor)
        
    # 4. Prepare APKs & Native Libraries
    os.makedirs('build_rom/system_root/app/ATVLauncher', exist_ok=True)
    shutil.copy2('ATV Launcher Pro v0.2.1.apk', 'build_rom/system_root/app/ATVLauncher/ATVLauncher.apk')
    
    os.makedirs('build_rom/system_root/app/XiaoBaiFile', exist_ok=True)
    shutil.copy2('小白电视文件传输v2.8.0.apk', 'build_rom/system_root/app/XiaoBaiFile/XiaoBaiFile.apk')
    
    os.makedirs('build_rom/system_root/app/Kodi', exist_ok=True)
    shutil.copy2('tools/Kodi_19.5_Matrix_arm64.apk', 'build_rom/system_root/app/Kodi/Kodi.apk')
    
    os.makedirs('build_rom/system_root/app/MXPlayerPro', exist_ok=True)
    shutil.copy2('tools/MXPlayerPro.apk', 'build_rom/system_root/app/MXPlayerPro/MXPlayerPro.apk')
    
    # 5. Build debugfs commands
    cmds = [
        # --- PHASE 1: Purge All Phicomm Mining, CDN, Backdoors ---
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
        
        # --- PHASE 2: Inject T1 Official Remote Pairing Wizard ---
        "mkdir /priv-app/Provision",
        "write extracted_webpad/system_root/priv-app/Provision/Provision.apk /priv-app/Provision/Provision.apk",
        "set_inode_field /priv-app/Provision mode 040755",
        "set_inode_field /priv-app/Provision/Provision.apk mode 0100644",
        "set_inode_field /priv-app/Provision/Provision.apk uid 0",
        "set_inode_field /priv-app/Provision/Provision.apk gid 0",
        
        # --- PHASE 3: Inject Premium ATV Launcher Pro ---
        "mkdir /app/ATVLauncher",
        "write build_rom/system_root/app/ATVLauncher/ATVLauncher.apk /app/ATVLauncher/ATVLauncher.apk",
        "set_inode_field /app/ATVLauncher mode 040755",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk mode 0100644",
        
        # --- PHASE 4: Inject XiaoBai TV File Web Push ---
        "mkdir /app/XiaoBaiFile",
        "write build_rom/system_root/app/XiaoBaiFile/XiaoBaiFile.apk /app/XiaoBaiFile/XiaoBaiFile.apk",
        "set_inode_field /app/XiaoBaiFile mode 040755",
        "set_inode_field /app/XiaoBaiFile/XiaoBaiFile.apk mode 0100644",
        
        # --- PHASE 5: Inject KODI Matrix Media Center + Native Libs ---
        "mkdir /app/Kodi",
        "write build_rom/system_root/app/Kodi/Kodi.apk /app/Kodi/Kodi.apk",
        "set_inode_field /app/Kodi mode 040755",
        "set_inode_field /app/Kodi/Kodi.apk mode 0100644",
        "mkdir /app/Kodi/lib",
        "set_inode_field /app/Kodi/lib mode 040755",
        "mkdir /app/Kodi/lib/arm64",
        "set_inode_field /app/Kodi/lib/arm64 mode 040755",
    ]
    
    # Add Kodi arm64 native libs
    for fn in os.listdir('tools/kodi_libs/arm64'):
        cmds.append(f"write tools/kodi_libs/arm64/{fn} /app/Kodi/lib/arm64/{fn}")
        cmds.append(f"set_inode_field /app/Kodi/lib/arm64/{fn} mode 0100644")
        cmds.append(f"set_inode_field /app/Kodi/lib/arm64/{fn} uid 0")
        cmds.append(f"set_inode_field /app/Kodi/lib/arm64/{fn} gid 0")
        
    # --- PHASE 6: Inject MX Player Pro TV Edition + Native Libs ---
    cmds += [
        "mkdir /app/MXPlayerPro",
        "write build_rom/system_root/app/MXPlayerPro/MXPlayerPro.apk /app/MXPlayerPro/MXPlayerPro.apk",
        "set_inode_field /app/MXPlayerPro mode 040755",
        "set_inode_field /app/MXPlayerPro/MXPlayerPro.apk mode 0100644",
        "mkdir /app/MXPlayerPro/lib",
        "set_inode_field /app/MXPlayerPro/lib mode 040755",
        "mkdir /app/MXPlayerPro/lib/arm",
        "set_inode_field /app/MXPlayerPro/lib/arm mode 040755",
    ]
    
    # Add MX Player arm native libs
    for fn in os.listdir('tools/mx_libs/arm'):
        cmds.append(f"write tools/mx_libs/arm/{fn} /app/MXPlayerPro/lib/arm/{fn}")
        cmds.append(f"set_inode_field /app/MXPlayerPro/lib/arm/{fn} mode 0100644")
        cmds.append(f"set_inode_field /app/MXPlayerPro/lib/arm/{fn} uid 0")
        cmds.append(f"set_inode_field /app/MXPlayerPro/lib/arm/{fn} gid 0")
        
    # --- PHASE 7: Inject Geek Utilities & One-Click U-Disk Boot ---
    cmds += [
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
        
        # --- PHASE 8: Inject Native Root Architecture ---
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
        
        # --- PHASE 9: Inject Power Key Layout Mappings ---
        "write build_rom/system_root/usr/keylayout/Generic.kl /usr/keylayout/Generic.kl",
        "set_inode_field /usr/keylayout/Generic.kl mode 0100644",
        "set_inode_field /usr/keylayout/Generic.kl uid 0",
        "set_inode_field /usr/keylayout/Generic.kl gid 0",
        
        "write build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl /usr/keylayout/Vendor_0001_Product_0001.kl",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl mode 0100644",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl uid 0",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl gid 0",
        
        # --- PHASE 10: Inject Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]
    
    cmd_script_path = "tools/debugfs_v7_media_fixed.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Applying {len(cmds)} surgical modifications...")
    wsl_cmd = f"wsl debugfs -w -f tools/debugfs_v7_media_fixed.txt build_rom/system.raw.img"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    
    # 6. Ensure physical size
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)
        
    # 7. e2fsck verification
    print("[*] Running e2fsck system verification...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on system.raw.img!")
        
    # 8. Generate Sparse system.PARTITION
    print("[*] Generating Android Sparse system.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/system.raw.img build_rom/package/system.PARTITION", shell=True, check=True)
    
    # 9. Package final image
    out_img = "N1_NextGen_TV_v7.1_MediaFixed.img"
    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img}")

if __name__ == '__main__':
    build_v7_media_fixed()
