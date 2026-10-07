import subprocess
import sqlite3
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

subprocess.run([adb, '-s', dev, 'shell', 'su -c "cp /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db /sdcard/sections.db"'])
subprocess.run([adb, '-s', dev, 'shell', 'su -c "chmod 666 /sdcard/sections.db"'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/sections.db', 'logs/atv_device_db/sections.db'])

db_path = 'logs/atv_device_db/sections.db'
if os.path.exists(db_path):
    print("Pulled DB size:", os.path.getsize(db_path))
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print("\n--- Sections Table ---")
    c.execute("SELECT uuid, title, visible, [always-visible], [primary], rows, cols, [item-height] FROM sections")
    for r in c.fetchall():
        print(r)
        
    print("\n--- Applications Table ---")
    c.execute("SELECT [package-name], [section-uuid], [position], [border-radius], [display-mode], [background-color] FROM applications")
    for r in c.fetchall():
        print(r)
        
    print("\n--- Settings Table ---")
    c.execute("SELECT [key], [value] FROM settings")
    for r in c.fetchall():
        print(r)
    conn.close()
else:
    print("Database file NOT found on device!")
