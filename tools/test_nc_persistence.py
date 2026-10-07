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

print("[*] 1. Kill any existing nc on device:")
run(['shell', 'killall busybox'])
time.sleep(1)

print("[*] 2. Start busybox nc -ll -p 19999 -e /system/bin/do_sleep.sh:")
run(['shell', '/system/xbin/busybox nohup /system/xbin/busybox nc -ll -p 19999 -e /system/bin/do_sleep.sh > /dev/null 2>&1 &'])
time.sleep(1)

print("[*] 3. Check netstat for 19999:")
out, _ = run(['shell', 'netstat -tlpn | grep 19999'])
print("    netstat:", out.strip())

print("[*] 4. Trigger FIRST connection (sending dummy newline, don't sleep yet by checking do_sleep.sh):")
# Let's see if nc accepts connection and stays alive:
s = socket.socket()
s.connect(('192.168.31.115', 19999))
s.sendall(b'ping\n')
s.close()
time.sleep(1)

print("[*] 5. Check if nc is STILL listening after first connection (that is what -ll does!):")
out, _ = run(['shell', 'netstat -tlpn | grep 19999'])
print("    netstat after 1st connection:", out.strip())
