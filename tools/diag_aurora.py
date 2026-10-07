import subprocess
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

subprocess.run([adb, 'connect', dev], capture_output=True, text=True)

# 1. Capture screen
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_aurora.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_aurora.png', 'tools/screen_aurora.png'], capture_output=True)
print('[+] Pulled tools/screen_aurora.png')

# 2. Check Aurora Store package version
res_pkg = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys package com.aurora.store'], capture_output=True, text=True, errors='ignore')
for line in res_pkg.stdout.splitlines():
    if 'versionName' in line or 'versionCode' in line:
        print(line)

# 3. Check recent logcat for AuroraStore
res_log = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d'], capture_output=True, text=True, errors='ignore')
print('\nRecent Aurora logs:')
for line in res_log.stdout.splitlines()[-60:]:
    if any(k in line.lower() for k in ['aurora', 'auth', 'token', '404', 'denied', 'exception', 'finsky']):
        print(line)
