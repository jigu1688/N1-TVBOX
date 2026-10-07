import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

run(['shell', 'mount -o remount,rw /system'])

# 1. Update sleepdaemon.rc
rc_content = """service sleepdaemon /system/xbin/busybox nc -ll -p 19999 -e /system/bin/do_sleep.sh
    class main
    user root
    group root
    seclabel u:r:su:s0
"""
with open("tools/temp_sleep.rc", "w", newline="\n") as f:
    f.write(rc_content)

run(['push', 'tools/temp_sleep.rc', '/system/etc/init/sleepdaemon.rc'])
run(['shell', 'chmod 644 /system/etc/init/sleepdaemon.rc'])
run(['shell', 'chown 0:0 /system/etc/init/sleepdaemon.rc'])

# 2. Update daemonsu.rc to ensure webpadservice uses adbd_exec and sleepdaemon uses su_exec
daemonsu_rc = """# powered by Rush , mod by webpad

on boot
    start webpadservice
    start sleepdaemon

on property:ro.debuggable=0
    start webpadservice

on property:ro.debuggable=1
    start webpadservice

service webpadservice /system/bin/webpad
    class main
    group root shell log readproc
    oneshot
    seclabel u:r:adbd:s0

service sleepdaemon /system/xbin/busybox nc -ll -p 19999 -e /system/bin/do_sleep.sh
    class main
    user root
    group root
    seclabel u:r:su:s0
"""
with open("tools/temp_daemonsu.rc", "w", newline="\n") as f:
    f.write(daemonsu_rc)

run(['push', 'tools/temp_daemonsu.rc', '/system/etc/init/daemonsu.rc'])
run(['shell', 'chmod 644 /system/etc/init/daemonsu.rc'])
run(['shell', 'chown 0:0 /system/etc/init/daemonsu.rc'])

# 3. Set proper contexts
run(['shell', 'chcon u:object_r:adbd_exec:s0 /system/bin/webpad'])
run(['shell', 'chcon u:object_r:su_exec:s0 /system/xbin/busybox'])
run(['shell', 'chcon u:object_r:su_exec:s0 /system/bin/do_sleep.sh'])
run(['shell', 'chcon u:object_r:su_exec:s0 /system/bin/run_nc.sh'])

print("[*] Checked labels:")
print(run(['shell', 'ls -lZ /system/bin/webpad /system/xbin/busybox /system/bin/do_sleep.sh']))
