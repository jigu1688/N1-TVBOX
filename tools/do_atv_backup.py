import subprocess, time, sys, os
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Take a snapshot of /sdcard before backup
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /sdcard -name "*.json" -o -name "*.atvl" -o -name "*backup*" -o -name "*ATVLauncher*" 2>/dev/null'], 
    capture_output=True, text=True)
print('Files before backup:')
print(r.stdout.strip() or 'NONE')

# Click "备份" (should be already selected/highlighted)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_ENTER'])
time.sleep(3)

# Screenshot to see result
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/after_backup.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/after_backup.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\after_backup.png'])

# Check what files were created
time.sleep(1)
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /sdcard -name "*.json" -o -name "*.atvl" -o -name "*backup*" -o -name "*ATVLauncher*" -o -name "*atv*" 2>/dev/null'], 
    capture_output=True, text=True)
print('\nFiles after backup:')
print(r.stdout.strip() or 'NONE')

# Also check /data/data for changes
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f -newer /data/local/tmp/.atv_preset_done 2>/dev/null'], 
    capture_output=True, text=True)
print('\nNew files in app data:')
print(r.stdout.strip() or 'NONE')

# Broader search for any recently modified files
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /sdcard -maxdepth 3 -type f -newer /data/local/tmp/.atv_preset_done 2>/dev/null'], 
    capture_output=True, text=True)
print('\nRecently modified files on sdcard:')
print(r.stdout.strip() or 'NONE')

print('\nDone')
