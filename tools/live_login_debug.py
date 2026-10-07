import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

# Connect
subprocess.run([adb, 'connect', dev])
time.sleep(1)

# Check packages
res_pkgs = subprocess.run([adb, '-s', dev, 'shell', 'pm list packages -f'], capture_output=True, text=True)
print('Current Google Packages on device:')
for l in res_pkgs.stdout.splitlines():
    if any(k in l.lower() for k in ['google', 'vending', 'gms']):
        print('  [+]', l)

# Check dumpsys account
res_acc = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys account'], capture_output=True, text=True)
print('\nAccount Authenticators:')
for l in res_acc.stdout.splitlines():
    if any(k in l for k in ['Account', 'Authenticator', 'com.google', 'Registered']):
        print('  ', l)

# Check logcat
res_logs = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d | tail -n 80'], capture_output=True, text=True, errors='ignore')
print('\nRecent 80 log lines:\n', res_logs.stdout)

# Pull screenshot
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/play_login_debug.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/play_login_debug.png', 'C:/Users/jigu/.gemini/antigravity-ide/brain/59392cea-4993-4618-813e-365af128b445/play_login_debug.png'])
print('[+] Screenshot pulled to artifacts!')
