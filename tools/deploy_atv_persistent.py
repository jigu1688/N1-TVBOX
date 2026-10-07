import subprocess
import time
import sqlite3
import shutil
import os

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'
    wp = r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\tv_wallpaper_modern_1788019108494.jpg'

    print("[*] Killing ATV Launcher process completely...")
    # First start Projectivy so ATV is no longer active foreground
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'start', '-n', 'com.spocky.projengmenu/com.spocky.projengmenu.ui.home.MainActivity'])
    time.sleep(1)
    
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'killall', '-9', 'ca.dstudio.atvlauncher.pro'])
    time.sleep(1)

    db_path = 'logs/sections_deploy.db'
    shutil.copy2('logs/sections_5col.db', db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("PRAGMA journal_mode = DELETE;")

    sec_media_uuid = '4355e037-d041-442f-b38a-3a31c0a91c7e'
    sec_tools_uuid = 'c28e1d23-4567-4890-abcd-ef0123456789'
    sec_widget_uuid = 'b37bda62-b1b6-4c0a-951c-e7b353919064'

    # Hide widget section
    c.execute(f"UPDATE sections SET [item-height] = 0, [visible] = 0, [rows] = 0 WHERE [uuid] = '{sec_widget_uuid}'")

    # Section 1: 🎬 常用推荐 & 影音娱乐 (Cols = 4)
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

    # Section 2: ⚙️ 系统工具 & 桌面切换 (Cols = 4)
    c.execute("DELETE FROM sections WHERE [uuid] = ?", (sec_tools_uuid,))
    c.execute("""
        INSERT INTO sections ([uuid], [type], [sticky], [primary], [always-visible], [visible], [title], [show-title], [position], [sorting-order], [orientation], [item-height], [rows], [cols])
        VALUES (?, 'APPLICATION_SECTION', 0, 0, 1, 1, '⚙️ 系统工具 & 桌面切换', 1, 2, 'POSITION', 'VERTICAL', 140, 1, 4)
    """, (sec_tools_uuid,))

    # Insert ATV Launcher into tools section
    c.execute("DELETE FROM applications WHERE [package-name] = 'ca.dstudio.atvlauncher.pro'")
    c.execute("""
        INSERT INTO applications ([package-name], [class-name], [version-name], [version-code], [sticky], [show-title], [icon-scale], [show-icon], [show-shadow], [display-mode], [border-radius], [launch-count], [uuid], [section-uuid], [resource-version], [position], [visibility], [state], [background-type], [background-color])
        VALUES ('ca.dstudio.atvlauncher.pro', 'ca.dstudio.atvlauncher.screens.launcher.LauncherActivity', '0.2.1-pro', 26396284, 0, 1, 1, 1, 1, 'DEFAULT', 0, 0, 'atv-uuid-001', ?, 'v1', 3, 'VISIBLE', 'ACTIVE', 'DEFAULT', 0)
    """, (sec_tools_uuid,))

    # Insert Projectivy Launcher into tools section
    c.execute("DELETE FROM applications WHERE [package-name] = 'com.spocky.projengmenu'")
    c.execute("""
        INSERT INTO applications ([package-name], [class-name], [version-name], [version-code], [sticky], [show-title], [icon-scale], [show-icon], [show-shadow], [display-mode], [border-radius], [launch-count], [uuid], [section-uuid], [resource-version], [position], [visibility], [state], [background-type], [background-color])
        VALUES ('com.spocky.projengmenu', 'com.spocky.projengmenu.ui.home.MainActivity', '4.71', 95, 0, 1, 1, 1, 1, 'DEFAULT', 0, 0, 'proj-uuid-001', ?, 'v1', 2, 'VISIBLE', 'ACTIVE', 'DEFAULT', 0)
    """, (sec_tools_uuid,))

    # Row 1 Apps:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.nextgen.webpush'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.hpplay.happyplay.aw'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 2, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.tv.qx'", (sec_media_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 3, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.droidlogic.FileBrower'", (sec_media_uuid,))

    # Row 2 Apps:
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 0, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.xiaobaifile.tv'", (sec_tools_uuid,))
    c.execute("UPDATE applications SET [section-uuid] = ?, [position] = 1, [visibility] = 'VISIBLE' WHERE [package-name] = 'com.android.settings'", (sec_tools_uuid,))

    # Ensure wallpaper mode is false
    c.execute("UPDATE settings SET value = 'false' WHERE key = 'settings-application-wallpaper-mode'")

    conn.commit()
    conn.close()

    # Clean target files on device and push
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db*'])
    files_dir = '/data/data/ca.dstudio.atvlauncher.pro/files'
    subprocess.run([adb, '-s', dev, 'shell', f'mkdir -p {files_dir}'])
    subprocess.run([adb, '-s', dev, 'push', wp, f'{files_dir}/wallpaper-source.png'])
    subprocess.run([adb, '-s', dev, 'push', wp, f'{files_dir}/wallpaper-updated.png'])
    subprocess.run([adb, '-s', dev, 'push', db_path, '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])

    # Fix permissions
    subprocess.run([adb, '-s', dev, 'shell', 'chown -R 10025:10025 /data/data/ca.dstudio.atvlauncher.pro/'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/'])

    # Now Start ATV Launcher
    time.sleep(1)
    subprocess.run([adb, '-s', dev, 'shell', 'monkey', '-p', 'ca.dstudio.atvlauncher.pro', '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(3)

    # Capture Screen
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_fresh_verified.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_fresh_verified.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_fresh_verified.png'])
    print('[+] Successfully verified!')

if __name__ == '__main__':
    main()
