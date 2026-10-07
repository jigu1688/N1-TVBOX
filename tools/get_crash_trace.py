import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

r = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d -s AndroidRuntime:E'], capture_output=True, text=True)
print(r.stdout[-2500:])
