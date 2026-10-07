import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

subprocess.run([adb, 'connect', dev])
cmd = "su 10029 /system/xbin/su -c 'pm install -r /sdcard/Download/SeleneTV-v1.4.6-arm64-v8a.apk'"
r = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
print('run pm install as 10029:', r.returncode, repr(r.stdout), repr(r.stderr))
