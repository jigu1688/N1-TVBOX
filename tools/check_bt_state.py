import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])
res = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys bluetooth_manager'], capture_output=True, encoding='utf-8', errors='ignore')
lines = res.stdout.splitlines()
for line in lines:
    if any(k in line.lower() for k in ['bonded', 'device', 'state:', 'enabled:', 'connected', 'profile', 'adapter']):
        print(line)
