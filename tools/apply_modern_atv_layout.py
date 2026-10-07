import subprocess
import sqlite3
import time
import os

def apply_layout():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'
    wp = r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\tv_wallpaper_modern_1788019108494.jpg'

    # 1. Push wallpaper
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/system/users/0/wallpaper'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 600 /data/system/users/0/wallpaper'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown system:system /data/system/users/0/wallpaper'])
    
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper.jpg'])
    subprocess.run([adb, '-s', dev, 'push', wp, '/data/data/ca.dstudio.atvlauncher.pro/files/wallpaper.png'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/files/'])

    # 2. Stop launcher
    subprocess.run([adb, '-s', dev, 'shell', 'killall ca.dstudio.atvlauncher.pro'])
    time.sleep(0.5)

    # 3. Pull DB
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/sections_edit.db'])

    # 4. Modify SQLite DB
    conn = sqlite3.connect('logs/sections_edit.db')
    c = conn.cursor()

    # Enable wallpaper mode
    c.execute("UPDATE settings SET value = 'true' WHERE key = 'settings-application-wallpaper-mode'")

    # Delete / completely disable ATV Launcher tile
    c.execute("DELETE FROM applications WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'")

    # Sections UUIDs
    sec_media_uuid = '4355e037-d041-442f-b38a-3a31c0a91c7e'
    sec_tools_uuid = 'c28e1d23-4567-4890-abcd-ef0123456789'
    sec_widget_uuid = 'b37bda62-b1b6-4c0a-951c-e7b353919064'

    # Hide empty widget gap
    c.execute(f"UPDATE sections SET [item-height] = 60, [visible] = 0, [rows] = 0 WHERE [uuid] = '{sec_widget_uuid}'")

    # Section 1: 🎬 影音娱乐 (Featured Row)
    c.execute(f"""
        UPDATE sections 
        SET [title] = '🎬 影音娱乐', 
            [show-title] = 1, 
            [item-height] = 185, 
            [rows] = 1, 
            [cols] = 4, 
            [position] = 1,
            [visible] = 1
        WHERE [uuid] = '{sec_media_uuid}'
    """)

    # Section 2: ⚙️ 实用工具
    c.execute("DELETE FROM sections WHERE [uuid] = ?", (sec_tools_uuid,))
    c.execute("""
        INSERT INTO sections ([uuid], [type], [sticky], [primary], [always-visible], [visible], [title], [show-title], [position], [sorting-order], [orientation], [item-height], [rows], [cols])
        VALUES (?, 'APPLICATION_SECTION', 0, 0, 1, 1, '⚙️ 实用工具', 1, 2, 'POSITION', 'VERTICAL', 145, 1, 4)
    """, (sec_tools_uuid,))

    # Applications assignment & styling:
    # Row 1:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.nextgen.webpush'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.hpplay.happyplay.aw'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.tv.qx'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.droidlogic.FileBrower'", (sec_media_uuid,))

    # Row 2:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.xiaobaifile.tv'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.android.settings'", (sec_tools_uuid,))

    conn.commit()
    conn.close()

    # 5. Push DB
    subprocess.run([adb, '-s', dev, 'push', 'logs/sections_edit.db', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-shm'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 660 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown 10025:10025 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])

    # Restart launcher
    subprocess.run([adb, '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
    time.sleep(2)

    # Capture screen
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_modern_final.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_modern_final.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_modern_final.png'])
    print('[+] Complete!')

if __name__ == '__main__':
    apply_layout()
