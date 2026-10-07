import subprocess
import sqlite3
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    # Stop ATV
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    db_path = 'logs/sections_polish.db'
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', db_path])

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Update cards with rounded corners (border-radius = 16) and subtle elevation shadow
    c.execute("""
        UPDATE applications 
        SET [border-radius] = 16, 
            [show-shadow] = 1,
            [show-title] = 1
    """)

    # Ensure 2 clean categories:
    sec_media_uuid = '4355e037-d041-442f-b38a-3a31c0a91c7e'
    sec_tools_uuid = 'c28e1d23-4567-4890-abcd-ef0123456789'

    # Section 1: 🎬 常用推荐 & 影音娱乐
    c.execute(f"""
        UPDATE sections 
        SET [title] = '🎬 常用推荐 & 影音娱乐', 
            [show-title] = 1, 
            [item-height] = 175, 
            [rows] = 1, 
            [cols] = 4, 
            [position] = 1,
            [visible] = 1
        WHERE [uuid] = '{sec_media_uuid}'
    """)

    # Section 2: ⚙️ 系统工具 & 桌面切换
    c.execute(f"""
        UPDATE sections 
        SET [title] = '⚙️ 系统工具 & 桌面切换', 
            [show-title] = 1, 
            [item-height] = 140, 
            [rows] = 1, 
            [cols] = 4, 
            [position] = 2,
            [visible] = 1
        WHERE [uuid] = '{sec_tools_uuid}'
    """)

    # Row 1 Apps:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.nextgen.webpush'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.hpplay.happyplay.aw'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.tv.qx'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.droidlogic.FileBrower'", (sec_media_uuid,))

    # Row 2 Apps:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.xiaobaifile.tv'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.android.settings'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.spocky.projengmenu'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'", (sec_tools_uuid,))

    conn.commit()
    conn.close()

    subprocess.run([adb, '-s', dev, 'push', db_path, '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro/'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/'])

    # Start ATV
    subprocess.run([adb, '-s', dev, 'shell', 'monkey', '-p', 'ca.dstudio.atvlauncher.pro', '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(2)

    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_polished_live.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_polished_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_polished_live.png'])
    print('[+] Polished layout live on device!')

if __name__ == '__main__':
    main()
