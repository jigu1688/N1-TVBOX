import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

subprocess.run([adb, 'connect', dev], capture_output=True)

# 1. Push patched PhiTvSettings.apk to live device
print("[*] Pushing patched PhiTvSettings.apk to device...")
subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'], capture_output=True)
subprocess.run([adb, '-s', dev, 'push', 'build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk', '/system/priv-app/PhiTvSettings/PhiTvSettings.apk'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'chmod 644 /system/priv-app/PhiTvSettings/PhiTvSettings.apk'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'chown 0:0 /system/priv-app/PhiTvSettings/PhiTvSettings.apk'], capture_output=True)

# 2. Clear previous process
subprocess.run([adb, '-s', dev, 'shell', 'am force-stop com.android.tv.settings'], capture_output=True)

time.sleep(1)

# 3. Simulate short press on power button (input keyevent 26)
print("[*] Simulating short press on remote POWER button (input keyevent 26)...")
subprocess.run([adb, '-s', dev, 'logcat', '-c'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 26'], capture_output=True)

time.sleep(2)

# 4. Capture screenshot
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_power_menu_live.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_power_menu_live.png', 'tools/screen_power_menu_live.png'], capture_output=True)
print("[+] Captured tools/screen_power_menu_live.png")
