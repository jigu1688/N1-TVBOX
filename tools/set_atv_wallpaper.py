import subprocess
import time
import sqlite3

def clean_layout():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    subprocess.run([adb, '-s', dev, 'shell', 'killall ca.dstudio.atvlauncher.pro'])
    time.sleep(0.5)
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/sections_clean.db'])

    conn = sqlite3.connect('logs/sections_clean.db')
    c = conn.cursor()

    sec_media_uuid = '4355e037-d041-442f-b38a-3a31c0a91c7e'
    sec_tools_uuid = 'c28e1d23-4567-4890-abcd-ef0123456789'
    sec_widget_uuid = 'b37bda62-b1b6-4c0a-951c-e7b353919064'

    # Hide widget section
    c.execute(f"UPDATE sections SET [item-height] = 0, [visible] = 0, [rows] = 0 WHERE [uuid] = '{sec_widget_uuid}'")

    # Section 1: 🎬 影音娱乐 (Exact 4 columns)
    c.execute(f"""
        UPDATE sections 
        SET [title] = '🎬 影音娱乐', 
            [show-title] = 1, 
            [item-height] = 180, 
            [rows] = 1, 
            [cols] = 4, 
            [position] = 1,
            [visible] = 1
        WHERE [uuid] = '{sec_media_uuid}'
    """)

    # Section 2: ⚙️ 实用工具 (Exact 4 columns)
    c.execute("DELETE FROM sections WHERE [uuid] = ?", (sec_tools_uuid,))
    c.execute("""
        INSERT INTO sections ([uuid], [type], [sticky], [primary], [always-visible], [visible], [title], [show-title], [position], [sorting-order], [orientation], [item-height], [rows], [cols])
        VALUES (?, 'APPLICATION_SECTION', 0, 0, 1, 1, '⚙️ 实用工具', 1, 2, 'POSITION', 'VERTICAL', 140, 1, 4)
    """, (sec_tools_uuid,))

    # Insert ATV Launcher with exact class-name into tools section
    c.execute("DELETE FROM applications WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'")
    c.execute("""
        INSERT INTO applications ([package-name], [class-name], [version-name], [version-code], [sticky], [show-title], [icon-scale], [show-icon], [show-shadow], [display-mode], [border-radius], [launch-count], [uuid], [section-uuid], [resource-version], [position], [visibility], [state], [background-type], [background-color])
        VALUES ('ca.dstudio.atvlauncher.pro', 'ca.dstudio.atvlauncher.screens.launcher.LauncherActivity', '0.2.1-pro', 26396284, 0, 1, 1, 1, 1, 'DEFAULT', 0, 0, 'atv-launcher-uuid-001', ?, 'v1', 2, 'VISIBLE', 'ACTIVE', 'DEFAULT', 0)
    """, (sec_tools_uuid,))

    # Row 1 Apps (Exact 4 items):
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.nextgen.webpush'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.hpplay.happyplay.aw'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.tv.qx'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.droidlogic.FileBrower'", (sec_media_uuid,))

    # Row 2 Apps (Exact 3 items):
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.xiaobaifile.tv'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.android.settings'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'", (sec_tools_uuid,))

    # Ensure wallpaper mode is false
    c.execute("UPDATE settings SET value = 'false' WHERE key = 'settings-application-wallpaper-mode'")

    conn.commit()
    conn.close()

    subprocess.run([adb, '-s', dev, 'push', 'logs/sections_clean.db', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-shm'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 660 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
    subprocess.run([adb, '-s', dev, 'shell', 'chown 10025:10025 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])

    # Restart launcher
    subprocess.run([adb, '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
    time.sleep(2)

    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_perfect_2rows.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_perfect_2rows.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_perfect_2rows.png'])
    print('[+] Complete!')

if __name__ == '__main__':
    clean_layout()
