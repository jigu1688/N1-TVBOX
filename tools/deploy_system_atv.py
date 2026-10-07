import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'
apk = 'tools/re_tools/ATVLauncher_Custom_Hardcoded.apk'

# 1. Remount system rw
subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'])

# 2. Push directly to /system/app/ATVLauncher/ATVLauncher.apk
subprocess.run([adb, '-s', dev, 'push', apk, '/system/app/ATVLauncher/ATVLauncher.apk'])
subprocess.run([adb, '-s', dev, 'shell', 'chmod 644 /system/app/ATVLauncher/ATVLauncher.apk'])

# 3. Clean up /data/app user-installed override if any
subprocess.run([adb, '-s', dev, 'shell', 'rm -rf /data/app/ca.dstudio.atvlauncher.pro*'])
subprocess.run([adb, '-s', dev, 'shell', 'rm -rf /data/dalvik-cache/arm64/*ca.dstudio.atvlauncher*'])
subprocess.run([adb, '-s', dev, 'shell', 'rm -rf /data/dalvik-cache/arm/*ca.dstudio.atvlauncher*'])

# 4. Restart ATV Launcher
subprocess.run([adb, '-s', dev, 'shell', 'am force-stop ca.dstudio.atvlauncher.pro'])
time.sleep(1)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(3)

print("[+] Successfully deployed newest ATV Launcher to /system/app/!")
