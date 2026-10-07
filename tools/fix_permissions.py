import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Fix owner and permissions for ATV launcher data directory
subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', 'chown -R u0_a25:u0_a25 /data/data/ca.dstudio.atvlauncher.pro/'])
subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', 'chmod -R 777 /data/data/ca.dstudio.atvlauncher.pro/databases/'])

# Restart ATV Launcher
subprocess.run([adb, '-s', dev, 'shell', 'am force-stop ca.dstudio.atvlauncher.pro'])
time.sleep(1)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(3)

# Capture screen
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/permission_fixed.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/permission_fixed.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\permission_fixed.png'])

print("[+] Fixed permissions and restarted ATV Launcher!")
