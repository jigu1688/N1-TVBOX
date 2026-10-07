import subprocess
import time

def main():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'
    
    print("[1] Push updated webpadinit.sh to device...")
    subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'])
    subprocess.run([adb, '-s', dev, 'push', 'build_rom/system_root/bin/webpadinit.sh', '/system/bin/webpadinit.sh'])
    subprocess.run([adb, '-s', dev, 'shell', 'chmod 755 /system/bin/webpadinit.sh'])
    
    print("[2] Remove preset flag to simulate fresh boot...")
    subprocess.run([adb, '-s', dev, 'shell', 'rm -f /data/local/tmp/.atv_preset_done'])
    
    print("[3] Running webpadinit.sh directly (simulating boot)...")
    r = subprocess.run([adb, '-s', dev, 'shell', 'sh /system/bin/webpadinit.sh'], 
                       capture_output=True, text=True, timeout=60)
    print("stdout:", r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
    print("stderr:", r.stderr[-500:] if len(r.stderr) > 500 else r.stderr)
    
    print("[4] Wait and capture screen...")
    time.sleep(2)
    subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/sync_inject_test.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/sync_inject_test.png', 
                    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\sync_inject_test.png'])
    
    print("[5] Verify preset flag was created...")
    r = subprocess.run([adb, '-s', dev, 'shell', 'ls -la /data/local/tmp/.atv_preset_done'], 
                       capture_output=True, text=True)
    print(r.stdout.strip())
    
    print("[6] Verify DB size on device...")
    r = subprocess.run([adb, '-s', dev, 'shell', 'ls -la /data/data/ca.dstudio.atvlauncher.pro/databases/'], 
                       capture_output=True, text=True)
    print(r.stdout)
    
    print("[+] Done!")

if __name__ == '__main__':
    main()
