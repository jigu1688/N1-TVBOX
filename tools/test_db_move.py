import subprocess
import time
import sqlite3

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Pull db
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/manual_test.db'])

# Update SeleneTV section-uuid to Media Section in manual_test.db
conn = sqlite3.connect('logs/manual_test.db')
c = conn.cursor()
c.execute("UPDATE applications SET [section-uuid] = '4355e037-d041-442f-b38a-3a31c0a91c7e', [position] = 2 WHERE [package-name] = 'org.moontechlab.selenetv'")
conn.commit()
conn.close()

# Stop launcher, push db, start launcher
subprocess.run([adb, '-s', dev, 'shell', 'am force-stop ca.dstudio.atvlauncher.pro'])
subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db*'])
subprocess.run([adb, '-s', dev, 'push', 'logs/manual_test.db', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
subprocess.run([adb, '-s', dev, 'shell', 'chmod 777 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(3)

# Screencap
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/selene_in_media.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/selene_in_media.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\selene_in_media.png'])
print("[+] Finished!")
