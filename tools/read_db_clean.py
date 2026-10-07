import subprocess, sqlite3, os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

r = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows'], capture_output=True, text=True)
for line in r.stdout.split('\n'):
    if 'mCurrentFocus' in line:
        print('Focus:', line.strip())

if os.path.exists('s.db'):
    os.remove('s.db')

subprocess.run([adb, '-s', dev, 'shell', 'cp /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db /sdcard/s.db'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/s.db', 's.db'])

if os.path.exists('s.db'):
    conn = sqlite3.connect('s.db')
    c = conn.cursor()
    print('SECTIONS:')
    for row in c.execute('SELECT uuid, title, visible, [primary], rows, cols, [item-height] FROM sections'):
        print(row)
    print('\nAPPLICATIONS:')
    for row in c.execute('SELECT [package-name], [section-uuid], [position], [border-radius], [display-mode], [background-color] FROM applications'):
        print(row)
