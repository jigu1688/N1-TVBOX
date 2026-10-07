import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

print("[*] 1. Remount rw:")
print(run(['shell', 'mount -o remount,rw /system']))

print("[*] 2. Inspect /system/bin/install-recovery.sh:")
print(run(['shell', 'cat /system/bin/install-recovery.sh']))

print("[*] 3. Set label to install_recovery_exec:")
print(run(['shell', 'chcon u:object_r:install_recovery_exec:s0 /system/bin/install-recovery.sh']))
print(run(['shell', 'ls -lZ /system/bin/install-recovery.sh']))

print("[*] 4. Start flash_recovery:")
print(run(['shell', 'start flash_recovery']))
time.sleep(1)

print("[*] 5. Check init.svc.flash_recovery:")
print(run(['shell', 'getprop init.svc.flash_recovery']))

print("[*] 6. Check dmesg for flash_recovery:")
print(run(['shell', 'dmesg | tail -n 15']))
