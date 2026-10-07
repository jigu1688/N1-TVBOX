import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# 1. Clear ATV Launcher data
print("[*] Clearing ATV Launcher data & permissions...")
subprocess.run([adb, '-s', dev, 'shell', 'pm clear ca.dstudio.atvlauncher.pro'], capture_output=True)

# 2. Grant permissions
subprocess.run([adb, '-s', dev, 'shell', 'appops set ca.dstudio.atvlauncher.pro BIND_APPWIDGET allow'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'pm grant ca.dstudio.atvlauncher.pro android.permission.BIND_APPWIDGET'], capture_output=True)

# 3. Launch ATV Launcher
print("[*] Launching ATV Launcher via category.HOME...")
subprocess.run([adb, '-s', dev, 'shell', 'am start -a android.intent.action.MAIN -c android.intent.category.HOME'], capture_output=True)

time.sleep(3)
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_desktop_fixed.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_desktop_fixed.png', 'tools/screen_desktop_fixed.png'], capture_output=True)
print("[+] Captured tools/screen_desktop_fixed.png")
