import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'
subprocess.run([adb, 'connect', dev])
r = subprocess.run([adb, '-s', dev, 'shell', 'for f in /system/etc/init/*.rc; do echo "=== $f ==="; cat $f; done'], capture_output=True, text=True)
print(r.stdout)
