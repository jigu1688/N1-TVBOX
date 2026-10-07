import subprocess
import time
import socket

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

print("[*] 1. Starting /system/bin/run_nc.sh via busybox nohup...")
run(['shell', '/system/xbin/busybox nohup /system/bin/sh /system/bin/run_nc.sh > /dev/null 2>&1 &'])
time.sleep(1)

print("[*] 2. Checking ps for run_nc.sh / busybox nc:")
out, _ = run(['shell', 'ps | grep busybox'])
print("    ps:", out.strip())

print("[*] 3. Checking netstat for 19999:")
out, _ = run(['shell', 'netstat -tlpn | grep 19999'])
print("    netstat:", out.strip())

print("[*] 4. Triggering test sleep via 127.0.0.1:19999 inside box...")
out, err = run(['shell', 'echo sleep | /system/xbin/busybox nc 127.0.0.1 19999'])
print("    trigger out:", out, "err:", err)
time.sleep(2)

print("[*] 5. Checking mWakefulness:")
out, _ = run(['shell', 'dumpsys power | grep mWakefulness'])
print("    power state:", out.strip())
