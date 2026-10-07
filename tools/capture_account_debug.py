import subprocess
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

subprocess.run([adb, 'connect', dev], capture_output=True, text=True)

# 1. Capture screen
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_account.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_account.png', 'tools/screen_account.png'], capture_output=True)
print('[+] Pulled tools/screen_account.png')

# 2. Get dumpsys window
res_win = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows'], capture_output=True, text=True)
for line in res_win.stdout.splitlines():
    if 'mCurrentFocus' in line or 'mFocusedApp' in line:
        print(line)

# 3. Check recent logcat
res_log = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d | tail -n 80'], capture_output=True, text=True)
print('\nRecent logcat:')
for line in res_log.stdout.splitlines()[-40:]:
    print(line)
