import subprocess
import time

def test_hardcoded_apk():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    print("[1] Pushing hardcoded customized ATVLauncher.apk to /system/app/...")
    subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'])
    subprocess.run([adb, '-s', dev, 'push', 'tools/re_tools/ATVLauncher_Custom_Hardcoded.apk', '/system/app/ATVLauncher/ATVLauncher.apk'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 644 /system/app/ATVLauncher/ATVLauncher.apk'])

    print("[2] Complete Data Wipe (pm clear) to simulate Clean Flash state...")
    subprocess.run([adb, '-s', dev, 'shell', 'pm clear ca.dstudio.atvlauncher.pro'])
    # Remove any extra flag or backup
    subprocess.run([adb, '-s', dev, 'shell', 'rm -rf /data/data/ca.dstudio.atvlauncher.pro'])
    time.sleep(2)

    print("[3] Launching ATV Launcher Pro from clean state...")
    subprocess.run([adb, '-s', dev, 'shell', 'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
    time.sleep(5)

    print("[4] Capturing live screen...")
    subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/hardcoded_atv_test.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/hardcoded_atv_test.png', 
                    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\hardcoded_atv_test.png'])

    print("[+] Test completed! Check hardcoded_atv_test.png")

if __name__ == '__main__':
    test_hardcoded_apk()
