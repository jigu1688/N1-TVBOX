import subprocess
import time

def fix_tile():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    # 1. Clear databases & shared_prefs in ca.dstudio.atvlauncher.pro
    print('[*] Cleaning ATV Launcher Pro cache...')
    subprocess.run([adb, '-s', dev, 'shell', 'rm', '-rf', '/data/data/ca.dstudio.atvlauncher.pro/databases'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm', '-rf', '/data/data/ca.dstudio.atvlauncher.pro/files'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm', '-rf', '/data/data/ca.dstudio.atvlauncher.pro/shared_prefs'])

    # 2. Reinstall new WebPush APK
    print('[*] Reinstalling WebPush APK...')
    subprocess.run([adb, '-s', dev, 'install', '-r', '-d', 'NextGen_隔空传装_v1.0.apk'])

    # 3. Kill and restart launcher
    print('[*] Restarting ATV Launcher Pro...')
    subprocess.run([adb, '-s', dev, 'shell', 'pkill', '-f', 'ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])
    time.sleep(3)

    # 4. Capture screenshot
    print('[*] Capturing screenshot...')
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/atv_horizontal_verified.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_horizontal_verified.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_horizontal_verified.png'])
    print('[+] Complete!')

if __name__ == '__main__':
    fix_tile()
