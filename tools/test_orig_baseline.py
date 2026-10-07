import zipfile, subprocess, time, sqlite3, os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Sign original APK with testkey
cmd_sign = f'java -jar tools/re_tools/apktool.jar --version' # test java
cmd_apksigner = f'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore tools/re_tools/debug.keystore -storepass android -keypass android -signedjar tools/re_tools/orig_signed.apk "ATV Launcher Pro v0.2.1.apk" androiddebugkey'
subprocess.run(cmd_apksigner, shell=True)

# 2. Push orig_signed to system
subprocess.run([adb, '-s', dev, 'root'])
time.sleep(1)
subprocess.run([adb, '-s', dev, 'remount'])
subprocess.run([adb, '-s', dev, 'push', 'tools/re_tools/orig_signed.apk', '/system/app/ATVLauncher/ATVLauncher.apk'])
subprocess.run([adb, '-s', dev, 'shell', 'chmod 644 /system/app/ATVLauncher/ATVLauncher.apk'])

# 3. pm clear and test
subprocess.run([adb, '-s', dev, 'shell', 'pm clear ca.dstudio.atvlauncher.pro'])
time.sleep(1)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(3)

# 4. Check focus and screencap
r = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows'], capture_output=True, text=True)
for line in r.stdout.split('\n'):
    if 'mCurrentFocus' in line:
        print('Focus:', line.strip())

subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/orig_test.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/orig_test.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\orig_test.png'])

# 5. Pull db
subprocess.run([adb, '-s', dev, 'shell', 'cp /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db /sdcard/orig_s.db'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/orig_s.db', 'orig_s.db'])
if os.path.exists('orig_s.db'):
    conn = sqlite3.connect('orig_s.db')
    c = conn.cursor()
    print('ORIGINAL SECTIONS:')
    for row in c.execute('SELECT uuid, title, visible, [primary], rows, cols, [item-height] FROM sections'):
        print(row)
    print('\nORIGINAL APPLICATIONS:')
    for row in c.execute('SELECT [package-name], [section-uuid], [position], [border-radius], [display-mode], [background-color] FROM applications'):
        print(row)
