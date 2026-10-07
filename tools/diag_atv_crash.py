import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# 1. Start ATV Launcher explicitly and check errors
print("[*] Starting ATV Launcher Activity...")
p = subprocess.run([adb, '-s', dev, 'shell', 'am start -W -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'], capture_output=True)
print(p.stdout.decode('utf-8', errors='ignore'))
print(p.stderr.decode('utf-8', errors='ignore'))

# 2. Check recent crashes from logcat
p_log = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d -b crash,main | tail -n 40'], capture_output=True)
print("\nLogcat crash snippet:")
for line in p_log.stdout.decode('utf-8', errors='ignore').splitlines():
    if any(k in line.lower() for k in ['fatal', 'crash', 'exception', 'atvlauncher', 'error']):
        print(' ', line)
