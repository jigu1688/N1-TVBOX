import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Find all files under ATV data dir
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f 2>/dev/null'], 
    capture_output=True, text=True)
print('All files in ATV data:')
print(r.stdout)

# Check /data/user_de
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/user_de/0/ca.dstudio.atvlauncher.pro/ -type f 2>/dev/null'], 
    capture_output=True, text=True)
print('\nAll files in user_de:')
print(r.stdout or 'NONE')

# Check ATV APK version
r = subprocess.run([adb, '-s', dev, 'shell', 
    'dumpsys package ca.dstudio.atvlauncher.pro'], 
    capture_output=True, text=True)
for line in r.stdout.split('\n'):
    line = line.strip()
    if any(k in line.lower() for k in ['version', 'codepath', 'resourcepath']):
        print(line)

# Now manually add something to the ATV layout and check what files change
print('\n\n=== Now checking what the previous injection did ===')
# Let's inject the DB again using our safe_deploy method
subprocess.run([adb, '-s', dev, 'shell', 
    'am force-stop ca.dstudio.atvlauncher.pro'])

import time
time.sleep(1)

# Create databases dir and inject
subprocess.run([adb, '-s', dev, 'shell', 
    'mkdir -p /data/data/ca.dstudio.atvlauncher.pro/databases'])
subprocess.run([adb, '-s', dev, 'shell', 
    'cp /system/etc/atvlauncher/sections.db /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db'])
subprocess.run([adb, '-s', dev, 'shell', 
    'rm -f /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-shm'])

# Fix perms
subprocess.run([adb, '-s', dev, 'shell', 
    'chown -R u0_a25:u0_a25 /data/data/ca.dstudio.atvlauncher.pro/databases'])
subprocess.run([adb, '-s', dev, 'shell', 
    'chmod -R 770 /data/data/ca.dstudio.atvlauncher.pro/databases'])

# Start ATV
subprocess.run([adb, '-s', dev, 'shell', 
    'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(5)

# Screenshot
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/after_inject2.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/after_inject2.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\after_inject2.png'])

# Check files now
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f 2>/dev/null'], 
    capture_output=True, text=True)
print('\nAll files AFTER injection:')
print(r.stdout)

print('Done')
