import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.118:5555'

subprocess.run([adb, 'connect', dev])
time.sleep(1)

# Check boot animation
print('[*] Checking /system/media/bootanimation.zip on device...')
r = subprocess.run([adb, '-s', dev, 'shell', 'ls -l /system/media/boot* /system/media/shut*'], capture_output=True, text=True)
print(r.stdout)

# Check boot partition
print('[*] Checking boot / recovery partitions on device...')
r2 = subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', 'ls -l /dev/block/by-name/ || ls -l /dev/block/boot* /dev/block/logo*'], capture_output=True, text=True)
print(r2.stdout)
