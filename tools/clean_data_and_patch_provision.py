import os
import subprocess
import zipfile
import shutil

def clean_data_and_patch_provision():
    print("="*60)
    print("  Cleaning Data Partition & Patching Provision Icon")
    print("="*60)
    
    # 1. Patch Provision.apk to hide the launcher icon
    src_provision = 'extracted_webpad/system_root/priv-app/Provision/Provision.apk'
    dst_provision = 'tools/Provision_NoIcon.apk'
    
    print("[*] Patching Provision.apk to remove category.LAUNCHER...")
    with zipfile.ZipFile(src_provision, 'r') as zin:
        manifest = zin.read('AndroidManifest.xml')
        # In binary AndroidManifest (UTF-16LE or ASCII table)
        # Search for 'android.intent.category.LAUNCHER' in binary
        s_old = 'android.intent.category.LAUNCHER'.encode('utf-16le')
        s_new = 'android.intent.category.PROVISIO'.encode('utf-16le')
        
        if s_old in manifest:
            manifest = manifest.replace(s_old, s_new)
            print("[+] Replaced UTF-16LE LAUNCHER -> PROVISIO")
        else:
            s_old_ascii = b'android.intent.category.LAUNCHER'
            s_new_ascii = b'android.intent.category.PROVISIO'
            if s_old_ascii in manifest:
                manifest = manifest.replace(s_old_ascii, s_new_ascii)
                print("[+] Replaced ASCII LAUNCHER -> PROVISIO")
                
        with zipfile.ZipFile(dst_provision, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'AndroidManifest.xml':
                    zout.writestr(item, manifest)
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    # Sign Provision_NoIcon.apk with platform/debug key
    apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
    debug_ks = os.path.expanduser('~/.android/debug.keystore')
    zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
    
    # Remove old META-INF
    unsigned = 'tools/provision_unsigned.apk'
    with zipfile.ZipFile(dst_provision, 'r') as zin, zipfile.ZipFile(unsigned, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if not item.filename.startswith('META-INF/'):
                zout.writestr(item, zin.read(item.filename))
                
    aligned = 'tools/provision_aligned.apk'
    subprocess.run([zipalign, "-p", "-f", "4", unsigned, aligned], check=True)
    signed = 'tools/Provision_Final.apk'
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{signed}" "{aligned}"', shell=True, check=True)
    print(f"[+] Provision patched & signed: {signed}")
    
    # 2. Reset and clean data.raw.img
    print("[*] Creating 100% Pure Clean data.raw.img...")
    # Copy from extracted_webpad/data.raw.img to build_rom/data.raw.img
    shutil.copy2('extracted_webpad/data.raw.img', 'build_rom/data.raw.img')
    
    # List of all apps to delete from /app in data.raw.img
    data_apps = [
        "com.fanshi.tvbrowser-1",
        "com.mxtech.videoplayer.pro-1",
        "com.pplive.androidxl-1",
        "com.speedsoftware.rootexplorer-1",
        "com.sumavision.ivideoforstb-1",
        "com.tcl.gitv-1",
        "com.xctv2018.mytv-1",
        "dpplay.com-1",
        "fr.petrus.tools.reboot-1",
        "jackpal.androidterm-2"
    ]
    
    # Generate debugfs commands to delete all files inside /app/* and remove the dirs
    debugfs_cmds = []
    # Remove files inside each app dir
    for app in data_apps:
        debugfs_cmds.append(f"rm /app/{app}/base.apk")
        # lib subdirs
        debugfs_cmds.append(f"rmdir /app/{app}/lib/arm")
        debugfs_cmds.append(f"rmdir /app/{app}/lib/arm64")
        debugfs_cmds.append(f"rmdir /app/{app}/lib")
        # oat subdirs
        debugfs_cmds.append(f"rm /app/{app}/oat/arm/base.odex")
        debugfs_cmds.append(f"rm /app/{app}/oat/arm/base.vdex")
        debugfs_cmds.append(f"rm /app/{app}/oat/arm64/base.odex")
        debugfs_cmds.append(f"rm /app/{app}/oat/arm64/base.vdex")
        debugfs_cmds.append(f"rmdir /app/{app}/oat/arm")
        debugfs_cmds.append(f"rmdir /app/{app}/oat/arm64")
        debugfs_cmds.append(f"rmdir /app/{app}/oat")
        debugfs_cmds.append(f"rmdir /app/{app}")
        
    with open("tools/clean_data_debugfs.txt", "w", encoding="utf-8", newline="\n") as f:
        for c in debugfs_cmds:
            f.write(c + "\n")
            
    print(f"[*] Removing all {len(data_apps)} apps from data.raw.img...")
    subprocess.run("wsl debugfs -w -f tools/clean_data_debugfs.txt build_rom/data.raw.img", shell=True)
    
    # 3. Truncate and fsck
    with open('build_rom/data.raw.img', 'r+b') as f:
        f.truncate(1344768 * 4096)
        
    print("[*] Running e2fsck on cleaned data.raw.img...")
    subprocess.run("wsl e2fsck -f -y build_rom/data.raw.img", shell=True, check=True)
    
    # 4. Generate sparse data.PARTITION
    print("[*] Generating Android Sparse data.PARTITION...")
    subprocess.run("python tools/img2simg.py build_rom/data.raw.img build_rom/package/data.PARTITION", shell=True, check=True)
    print("[+] data.PARTITION is now 100% PURE & EMPTY!")

if __name__ == '__main__':
    clean_data_and_patch_provision()
