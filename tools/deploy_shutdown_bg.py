import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.118:5555'

subprocess.run([adb, 'connect', dev])
time.sleep(1)

apk_path = r'tools\re_tools\PhiTvSettings_Signed.apk'
print(f'[*] Pushing {apk_path} to /sdcard/PhiTvSettings.apk...')
r1 = subprocess.run([adb, '-s', dev, 'push', apk_path, '/sdcard/PhiTvSettings.apk'], capture_output=True, text=True)
print(r1.stdout, r1.stderr)

print('[*] Installing to /system/priv-app/PhiTvSettings/PhiTvSettings.apk...')
install_cmd = """
mount -o remount,rw /system
cp /sdcard/PhiTvSettings.apk /system/priv-app/PhiTvSettings/PhiTvSettings.apk
chmod 644 /system/priv-app/PhiTvSettings/PhiTvSettings.apk
chown root:root /system/priv-app/PhiTvSettings/PhiTvSettings.apk
mount -o remount,ro /system
ls -l /system/priv-app/PhiTvSettings/PhiTvSettings.apk
"""
r2 = subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', install_cmd], capture_output=True, text=True)
print(r2.stdout, r2.stderr)

print('[*] Launching ShutdownActivity on TV screen...')
r3 = subprocess.run([adb, '-s', dev, 'shell', 'am start -n com.android.tv.settings/.ShutdownActivity'], capture_output=True, text=True)
print(r3.stdout, r3.stderr)

time.sleep(2)
print('[*] Capturing TV screen of the new shutdown menu...')
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/shutdown_screen.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/shutdown_screen.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\live_shutdown_screen.png'])

print('[+] Done!')
