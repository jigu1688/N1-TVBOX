import subprocess, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Snapshot 1: all files before any interaction
print("=== BEFORE state ===")
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f 2>/dev/null | sort'], 
    capture_output=True, text=True)
before_files = set(r.stdout.strip().split('\n')) if r.stdout.strip() else set()
print(f'Files: {len(before_files)}')
for f in sorted(before_files):
    print(f'  {f}')

# Now interact with ATV - press menu key to open settings  
print("\n=== Pressing MENU to configure ATV ===")
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_HOME'])
time.sleep(2)

# Long press on an item - press MENU or try to rearrange
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_MENU'])
time.sleep(3)

# Screenshot
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/atv_menu.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_menu.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_menu.png'])

# Check what files changed
print("\n=== AFTER menu interaction ===")
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f 2>/dev/null | sort'], 
    capture_output=True, text=True)
after_files = set(r.stdout.strip().split('\n')) if r.stdout.strip() else set()
print(f'Files: {len(after_files)}')

new_files = after_files - before_files
if new_files:
    print('\nNEW files created:')
    for f in sorted(new_files):
        print(f'  {f}')
else:
    print('\nNo new files created')

# Check shared_prefs again
r = subprocess.run([adb, '-s', dev, 'shell', 
    'ls -la /data/data/ca.dstudio.atvlauncher.pro/shared_prefs/'], 
    capture_output=True, text=True)
print(f'\nSharedPrefs: {r.stdout.strip()}')

# List ALL files recursively with size and timestamp
r = subprocess.run([adb, '-s', dev, 'shell', 
    'find /data/data/ca.dstudio.atvlauncher.pro/ -type f -exec ls -la {} ;'], 
    capture_output=True, text=True)
print(f'\nAll files with details:')
print(r.stdout)
