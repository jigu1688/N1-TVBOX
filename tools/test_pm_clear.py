import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

print("[1] Executing standard pm clear...")
subprocess.run([adb, '-s', dev, 'shell', 'pm clear ca.dstudio.atvlauncher.pro'])
time.sleep(1)

print("[2] Launching ATV Launcher Pro...")
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(4)

print("[3] Capturing screen...")
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/pm_clear_launch.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/pm_clear_launch.png', 
                r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\pm_clear_launch.png'])

print("[4] Pulling database if created...")
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/atv_device_db/sections.db'])

print("[+] Done!")
