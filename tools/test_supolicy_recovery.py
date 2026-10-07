import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

script_content = """#!/system/bin/sh
/system/xbin/supolicy --live "permissive install_recovery;"
/system/bin/run_nc.sh &
exit 0
"""

with open("tools/temp_ir.sh", "w", newline="\n") as f:
    f.write(script_content)

run(['push', 'tools/temp_ir.sh', '/system/bin/install-recovery.sh'])
run(['shell', 'chmod 755 /system/bin/install-recovery.sh'])
run(['shell', 'chcon u:object_r:install_recovery_exec:s0 /system/bin/install-recovery.sh'])

print("Starting flash_recovery...")
run(['shell', 'start flash_recovery'])
time.sleep(1)

print("dmesg:")
out, _ = run(['shell', 'dmesg | tail -n 15'])
print(out)

print("netstat 19999:")
out, _ = run(['shell', 'netstat -tlpn | grep 19999'])
print(out)
