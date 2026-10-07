import subprocess
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'
    wp = r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\tv_wallpaper_modern_1788019108494.jpg'

    # 1. Push to ATV Launcher files and system wallpaper
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper.jpg'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper.png'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/system/users/0/wallpaper'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/files/'])

    # 2. SQLite updates
    sql1 = "UPDATE settings SET value = 'true' WHERE key = 'settings-application-wallpaper-mode';"
    sql2 = "UPDATE applications SET state = 'DISABLED', [section-uuid] = NULL, visibility = 'HIDDEN' WHERE [package-name] = 'ca.dstudio.atvlauncher.pro';"
    
    subprocess.run([adb, '-s', dev, 'shell', 'sqlite3', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', sql1])
    subprocess.run([adb, '-s', dev, 'shell', 'sqlite3', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', sql2])

    # 3. Restart ATV Launcher
    subprocess.run([adb, '-s', dev, 'shell', 'killall', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1.5)
    subprocess.run([adb, '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
    time.sleep(2)

    # 4. Capture screenshot
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_modern_v2.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_modern_v2.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_modern_v2.png'])
    print('[+] Done!')

if __name__ == '__main__':
    main()
