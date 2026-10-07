import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.118:5555'

subprocess.run([adb, 'connect', dev])
time.sleep(1)

print('[*] Pushing bootanimation_custom.zip to /sdcard/...')
r1 = subprocess.run([adb, '-s', dev, 'push', 'tools/bootanimation_custom.zip', '/sdcard/bootanimation.zip'], capture_output=True, text=True)
print(r1.stdout, r1.stderr)

print('[*] Remounting /system and installing /system/media/bootanimation.zip...')
install_cmd = """
mount -o remount,rw /system
cp /sdcard/bootanimation.zip /system/media/bootanimation.zip
chmod 644 /system/media/bootanimation.zip
chown root:root /system/media/bootanimation.zip
mount -o remount,ro /system
ls -l /system/media/bootanimation.zip
"""
r2 = subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', install_cmd], capture_output=True, text=True)
print(r2.stdout, r2.stderr)

print('[+] Installation completed!')
