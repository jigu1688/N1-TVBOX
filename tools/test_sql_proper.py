import sqlite3
import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Pull db from device
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'local_test.db'])

conn = sqlite3.connect('local_test.db')
c = conn.cursor()

print("--- Current Database Rows ---")
for row in c.execute('SELECT uuid, type, title, "show-title" FROM sections'):
    print(row)

# Test 1: Hide Widget Section Title, Show Applications Section Title, Show Media Section Title
c.execute('UPDATE sections SET "show-title" = 0 WHERE type = "WIDGET_SECTION"')
c.execute('UPDATE sections SET "show-title" = 1 WHERE type = "APPLICATION_SECTION"')
conn.commit()

print("--- After Update Rows ---")
for row in c.execute('SELECT uuid, type, title, "show-title" FROM sections'):
    print(row)
conn.close()

# Push db to device
subprocess.run([adb, '-s', dev, 'push', 'local_test.db', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
subprocess.run([adb, '-s', dev, 'shell', 'chmod 660 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])

# Restart ATV
subprocess.run([adb, '-s', dev, 'shell', 'am force-stop ca.dstudio.atvlauncher.pro'])
time.sleep(1)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])

time.sleep(3)
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/desktop_hide_widget_success.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/desktop_hide_widget_success.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\desktop_hide_widget_success.png'])
