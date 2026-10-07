import subprocess
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

# 1. Connect
subprocess.run([adb, 'connect', dev], capture_output=True)

# 2. Screencap
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_cur.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_cur.png', 'tools/screen_cur.png'], capture_output=True)

if os.path.exists('tools/screen_cur.png'):
    print(f'[+] Pulled screen_cur.png: {os.path.getsize("tools/screen_cur.png")} bytes')
else:
    print('[!] Failed to pull screenshot')

# 3. Check installed packages
p = subprocess.run([adb, '-s', dev, 'shell', 'pm list packages -f'], capture_output=True)
stdout_str = p.stdout.decode('utf-8', errors='ignore')
print('\n[System packages found]:')
for line in stdout_str.splitlines():
    if any(k in line.lower() for k in ['smarttube', 'fdroid', 'microg', 'cloudbox', 'downloader', 'nas', 'aurora']):
        print(' ', line)
