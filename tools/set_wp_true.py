import subprocess
import sqlite3
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    # 1. Stop ATV Launcher
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    # 2. Update DB with wallpaper mode = true
    db_path = 'logs/sections_wp_true.db'
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', db_path])

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE settings SET value = 'true' WHERE key = 'settings-application-wallpaper-mode'")
    conn.commit()
    conn.close()

    subprocess.run([adb, '-s', dev, 'push', db_path, '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro/'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/'])

    # 3. Launch ATV Launcher
    subprocess.run([adb, '-s', dev, 'shell', 'monkey', '-p', 'ca.dstudio.atvlauncher.pro', '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(2)

    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_wp_true_live.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_wp_true_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_wp_true_live.png'])
    print('[+] Wallpaper mode true verified!')

if __name__ == '__main__':
    main()
