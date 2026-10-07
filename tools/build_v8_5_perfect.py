import os
import subprocess
import shutil

import sys

def build_v19_domestic():
    print("=" * 65)
    print("  Building N1 NextGen TV v19 (Domestic Pure Release)")
    print("=" * 65)
    sys.path.insert(0, os.path.abspath('tools'))
    
    # 1. Update logo.PARTITION (clean TV logo)
    shutil.copy2('extracted_webpad/logo.PARTITION', 'build_rom/package/logo.PARTITION')
    
    # 2. Reset base system.raw.img from extracted_aml/system.raw.img
    src_raw = 'extracted_aml/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    print(f"[*] Copying pure official base {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)
    
    # 3. Prepare pristine official keylayout files
    os.makedirs('build_rom/system_root/usr/keylayout', exist_ok=True)
    shutil.copy2('extracted_aml/system_root/usr/keylayout/Generic.kl', 'build_rom/system_root/usr/keylayout/Generic.kl')
    shutil.copy2('extracted_aml/system_root/usr/keylayout/Vendor_0001_Product_0001.kl', 'build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl')
        
    # 4. Prepare APKs (ATV Launcher Pro Custom & NextGen WebPush)
    os.makedirs('build_rom/system_root/app/ATVLauncher', exist_ok=True)
    shutil.copy2('tools/re_tools/ATVLauncher_Custom_Hardcoded.apk', 'build_rom/system_root/app/ATVLauncher/ATVLauncher.apk')
    
    os.makedirs('build_rom/system_root/app/WebPush', exist_ok=True)
    shutil.copy2('tools/WebPush.apk', 'build_rom/system_root/app/WebPush/WebPush.apk')

    # Build and copy NextGen TV Dashboard Widget APK
    print("[*] Compiling latest NextGen TV Widget APK...")
    subprocess.run("python tools/build_tvwidget_apk.py", shell=True, check=True)
    os.makedirs('build_rom/system_root/app/NextGenWidget', exist_ok=True)
    shutil.copy2('tools/NextGen_TVWidget.apk', 'build_rom/system_root/app/NextGenWidget/NextGenWidget.apk')

    # Generate master ATV 3-sections database
    print("[*] Generating master ATV Launcher 3-sections database...")
    from create_master_atv_db import create_master_db
    create_master_db()

    # Prepare optimized bt_stack.conf from extracted_webpad (complete 72-line config)
    os.makedirs('build_rom/system_root/etc/bluetooth', exist_ok=True)
    shutil.copy2('extracted_webpad/system_root/etc/bluetooth/bt_stack.conf', 'build_rom/system_root/etc/bluetooth/bt_stack.conf')
    
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
        
        # --- PHASE 1.5: Remove Legacy WebView 52 & its ODEX ---
        "rm /app/webview/webview.apk",
        "rm /app/webview/oat/arm/webview.odex",
        "rm /app/webview/oat/arm64/webview.odex",
        "rmdir /app/webview/oat/arm",
        "rmdir /app/webview/oat/arm64",
        "rmdir /app/webview/oat",
        "rmdir /app/webview",

        # --- PHASE 2: Inject T1 Official Remote Pairing Wizard (Official Platform Signed) ---
        "mkdir /priv-app/Provision",
        "write extracted_webpad/system_root/priv-app/Provision/Provision.apk /priv-app/Provision/Provision.apk",
        "set_inode_field /priv-app/Provision mode 040755",
        "set_inode_field /priv-app/Provision/Provision.apk mode 0100644",
        "set_inode_field /priv-app/Provision/Provision.apk uid 0",
        "set_inode_field /priv-app/Provision/Provision.apk gid 0",
        
        # --- PHASE 3: Inject Premium ATV Launcher Pro & Widget ---
        "mkdir /app/ATVLauncher",
        "write build_rom/system_root/app/ATVLauncher/ATVLauncher.apk /app/ATVLauncher/ATVLauncher.apk",
        "set_inode_field /app/ATVLauncher mode 040755",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk mode 0100644",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk uid 0",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk gid 0",
        
        # --- PHASE 3.5: Inject Modern Google System WebView 119 (Android 7.1 Ultimate Web Engine) ---
        "mkdir /app/WebViewGoogle",
        "write build_rom/system_root/app/WebViewGoogle/WebViewGoogle.apk /app/WebViewGoogle/WebViewGoogle.apk",
        "set_inode_field /app/WebViewGoogle mode 040755",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk mode 0100644",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk uid 0",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk gid 0",
        
        "rm /framework/framework-res.apk",
        "write build_rom/system_root/framework/framework-res.apk /framework/framework-res.apk",
        "set_inode_field /framework/framework-res.apk mode 0100644",
        "set_inode_field /framework/framework-res.apk uid 0",
        "set_inode_field /framework/framework-res.apk gid 0",

        # --- PHASE 3.6: Inject Fixed TV Settings (Display & Resolution Support) ---
        "mkdir /priv-app/PhiTvSettings",
        "write build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk /priv-app/PhiTvSettings/PhiTvSettings.apk",
        "set_inode_field /priv-app/PhiTvSettings mode 040755",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk mode 0100644",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk uid 0",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk gid 0",

        # --- PHASE 3.65: Inject Custom NextGen Boot Animation ---
        "rm /media/bootanimation.zip",
        "write build_rom/system_root/media/bootanimation.zip /media/bootanimation.zip",
        "set_inode_field /media/bootanimation.zip mode 0100644",
        "set_inode_field /media/bootanimation.zip uid 0",
        "set_inode_field /media/bootanimation.zip gid 0",

        # --- PHASE 3.7: Inject Safe Sleep Helper & Daemon ---
        "write build_rom/system_root/bin/do_sleep.sh /bin/do_sleep.sh",
        "set_inode_field /bin/do_sleep.sh mode 0100755",
        "set_inode_field /bin/do_sleep.sh uid 0",
        "set_inode_field /bin/do_sleep.sh gid 0",
        "write build_rom/system_root/bin/run_nc.sh /bin/run_nc.sh",
        "set_inode_field /bin/run_nc.sh mode 0100755",
        "set_inode_field /bin/run_nc.sh uid 0",
        "set_inode_field /bin/run_nc.sh gid 0",
        "write build_rom/system_root/bin/install-recovery.sh /bin/install-recovery.sh",
        "set_inode_field /bin/install-recovery.sh mode 0100755",
        "set_inode_field /bin/install-recovery.sh uid 0",
        "set_inode_field /bin/install-recovery.sh gid 0",

        "rm /etc/security/mac_permissions.xml",
        "write build_rom/system_root/etc/security/mac_permissions.xml /etc/security/mac_permissions.xml",
        "set_inode_field /etc/security/mac_permissions.xml mode 0100644",
        "set_inode_field /etc/security/mac_permissions.xml uid 0",
        "set_inode_field /etc/security/mac_permissions.xml gid 0",

        "mkdir /app/NextGenWidget",
        "write tools/NextGen_TVWidget.apk /app/NextGenWidget/NextGenWidget.apk",
        "set_inode_field /app/NextGenWidget mode 040755",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk mode 0100644",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk uid 0",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk gid 0",
        
        # --- PHASE 4: Inject NextGen WebPush TV (Ultra-pure 100KB Web Push Engine) ---
        "mkdir /app/WebPush",
        "write tools/WebPush.apk /app/WebPush/WebPush.apk",
        "set_inode_field /app/WebPush mode 040755",
        "set_inode_field /app/WebPush/WebPush.apk mode 0100644",
        "set_inode_field /app/WebPush/WebPush.apk uid 0",
        "set_inode_field /app/WebPush/WebPush.apk gid 0",
        
        # --- PHASE 5: Inject High-Definition Redesigned FileBrowser & Wallpaper ---
        "rm /app/FileBrowser/FileBrowser.apk",
        "write tools/FileBrowser_TV_HD.apk /app/FileBrowser/FileBrowser.apk",
        "set_inode_field /app/FileBrowser/FileBrowser.apk mode 0100644",
        "set_inode_field /app/FileBrowser/FileBrowser.apk uid 0",
        "set_inode_field /app/FileBrowser/FileBrowser.apk gid 0",
        
        "rm /etc/default_wallpaper.png",
        "write build_rom/system_root/etc/default_wallpaper.png /etc/default_wallpaper.png",
        "set_inode_field /etc/default_wallpaper.png mode 0100644",
        "set_inode_field /etc/default_wallpaper.png uid 0",
        "set_inode_field /etc/default_wallpaper.png gid 0",
        
        "mkdir /etc/atvlauncher",
        "write build_rom/system_root/etc/atvlauncher/sections.db /etc/atvlauncher/sections.db",
        "set_inode_field /etc/atvlauncher mode 040755",
        "set_inode_field /etc/atvlauncher/sections.db mode 0100644",
        "set_inode_field /etc/atvlauncher/sections.db uid 0",
        "set_inode_field /etc/atvlauncher/sections.db gid 0",
        
        # --- PHASE 6: Inject Native Root Architecture ---
        "rm /xbin/su",
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
        
        "write build_rom/system_root/lib64/libsupol.so /lib64/libsupol.so",
        "set_inode_field /lib64/libsupol.so mode 0100644",
        "set_inode_field /lib64/libsupol.so uid 0",
        "set_inode_field /lib64/libsupol.so gid 0",
        
        "rm /xbin/busybox",
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
        
        # --- PHASE 7: Inject Bluetooth & Keylayout Optimizations ---
        "rm /etc/bluetooth/bt_stack.conf",
        "write build_rom/system_root/etc/bluetooth/bt_stack.conf /etc/bluetooth/bt_stack.conf",
        "set_inode_field /etc/bluetooth/bt_stack.conf mode 0100644",
        "set_inode_field /etc/bluetooth/bt_stack.conf uid 0",
        "set_inode_field /etc/bluetooth/bt_stack.conf gid 0",
        
        # --- PHASE 7.5: Inject MediaCodec Seccomp Policy (Amlogic Hardware Video Decoding Fix) ---
        "rm /etc/seccomp_policy/mediacodec-seccomp.policy",
        "write build_rom/system_root/etc/seccomp_policy/mediacodec-seccomp.policy /etc/seccomp_policy/mediacodec-seccomp.policy",
        "set_inode_field /etc/seccomp_policy/mediacodec-seccomp.policy mode 0100644",
        "set_inode_field /etc/seccomp_policy/mediacodec-seccomp.policy uid 0",
        "set_inode_field /etc/seccomp_policy/mediacodec-seccomp.policy gid 0",
        
        "rm /usr/keylayout/Generic.kl",
        "write build_rom/system_root/usr/keylayout/Generic.kl /usr/keylayout/Generic.kl",
        "set_inode_field /usr/keylayout/Generic.kl mode 0100644",
        "set_inode_field /usr/keylayout/Generic.kl uid 0",
        "set_inode_field /usr/keylayout/Generic.kl gid 0",
        
        "rm /usr/keylayout/Vendor_0001_Product_0001.kl",
        "write build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl /usr/keylayout/Vendor_0001_Product_0001.kl",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl mode 0100644",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl uid 0",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl gid 0",
        
        # --- PHASE 8: Inject Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]
    
    cmd_script_path = "tools/debugfs_v10.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")
            
    print(f"[*] Applying {len(cmds)} surgical modifications to system...")
    wsl_cmd = f"wsl debugfs -w -f tools/debugfs_v10.txt build_rom/system.raw.img"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout)
    
    # 6. Ensure physical size
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)

    # 7. Enforce native ext4 SELinux extended attributes on all modified/injected inodes
    from ext4_set_selinux import fix_all_selinux_in_image
    fix_all_selinux_in_image(dst_raw)

    print("[*] Verifying critical SELinux attributes...")
    subprocess.run("python tools/verify_xattr.py", shell=True, check=True)
        
    # 8. e2fsck verification
    print("[*] Running e2fsck system verification...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on system.raw.img!")
        
    # 8. Generate Sparse system.PARTITION
    print("[*] Generating Android Sparse system.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/system.raw.img build_rom/package/system.PARTITION", shell=True, check=True)
    
    # 9. Package final image
    out_img = "N1_NextGen_TV_v19_Domestic_Release.img"
    if os.path.exists(out_img):
        try:
            with open(out_img, "ab"): pass
        except Exception:
            print(f"[!] Warning: {out_img} is currently opened/locked by USB_Burning_Tool!")
            out_img = "N1_NextGen_TV_v19_Domestic_Release_Fixed.img"
            print(f"[!] Writing to new image file: {out_img}")

    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img} ({os.path.getsize(out_img)/1024/1024:.2f} MB)")

if __name__ == '__main__':
    build_v19_domestic()
