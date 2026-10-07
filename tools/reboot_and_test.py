import subprocess
import time
import socket

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

print("[*] 1. Rebooting box...")
subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
subprocess.run([adb, '-s', dev, 'reboot'], capture_output=True, text=True)

print("[*] 2. Waiting 25s for box to boot up...")
time.sleep(25)

for attempt in range(15):
    print(f"[*] Attempt {attempt+1} connecting to {dev}...")
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    r = subprocess.run([adb, '-s', dev, 'shell', 'getprop sys.boot_completed'], capture_output=True, text=True)
    if '1' in r.stdout:
        print("[+] System boot completed!")
        break
    time.sleep(3)

print("=== CHECK SERVICES AFTER REBOOT ===")
r = subprocess.run([adb, '-s', dev, 'shell', 'getprop | grep -E "init.svc.(sleep|webpad)"'], capture_output=True, text=True)
print("init services:\n", r.stdout)

r = subprocess.run([adb, '-s', dev, 'shell', 'netstat -tlpn | grep -E "19999|2323"'], capture_output=True, text=True)
print("netstat:\n", r.stdout)

r = subprocess.run([adb, '-s', dev, 'shell', 'dmesg | grep -E "cannot execve|avc: denied" | tail -n 15'], capture_output=True, text=True)
print("dmesg errors:\n", r.stdout)
