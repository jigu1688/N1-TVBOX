import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

p = subprocess.run([adb, '-s', dev, 'shell', 'ls -la /system/app/ATVLauncher'], capture_output=True)
print("ls /system/app/ATVLauncher:")
print(p.stdout.decode('utf-8', errors='ignore'))

p_pm = subprocess.run([adb, '-s', dev, 'shell', 'pm list packages | grep dstudio'], capture_output=True)
print("pm list packages dstudio:")
print(p_pm.stdout.decode('utf-8', errors='ignore'))
