"""
N1 NextGen TV v19 (Pristine Global Edition)
=============================================
- Full microG Ecosystem (Google Account login, FCM push, Google Maps/Auth API)
- Pure Clean Baseline (No bulky 3rd-party player bloat in system partition)
- Complete removal of PhiLauncher, PhiCloudBox, PhiDownloader, PhiNas*, and AuroraStore
- WebPush TV built-in (Drag-and-drop 1-click APK installer via browser)
- 100% stable baseline (ATV Launcher Pro, WebView 119, NextGen Widget, Perfect TvSettings)
"""
import os
import subprocess
import shutil
import sys

def build_v19_pristine_global():
    print("=" * 65)
    print("  Building N1 NextGen TV v19 (Pristine Global Edition)")
    print("=" * 65)

    # 1. Update logo.PARTITION
    shutil.copy2('extracted_webpad/logo.PARTITION', 'build_rom/package/logo.PARTITION')

    # 2. Reset base system.raw.img from pristine base
    src_raw = 'extracted_aml/system.raw.img'
    dst_raw = 'build_rom/system.raw.img'
    print(f"[*] Copying pure official base {src_raw} -> {dst_raw}...")
    shutil.copy2(src_raw, dst_raw)

    # 3. Prepare pristine official keylayout files
    os.makedirs('build_rom/system_root/usr/keylayout', exist_ok=True)
    shutil.copy2('extracted_aml/system_root/usr/keylayout/Generic.kl', 'build_rom/system_root/usr/keylayout/Generic.kl')
    shutil.copy2('extracted_aml/system_root/usr/keylayout/Vendor_0001_Product_0001.kl', 'build_rom/system_root/usr/keylayout/Vendor_0001_Product_0001.kl')

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

    # Generate master ATV database
    print("[*] Generating master ATV Launcher database...")
    sys.path.insert(0, os.path.abspath('tools'))
    from create_master_atv_db import create_master_db
    create_master_db()

    # Prepare optimized bt_stack.conf from extracted_webpad (complete 72-line config)
    os.makedirs('build_rom/system_root/etc/bluetooth', exist_ok=True)
    shutil.copy2('extracted_webpad/system_root/etc/bluetooth/bt_stack.conf', 'build_rom/system_root/etc/bluetooth/bt_stack.conf')

    # Prepare microG permissions XML
    os.makedirs('build_rom/system_root/etc/permissions', exist_ok=True)
    shutil.copy2('tools/microg_permissions.xml', 'build_rom/system_root/etc/permissions/microg_permissions.xml')

    # 5. Assemble Debugfs modifications
    print("[*] Assembling debugfs injection plan...")
    cmds = [
        # --- PHASE 1: Remove Phicomm Bloatware & NAS Components ---
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

        # Remove NAS Launcher, CloudBox & Downloader
        "rm /priv-app/PhiLauncher/PhiLauncher.apk",
        "rmdir /priv-app/PhiLauncher/oat/arm",
        "rmdir /priv-app/PhiLauncher/oat",
        "rmdir /priv-app/PhiLauncher",
        "rm /priv-app/PhiCloudBox/PhiCloudBox.apk",
        "rmdir /priv-app/PhiCloudBox/oat/arm",
        "rmdir /priv-app/PhiCloudBox/oat",
        "rmdir /priv-app/PhiCloudBox",
        "rm /priv-app/PhiDownloader/PhiDownloader.apk",
        "rmdir /priv-app/PhiDownloader/oat/arm",
        "rmdir /priv-app/PhiDownloader/oat",
        "rmdir /priv-app/PhiDownloader",

        # --- PHASE 2: Upgrade WebView to Google WebView v119 ---
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
        "write build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk /priv-app/PhiTvSettings/PhiTvSettings.apk",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk mode 0100644",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk uid 0",
        "set_inode_field /priv-app/PhiTvSettings/PhiTvSettings.apk gid 0",

        # --- Inject Custom NextGen Boot Animation ---
        "rm /media/bootanimation.zip",
        "write build_rom/system_root/media/bootanimation.zip /media/bootanimation.zip",
        "set_inode_field /media/bootanimation.zip mode 0100644",
        "set_inode_field /media/bootanimation.zip uid 0",
        "set_inode_field /media/bootanimation.zip gid 0",

        # --- Inject Safe Sleep Helper & Daemon ---
        "rm /bin/do_sleep.sh",
        "write build_rom/system_root/bin/do_sleep.sh /bin/do_sleep.sh",
        "set_inode_field /bin/do_sleep.sh mode 0100755",
        "set_inode_field /bin/do_sleep.sh uid 0",
        "set_inode_field /bin/do_sleep.sh gid 0",
        "rm /bin/webpadinit.sh",
        "write build_rom/system_root/bin/webpadinit.sh /bin/webpadinit.sh",
        "set_inode_field /bin/webpadinit.sh mode 0100755",
        "set_inode_field /bin/webpadinit.sh uid 0",
        "set_inode_field /bin/webpadinit.sh gid 0",

        "rm /etc/security/mac_permissions.xml",
        "write build_rom/system_root/etc/security/mac_permissions.xml /etc/security/mac_permissions.xml",
        "set_inode_field /etc/security/mac_permissions.xml mode 0100644",
        "set_inode_field /etc/security/mac_permissions.xml uid 0",
        "set_inode_field /etc/security/mac_permissions.xml gid 0",

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

        # --- PHASE 4: Inject microG Core Suite ---
        "mkdir /priv-app/GmsCore",
        "set_inode_field /priv-app/GmsCore mode 040755",
        "write tools/microg_gmscore.apk /priv-app/GmsCore/GmsCore.apk",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk mode 0100644",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk uid 0",
        "set_inode_field /priv-app/GmsCore/GmsCore.apk gid 0",

        "mkdir /priv-app/FakeStore",
        "set_inode_field /priv-app/FakeStore mode 040755",
        "write tools/microg_fakestore.apk /priv-app/FakeStore/FakeStore.apk",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk mode 0100644",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk uid 0",
        "set_inode_field /priv-app/FakeStore/FakeStore.apk gid 0",

        "mkdir /priv-app/GsfProxy",
        "set_inode_field /priv-app/GsfProxy mode 040755",
        "write tools/microg_gsfproxy.apk /priv-app/GsfProxy/GsfProxy.apk",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk mode 0100644",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk uid 0",
        "set_inode_field /priv-app/GsfProxy/GsfProxy.apk gid 0",

        "write build_rom/system_root/etc/permissions/microg_permissions.xml /etc/permissions/microg_permissions.xml",
        "set_inode_field /etc/permissions/microg_permissions.xml mode 0100644",
        "set_inode_field /etc/permissions/microg_permissions.xml uid 0",
        "set_inode_field /etc/permissions/microg_permissions.xml gid 0",

        # --- PHASE 5: Root Daemons & Scripts ---
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

        # --- PHASE 6: Configuration Files ---
        "rm /etc/default_wallpaper.png",
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

        # --- PHASE 7: Clean Tuned build.prop ---
        "rm /build.prop",
        "write build_rom/system_root/build.prop /build.prop",
        "set_inode_field /build.prop mode 0100644",
        "set_inode_field /build.prop uid 0",
        "set_inode_field /build.prop gid 0"
    ]

    cmd_script_path = "tools/debugfs_v18_6_pristine.txt"
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

    print("[*] Verifying critical SELinux attributes...")
    subprocess.run("python tools/verify_xattr.py", shell=True, check=True)

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
    out_img = "N1_NextGen_TV_v19_Global_Release.img"
    if os.path.exists(out_img):
        try:
            with open(out_img, "ab"): pass
        except Exception:
            print(f"[!] Warning: {out_img} is currently opened/locked by USB_Burning_Tool!")
            out_img = "N1_NextGen_TV_v19_Global_Release_Fixed.img"
            print(f"[!] Writing to new image file: {out_img}")

    print(f"[*] Packaging final firmware: {out_img}...")
    subprocess.run(f"python tools/aml_pack.py build_rom/package {out_img}", shell=True, check=True)
    print(f"[+] COMPLETE! Generated: {out_img} ({os.path.getsize(out_img)/1024/1024:.2f} MB)")

if __name__ == '__main__':
    build_v19_pristine_global()
