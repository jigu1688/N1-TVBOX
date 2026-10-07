import subprocess
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    print("[1] Opening Settings to release ATV Launcher from foreground...")
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'start', '-n', 'com.android.settings/.Settings'])
    time.sleep(1)

    print("[2] Disabling ATV launcher component and force stopping...")
    subprocess.run([adb, '-s', dev, 'shell', 'pm', 'disable', 'ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'killall', '-9', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    print("[3] Removing WAL/SHM and pushing master sections.db...")
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db*'])
    subprocess.run([adb, '-s', dev, 'push', 'build_rom/system_root/etc/atvlauncher/sections.db', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    
    # Verify file size on device
    r = subprocess.run([adb, '-s', dev, 'shell', 'ls -la /data/data/ca.dstudio.atvlauncher.pro/databases/'], capture_output=True, text=True)
    print("Database on device:", r.stdout)

    print("[4] Pushing wallpaper...")
    wp = 'build_rom/system_root/etc/default_wallpaper.png'
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-source.png'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-updated.png'])

    print("[5] Fixing permissions...")
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro'])

    print("[6] Re-enabling ATV Launcher and launching...")
    subprocess.run([adb, '-s', dev, 'shell', 'pm', 'enable', 'ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
    time.sleep(0.5)
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'start', '-n', 'ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
    time.sleep(3)

    print("[7] Capturing screen...")
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/safe_switch_live.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/safe_switch_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\safe_switch_live.png'])
    print("[+] Done!")

if __name__ == '__main__':
    main()
