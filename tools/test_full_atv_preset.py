import subprocess
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    # 1. Stop ATV
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    # 2. Push database, wallpaper, and matching backup.xml
    db = 'build_rom/system_root/etc/atvlauncher/sections.db'
    wp = 'build_rom/system_root/etc/default_wallpaper.png'
    
    subprocess.run([adb, '-s', dev, 'push', db, '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-source.png'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper-updated.png'])
    
    # Also write matching backup.xml with the exact ID
    backup_xml = """<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <string name="id">505861458</string>
</map>
"""
    with open('logs/backup_preset.xml', 'w', encoding='utf-8') as f:
        f.write(backup_xml)
    subprocess.run([adb, '-s', dev, 'push', 'logs/backup_preset.xml', '/data/data/ca.dstudio.atvlauncher.pro/shared_prefs/backup.xml'])

    # 3. Clean wal files and fix permissions
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-shm'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro'])

    # 4. Start ATV
    subprocess.run([adb, '-s', dev, 'shell', 'monkey', '-p', 'ca.dstudio.atvlauncher.pro', '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(3)

    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_full_preset_test.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_full_preset_test.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_full_preset_test.png'])
    print('[+] Full preset tested!')

if __name__ == '__main__':
    main()
