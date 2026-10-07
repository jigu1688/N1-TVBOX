import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run_shell(cmd):
    r = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip()

print("[*] Connecting...")
subprocess.run([adb, 'connect', dev], capture_output=True, text=True)

print("=== 1. Init services status ===")
out, _ = run_shell("getprop | grep -E 'init.svc'")
for line in out.splitlines():
    if any(k in line for k in ['sleep', 'webpad', 'daemon']):
        print("  ", line)

print("=== 2. Listening ports (netstat) ===")
out, _ = run_shell("netstat -tlpn")
print(out)

print("=== 3. Processes matching nc, sleep, PhiTvSettings ===")
out, _ = run_shell("ps | grep -E 'nc|sleep|busybox|settings'")
print(out)

print("=== 4. Logcat for SafeSleepManager or sleepdaemon ===")
out, _ = run_shell("logcat -d | grep -E 'SafeSleepManager|sleepdaemon|ShutdownActivity'")
print(out[-2000:] if len(out) > 2000 else out)

print("=== 5. PowerManager state ===")
out, _ = run_shell("dumpsys power | grep -E 'mWakefulness|Display Power'")
print(out)
