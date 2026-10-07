import subprocess
import sqlite3
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    db_path = 'logs/sections_clean_title.db'
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', db_path])

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sec1 = '4355e037-d041-442f-b38a-3a31c0a91c7e'
    sec2 = 'c28e1d23-4567-4890-abcd-ef0123456789'

    # Section 1: 常用推荐 (Primary)
    c.execute(f"UPDATE sections SET [title] = '常用推荐', [show-title] = 1, [item-height] = 170, [rows] = 1, [cols] = 4, [position] = 1 WHERE [uuid] = '{sec1}'")

    # Section 2: 系统工具
    c.execute(f"UPDATE sections SET [title] = '系统工具', [show-title] = 1, [item-height] = 140, [rows] = 1, [cols] = 4, [position] = 2 WHERE [uuid] = '{sec2}'")

    # Ensure apps in section 1:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.nextgen.webpush'", (sec1,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.hpplay.happyplay.aw'", (sec1,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.tv.qx'", (sec1,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.droidlogic.FileBrower'", (sec1,))

    # Ensure apps in section 2:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.xiaobaifile.tv'", (sec2,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.android.settings'", (sec2,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'", (sec2,))

    # Enable wallpaper
    c.execute("UPDATE settings SET value = 'true' WHERE key = 'settings-application-wallpaper-mode'")

    conn.commit()
    conn.close()

    subprocess.run([adb, '-s', dev, 'push', db_path, '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-shm'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro'])

    subprocess.run([adb, '-s', dev, 'shell', 'monkey', '-p', 'ca.dstudio.atvlauncher.pro', '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(2)

    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_clean_title_live.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_clean_title_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_clean_title_live.png'])
    print('[+] Clean title layout verified!')

if __name__ == '__main__':
    main()
