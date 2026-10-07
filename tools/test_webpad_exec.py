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
run(['shell', 'mount -o remount,rw /system'])

print("[*] 2. Set label of /system/bin/webpad to adbd_exec:")
run(['shell', 'chcon u:object_r:adbd_exec:s0 /system/bin/webpad'])
out, _ = run(['shell', 'ls -lZ /system/bin/webpad'])
print("    label:", out.strip())

print("[*] 3. Starting webpadservice:")
run(['shell', 'start webpadservice'])
time.sleep(2)

print("[*] 4. Checking init.svc.webpadservice:")
out, _ = run(['shell', 'getprop init.svc.webpadservice'])
print("    init.svc.webpadservice:", out.strip())

print("[*] 5. Checking dmesg for any avc denials on webpad:")
out, _ = run(['shell', 'dmesg | tail -n 15'])
print("    dmesg:\n", out)
