"""
N1 NextGen TV v18.5 (microG Global Pure Edition) Build Script
===========================================================
- Based on 100% stable v18.3 baseline (ATV Launcher, WebView 119, NextGen Widget, WebPush TV)
- Integrates lightweight microG ecosystem (microG GmsCore, FakeStore, GsfProxy, Aurora Store)
- No complex smali signature patches or framework tampering needed
- Extremely lightweight (< 120MB total addition, plenty of room on 1152MB partition)
"""
import os
import subprocess
import shutil
import sys

def build_v18_5_microg():
    print("=" * 65)
    print("  Building N1 NextGen TV v18.5 (microG Global Pure Edition)")
    print("=" * 65)

    # 1. Update logo.PARTITION (clean TV logo)
    shutil.copy2('extracted_webpad/logo.PARTITION', 'build_rom/package/logo.PARTITION')

    # 2. Reset base system.raw.img from pristine base
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

    # 4. Prepare Core ATV APKs
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
    print("[*] Generating master ATV Launcher database...")
    sys.path.insert(0, os.path.abspath('tools'))
    from create_master_atv_db import create_master_db
    create_master_db()

    # Prepare optimized bt_stack.conf
    os.makedirs('build_rom/system_root/etc/bluetooth', exist_ok=True)
    bt_conf = """BtSnoopLogOutput=false
BtSnoopFileName=/sdcard/btsnoop_hci.log
BtSnoopSaveLog=false
TraceConf=true
TRC_BTM=1
TRC_HCI=1
TRC_L2CAP=1
TRC_GATT=1
TRC_BTIF=1
"""
    with open('build_rom/system_root/etc/bluetooth/bt_stack.conf', 'w', encoding='utf-8', newline='\n') as f:
        f.write(bt_conf)

    # Prepare microG permissions XML
    os.makedirs('build_rom/system_root/etc/permissions', exist_ok=True)
    shutil.copy2('tools/microg_permissions.xml', 'build_rom/system_root/etc/permissions/microg_permissions.xml')

    # 5. Prepare debugfs surgical removal & addition commands
    print("[*] Assembling debugfs injection plan...")
    cmds = [
        # --- PHASE 1: Remove Phicomm Bloatware ---
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

        # --- PHASE 2: Upgrade WebView to v119 ---
        "rm /app/webview/webview.apk",
        "rm /app/webview/oat/arm/webview.odex",
        "rm /app/webview/oat/arm64/webview.odex",
        "rmdir /app/webview/oat/arm",
        "rmdir /app/webview/oat/arm64",
        "rmdir /app/webview/oat",
        "rmdir /app/webview",
        "mkdir /app/WebViewGoogle",
        "set_inode_field /app/WebViewGoogle mode 040755",
        "write build_rom/system_root/app/WebViewGoogle/WebViewGoogle.apk /app/WebViewGoogle/WebViewGoogle.apk",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk mode 0100644",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk uid 0",
        "set_inode_field /app/WebViewGoogle/WebViewGoogle.apk gid 0",
        "rm /framework/framework-res.apk",
        "write build_rom/system_root/framework/framework-res.apk /framework/framework-res.apk",
        "set_inode_field /framework/framework-res.apk mode 0100644",
        "set_inode_field /framework/framework-res.apk uid 0",
        "set_inode_field /framework/framework-res.apk gid 0",

        # --- PHASE 3: Install Core ATV & System Apps ---
        "mkdir /priv-app/Provision",
        "set_inode_field /priv-app/Provision mode 040755",
        "write extracted_webpad/system_root/priv-app/Provision/Provision.apk /priv-app/Provision/Provision.apk",
        "set_inode_field /priv-app/Provision/Provision.apk mode 0100644",
        "set_inode_field /priv-app/Provision/Provision.apk uid 0",
        "set_inode_field /priv-app/Provision/Provision.apk gid 0",

        "mkdir /priv-app/PhiTvSettings",
        "set_inode_field /priv-app/PhiTvSettings mode 040755",
        "write tools/re_tools/PhiTvSettings_Signed.apk /priv-app/PhiTvSettings/PhiTvSettings.apk",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk mode 0100644",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk uid 0",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk gid 0",

        "mkdir /app/ATVLauncher",
        "set_inode_field /app/ATVLauncher mode 040755",
        "write build_rom/system_root/app/ATVLauncher/ATVLauncher.apk /app/ATVLauncher/ATVLauncher.apk",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk mode 0100644",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk uid 0",
        "set_inode_field /app/ATVLauncher/ATVLauncher.apk gid 0",

        "mkdir /app/NextGenWidget",
        "set_inode_field /app/NextGenWidget mode 040755",
        "write build_rom/system_root/app/NextGenWidget/NextGenWidget.apk /app/NextGenWidget/NextGenWidget.apk",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk mode 0100644",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk uid 0",
        "set_inode_field /app/NextGenWidget/NextGenWidget.apk gid 0",

        "mkdir /app/WebPush",
        "set_inode_field /app/WebPush mode 040755",
        "write build_rom/system_root/app/WebPush/WebPush.apk /app/WebPush/WebPush.apk",
        "set_inode_field /app/WebPush/WebPush.apk mode 0100644",
        "set_inode_field /app/WebPush/WebPush.apk uid 0",
        "set_inode_field /app/WebPush/WebPush.apk gid 0",

        "rm /app/FileBrowser/FileBrowser.apk",
        "write tools/FileBrowser_TV_HD.apk /app/FileBrowser/FileBrowser.apk",
        "set_inode_field /app/FileBrowser/FileBrowser.apk mode 0100644",
        "set_inode_field /app/FileBrowser/FileBrowser.apk uid 0",
        "set_inode_field /app/FileBrowser/FileBrowser.apk gid 0",

        # --- PHASE 4: Inject microG Ecosystem Components ---
        # 4.1 microG GmsCore (priv-app for signature spoofing / account manager access)
        "mkdir /priv-app/GmsCore",
        "set_inode_field /priv-app/GmsCore mode 040755",
        "write tools/microg_gmscore.apk /priv-app/GmsCore/GmsCore.apk",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk mode 0100644",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk uid 0",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk gid 0",

        # 4.2 microG FakeStore / Companion (priv-app)
        "mkdir /priv-app/FakeStore",
        "set_inode_field /priv-app/FakeStore mode 040755",
        "write tools/microg_fakestore.apk /priv-app/FakeStore/FakeStore.apk",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk mode 0100644",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk uid 0",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk gid 0",

        # 4.3 microG GsfProxy (priv-app)
        "mkdir /priv-app/GsfProxy",
        "set_inode_field /priv-app/GsfProxy mode 040755",
        "write tools/microg_gsfproxy.apk /priv-app/GsfProxy/GsfProxy.apk",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk mode 0100644",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk uid 0",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk gid 0",

        # 4.4 Aurora Store (app - Play Store Alternative with TV support)
        "mkdir /app/AuroraStore",
        "set_inode_field /app/AuroraStore mode 040755",
        "write tools/AuroraStore.apk /app/AuroraStore/AuroraStore.apk",
        "set_inode_field /app/AuroraStore/AuroraStore.apk mode 0100644",
        "set_inode_field /app/AuroraStore/AuroraStore.apk uid 0",
        "set_inode_field /app/AuroraStore/AuroraStore.apk gid 0",

        # 4.5 microG permissions
        "write build_rom/system_root/etc/permissions/microg_permissions.xml /etc/permissions/microg_permissions.xml",
        "set_inode_field /etc/permissions/microg_permissions.xml mode 0100644",
        "set_inode_field /etc/permissions/microg_permissions.xml uid 0",
        "set_inode_field /etc/permissions/microg_permissions.xml gid 0",

        # --- PHASE 5: Root & Webpad Daemons ---
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

        # --- PHASE 6: Configuration Files ---
        "write build_rom/system_root/etc/default_wallpaper.png /etc/default_wallpaper.png",
        "set_inode_field /etc/default_wallpaper.png mode 0100644",
        "set_inode_field /etc/default_wallpaper.png uid 0",
        "set_inode_field /etc/default_wallpaper.png gid 0",

        "mkdir /etc/atvlauncher",
        "set_inode_field /etc/atvlauncher mode 040755",
        "write build_rom/system_root/etc/atvlauncher/sections.db /etc/atvlauncher/sections.db",
        "set_inode_field /etc/atvlauncher/sections.db mode 0100644",
        "set_inode_field /etc/atvlauncher/sections.db uid 0",
        "set_inode_field /etc/atvlauncher/sections.db gid 0",

        "rm /etc/bluetooth/bt_stack.conf",
        "write build_rom/system_root/etc/bluetooth/bt_stack.conf /etc/bluetooth/bt_stack.conf",
        "set_inode_field /etc/bluetooth/bt_stack.conf mode 0100644",
        "set_inode_field /etc/bluetooth/bt_stack.conf uid 0",
        "set_inode_field /etc/bluetooth/bt_stack.conf gid 0",

        "write build_rom/system_root/usr/keylayout/Generic.kl /usr/keylayout/Generic.kl",
        "set_inode_field /usr/keylayout/Generic.kl mode 0100644",
        "set_inode_field /usr/keylayout/Generic.kl uid 0",
        "set_inode_field /usr/keylayout/Generic.kl gid 0",

        "write build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl /usr/keylayout/Vendor_0001_Product_0001.kl",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl mode 0100644",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl uid 0",
        "set_inode_field /usr/keylayout/Vendor_0001_Product_0001.kl gid 0",

        # --- PHASE 7: Clean Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]

    cmd_script_path = "tools/debugfs_v18_5_microg.txt"
    with open(cmd_script_path, "w", encoding="utf-8", newline="\n") as f:
        for c in cmds:
            f.write(c + "\n")

    print(f"[*] Applying {len(cmds)} modifications to system.raw.img via WSL debugfs...")
    wsl_cmd = f"wsl debugfs -w -f {cmd_script_path} {dst_raw}"
    res = subprocess.run(wsl_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout[-300:] if len(res.stdout) > 300 else res.stdout)

    # 6. Ensure physical size (1152MB)
    with open(dst_raw, 'r+b') as f:
        f.truncate(327680 * 4096)

    # 7. SELinux Extended Attributes Fix
    print("[*] Enforcing native ext4 SELinux extended attributes on all inodes...")
    from ext4_set_selinux import fix_all_selinux_in_image
    fix_all_selinux_in_image(dst_raw)

    # 8. File system verification (e2fsck)
    print("[*] Running e2fsck system verification...")
    fsck_res = subprocess.run("wsl e2fsck -f -y build_rom/system.raw.img", shell=True, capture_output=True, text=True)
    print(fsck_res.stdout)
    if fsck_res.returncode != 0:
        raise RuntimeError("e2fsck failed on system.raw.img!")

    # 9. Convert to Sparse Image
    print("[*] Generating Android Sparse system.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/system.raw.img build_rom/package/system.PARTITION", shell=True, check=True)

    # 10. Package final image
    out_img = "N1_NextGen_TV_v18.5_microG_Global_Flawless.img"
    if os.path.exists(out_img):
        try: os.remove(out_img)
        except Exception: pass

    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img}")

if __name__ == '__main__':
    build_v18_5_microg()
