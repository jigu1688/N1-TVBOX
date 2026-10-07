import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

r = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows'], capture_output=True, text=True)
for line in r.stdout.split('\n'):
    if 'mCurrentFocus' in line or 'mFocusedApp' in line:
        print('Focus:', line.strip())

r = subprocess.run([adb, '-s', dev, 'shell', 'sqlite3 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db "SELECT uuid, title, visible, rows, cols FROM sections;"'], capture_output=True, text=True)
print('Database sections:\n', r.stdout)

r = subprocess.run([adb, '-s', dev, 'shell', 'sqlite3 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db "SELECT [package-name], [section-uuid], [position], [border-radius] FROM applications;"'], capture_output=True, text=True)
print('Database applications:\n', r.stdout)
