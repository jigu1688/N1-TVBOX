import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

p = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows'], capture_output=True)
for line in p.stdout.decode('utf-8', errors='ignore').splitlines():
    if 'mCurrentFocus' in line or 'mFocusedApp' in line:
        print(line)
