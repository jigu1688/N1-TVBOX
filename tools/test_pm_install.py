import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

subprocess.run([adb, 'connect', dev])
subprocess.run([adb, '-s', dev, 'shell', 'su -c \'/system/xbin/supolicy --live "permissive zygote;"\''])
r = subprocess.run([adb, '-s', dev, 'shell', 'su -c \'pm install -r /sdcard/Download/SeleneTV-v1.4.6-arm64-v8a.apk\''], capture_output=True, text=True)
print('pm install after permissive zygote:', r.returncode, repr(r.stdout), repr(r.stderr))
