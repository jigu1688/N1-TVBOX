import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])
cmd = 'strings /system/lib64/libinput.so | grep -E "WAKE|FUNCTION|VIRTUAL|FALLBACK"'
res = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
print(res.stdout)
