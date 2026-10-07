import subprocess, time

def test_first_boot_simulation():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    print("[1] Remount and push latest webpadinit.sh...")
    subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'])
    subprocess.run([adb, '-s', dev, 'push', 'build_rom/system_root/bin/webpadinit.sh', '/system/bin/webpadinit.sh'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 755 /system/bin/webpadinit.sh'])

    print("[2] Clear ATV data to simulate clean flash state...")
    subprocess.run([adb, '-s', dev, 'shell', 'pm clear ca.dstudio.atvlauncher.pro'])
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/local/tmp/.atv_preset_done'])
    time.sleep(2)

    print("[3] Running webpadinit.sh (Simulating fresh system first-boot)...")
    r = subprocess.run([adb, '-s', dev, 'shell', 'sh /system/bin/webpadinit.sh'], capture_output=True, text=True, timeout=60)
    print("Script output:", r.stdout)

    print("[4] Waiting 3 seconds for ATV to render...")
    time.sleep(3)

    print("[5] Capturing screen to verify first-boot result...")
    subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/first_boot_verified.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/first_boot_verified.png', 
                    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\first_boot_verified.png'])

    print("[+] Test completed! Check first_boot_verified.png")

if __name__ == '__main__':
    test_first_boot_simulation()
